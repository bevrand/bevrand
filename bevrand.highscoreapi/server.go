package main

import (
	"context"
	"encoding/json"
	"fmt"
	"github.com/gin-gonic/gin"
	"github.com/joho/godotenv"
	"github.com/mediocregopher/radix.v2/pool"
	"github.com/opentracing/opentracing-go"
	openlog "github.com/opentracing/opentracing-go/log"
	"github.com/uber/jaeger-client-go/config"
	"gopkg.in/oauth2.v3/utils/uuid"
	"io"
	"log"
	"net/http"
	"os"
	"strconv"
)

var db *pool.Pool
var GLOBALNAME = "global"
var GLOBALLIST = "globalhighscore"

type ErrorModel struct {
	Message	string `json:"errorMessage"`
	UniqueCode string `json:"uniqueCode"`
}

type PostObject struct {
	Drink	string `json:"drink"`
}

type Score struct {
	Drink	string `json:"drink"`
	Rolled int `json:"rolled"`
}

func ConnectRedis() {
	var err error
	// Establish a pool of 10 connections to the Redis server listening on
	// port 6379 of the variable that has been used

	redisUrl := os.Getenv("REDIS_URL") + ":6379"
	fmt.Println(redisUrl)
	db, err = pool.New("tcp", redisUrl, 10)
	if err != nil {
		log.Panic(err)
	}
}

func main() {
	GetEnvFile()
	ConnectRedis()
	//init jaeger
	jaegerUrl := os.Getenv("JAEGER_AGENT_HOST")
	jaegerPort := os.Getenv("JAEGER_AGENT_PORT")
	jaegerConfig := jaegerUrl + ":" + jaegerPort
	println(jaegerConfig)

	tracer, closer := initJaeger("HighScoreApi", jaegerConfig)
	defer closer.Close()
	opentracing.SetGlobalTracer(tracer)

	span := tracer.StartSpan("StartingServer")
	span.SetTag("event", "Starting GINGONIC")
	defer span.Finish()

	ctx := context.Background()
	ctx = opentracing.ContextWithSpan(ctx, span)

	logValue := fmt.Sprintf("Starting server for HighScores!")
	printServerInfo(ctx, logValue)
	span.Finish()

	//init router
	r := InitRoutes()
	r.Run(":5000")
}

func GetEnvFile() {
	env := os.Getenv("GO_ENV")
	if "" == env {
		env = "development"
	}

	err := godotenv.Load(".env." + env)
	if err != nil {
		log.Fatal(err)
	}
}
// Init returns an instance of Jaeger Tracer that samples 100% of traces and logs all spans to stdout.
func initJaeger(service string, host string) (opentracing.Tracer, io.Closer) {
	cfg := &config.Configuration{
		Sampler: &config.SamplerConfig{
			Type:  "const",
			Param: 1,
		},
		Reporter: &config.ReporterConfig{
			LogSpans: true,
			LocalAgentHostPort: host,
		},
	}
	println(cfg)

	tracer, closer, err := cfg.New(service, nil)
	if err != nil {
		panic(fmt.Sprintf("ERROR: cannot init Jaeger: %v\n", err))
	}
	return tracer, closer
}

func printServerInfo(ctx context.Context, serverInfo string){
	span, _ := opentracing.StartSpanFromContext(ctx, "ServerInfo")
	defer span.Finish()

	span.LogKV("event", serverInfo)
}


func InitRoutes() *gin.Engine {
	r := gin.Default()

	//pingpong
	r.GET("/ping", PingPong)
	//redis
	r.GET("/api/v1/highscore/:user/:playList",  RouteShowHighScore)
	r.GET("/api/v1/highscore",  RouteShowAllHighScore)
	r.POST("/api/v1/highscore/:user/:playList", RouteIncrementHighscore)

	return r
}

func PingPong(c *gin.Context) {
	c.JSON(200, gin.H{
		"message": "pong",
	})
}

func RouteShowAllHighScore(c *gin.Context) {
	tracer:= opentracing.GlobalTracer()
	span := tracer.StartSpan("Getting data from Redis")
	span.SetTag("Method", "RouteShowAllHighScore")

	ctx := context.Background()
	ctx = opentracing.ContextWithSpan(ctx, span)

	span.LogFields(
		openlog.String("method", c.Request.Method),
		openlog.String("path", c.Request.URL.Path),
		openlog.String("host", c.Request.Host),
	)

	highScores, code := ShowHighScores(GLOBALNAME, GLOBALLIST, c, ctx)
	if highScores != nil {
		respondWithJson(c, code, highScores, ctx)
	}
	span.Finish()
}

func RouteShowHighScore(c *gin.Context) {
	tracer:= opentracing.GlobalTracer()
	span := tracer.StartSpan("Getting data from Redis")
	span.SetTag("Method", "RouteShowHighScore")

	ctx := context.Background()
	ctx = opentracing.ContextWithSpan(ctx, span)

	span.LogFields(
		openlog.String("method", c.Request.Method),
		openlog.String("path", c.Request.URL.Path),
		openlog.String("host", c.Request.Host),
	)

	user := c.Param("user")
	playlist := c.Param("playList")
	highScores, code := ShowHighScores(user, playlist, c, ctx)
	if highScores != nil {
		respondWithJson(c, code, highScores, ctx)
	}
	span.Finish()
}


func RouteIncrementHighscore(c *gin.Context) {
	tracer:= opentracing.GlobalTracer()
	span := tracer.StartSpan("Posting data to Redis")
	span.SetTag("Method", "RouteIncrementHighscore")

	ctx := context.Background()
	ctx = opentracing.ContextWithSpan(ctx, span)

	var po PostObject
	decoder := json.NewDecoder(c.Request.Body)
	if err := decoder.Decode(&po); err != nil {
		b, _ := uuid.NewRandom()
		localUuid := fmt.Sprintf("%x-%x-%x-%x-%x",
			b[0:4], b[4:6], b[6:8], b[8:10], b[10:])
		decodingError := ErrorModel{
			Message: err.Error(),
			UniqueCode: localUuid}

		respondWithJson(c, http.StatusBadRequest, decodingError, ctx)
		return
	}

	body, _ := json.Marshal(po)

	span.LogFields(
		openlog.String("method", c.Request.Method),
		openlog.String("path", c.Request.URL.Path),
		openlog.String("body", string(body)),
		openlog.String("host", c.Request.Host),
	)


	user := c.Param("user")
	playlist := c.Param("playList")

	CreateNewHighScore(user, playlist, po.Drink, ctx)

	c.Writer.WriteHeader(http.StatusCreated)
	span.Finish()
}

func ShowHighScores(user string, playlist string, c *gin.Context, ctx context.Context) ([]Score, int) {
	span, _ := opentracing.StartSpanFromContext(ctx, "ShowHighScores")
	span.SetTag("Method", "ShowHighScores")
	defer span.Finish()
	key := user + ":" + playlist

	res, err := db.Cmd("EXISTS", key).Int()
	if err != nil {
		log.Fatal(err)
	}
	exists := res != 0
	var redisResult []Score

	//todo: add this to middleware
	if !exists {
		span.LogFields(
			openlog.String("http_status_code", "404"),
			openlog.String("body", "not found"),
		)
		span.Finish()
		b, _ := uuid.NewRandom()
		localUuid := fmt.Sprintf("%x-%x-%x-%x-%x",
			b[0:4], b[4:6], b[6:8], b[8:10], b[10:])
		notFoundError := ErrorModel{
			Message: "Could not find combination of user: " + user + " & list: " + playlist,
			UniqueCode: localUuid}
		respondWithJson(c, http.StatusNotFound, notFoundError, ctx)
		return nil, 0
	}

	result, err := db.Cmd("HGETALL", key).Map()
	if err != nil {
		log.Fatal(err)
	}
	for drink, score := range result{
		i, err := strconv.Atoi(score)
		if err != nil {
			log.Fatal("cannot convert string to int")
		}
		newScore := Score{
			Drink: drink,
			Rolled: i}
		redisResult = append(redisResult, newScore)
	}
	body, _ := json.Marshal(redisResult)

	span.LogFields(
		openlog.String("http_status_code", "200"),
		openlog.String("body", string(body)),
	)
	return redisResult, http.StatusOK
}

func CreateNewHighScore(user string, playlist string, drink string, ctx context.Context) {
	span, _ := opentracing.StartSpanFromContext(ctx, "CreateNewHighScore")
	span.SetTag("Method", "IncreaseHighScore")

	defer span.Finish()
	key := user + ":" + playlist

	res, err := db.Cmd("EXISTS", key).Int()
	if err != nil {
		log.Fatal(err)
	}
	exists := res != 0

	if !exists {
		span.LogFields(
			openlog.String("http_status_code", "200"),
			openlog.String("body", "New entry, setting new key: " + key),
		)
		err = db.Cmd("HMSET", key, drink, 1).Err
		if err != nil {
			log.Fatal(err)
		}
		return
	}

	err = db.Cmd("HINCRBY", key, drink, 1).Err
	if err != nil {
		log.Fatal(err)
	}
	span.LogFields(
		openlog.String("http_status_code", "200"),
		openlog.String("body", "Increased " + drink + " by 1"),
	)

	IncreaseGlobalCount(drink, ctx)
	return
}

func IncreaseGlobalCount(drink string, ctx context.Context){
	span, _ := opentracing.StartSpanFromContext(ctx, "IncreaseGlobalCount")
	span.SetTag("Method", "GlobalHighscore")

	defer span.Finish()
	key := GLOBALNAME + ":" + GLOBALLIST

	res, err := db.Cmd("EXISTS", key).Int()
	if err != nil {
		log.Fatal(err)
	}
	exists := res != 0

	if !exists {
		span.LogFields(
			openlog.String("http_status_code", "200"),
			openlog.String("body", "New entry, setting new key: " + key),
		)
		err = db.Cmd("HMSET", key, drink, 1).Err
		if err != nil {
			log.Fatal(err)
		}
		return
	}

	err = db.Cmd("HINCRBY", key, drink, 1).Err
	if err != nil {
		log.Fatal(err)
	}
	span.LogFields(
		openlog.String("http_status_code", "200"),
		openlog.String("body", "Increased " + drink + " by 1"),
	)
	return
}

func respondWithJson(c *gin.Context, code int, payload interface{}, ctx context.Context) {
	span, _ := opentracing.StartSpanFromContext(ctx, "Response")
	span.SetTag("Method", "ResponseWriter")

	response, _ := json.Marshal(payload)
	c.Writer.Header().Set("Content-Type", "application/json")
	c.Writer.WriteHeader(code)
	c.JSON(code, payload)
	span.LogFields(
		openlog.String("http_status_code", strconv.Itoa(code)),
		openlog.String("body", string(response)),
	)
	defer span.Finish()
}