package routes

import (
	"context"
	"encoding/json"
	"github.com/bevrand/bevrand/bevrand.highscoreapi/handlers"
	"github.com/bevrand/bevrand/bevrand.highscoreapi/models"
	"github.com/gin-gonic/gin"
	"github.com/opentracing/opentracing-go"
	openlog "github.com/opentracing/opentracing-go/log"
	"gopkg.in/oauth2.v3/utils/uuid"
	"log"
	"net/http"
	"strconv"
)

func InitRoutes() *gin.Engine {
	r := gin.Default()

	//pingpong
	r.GET("/ping", PingPong)
	//redis
	r.GET("/api/v1/redis/:user/:playList",  RouteShowHighScore)
	r.POST("/api/v1/redis/:user/:playList", RouteIncrementHighscore)

	return r
}

func PingPong(c *gin.Context) {
	c.JSON(200, gin.H{
		"message": "pong",
	})
}


func RouteShowHighScore(c *gin.Context) {
	tracer:= opentracing.GlobalTracer()
	span := tracer.StartSpan("Getting data from Redis")
	span.SetTag("Method", "RouteShowHighScore")
	span.LogFields(
		openlog.String("method", c.Request.Method),
		openlog.String("path", c.Request.URL.Path),
		openlog.String("host", c.Request.Host),
	)

	ctx := context.Background()
	ctx = opentracing.ContextWithSpan(ctx, span)

	user := c.Param("user")
	playlist := c.Param("playList")
	highScores := handlers.ShowHighScores(user, playlist, c, ctx)
	respondWithJson(c.Writer, c.Request.Response.StatusCode, highScores, ctx)
	json.NewEncoder(c.Writer).Encode(highScores)

	span.Finish()
}


func RouteIncrementHighscore(c *gin.Context) {
	tracer:= opentracing.GlobalTracer()
	span := tracer.StartSpan("Posting data to Redis")
	span.SetTag("Method", "RouteIncrementHighscore")

	var po models.PostObject
	decoder := json.NewDecoder(c.Request.Body)
	if err := decoder.Decode(&po); err != nil {
		uuid, _ := uuid.NewRandom()
		decodingError := models.ErrorModel{
			Message: err.Error(),
			UniqueCode: uuid}

		respondWithJson(c.Writer, http.StatusBadRequest, decodingError, ctx)
		return
	}

	body, _ := json.Marshal(po)

	span.LogFields(
		openlog.String("method", c.Request.Method),
		openlog.String("path", c.Request.URL.Path),
		openlog.String("body", string(body)),
		openlog.String("host", c.Request.Host),
	)
	ctx := context.Background()
	ctx = opentracing.ContextWithSpan(ctx, span)

	user := c.Param("user")
	playlist := c.Param("playList")

	handlers.CreateNewHighScore(user, playlist, po.Drink, ctx)

	json.NewEncoder(c.Writer).Encode("success")

	span.Finish()
}

func respondWithJson(w http.ResponseWriter, code int, payload interface{}, ctx context.Context) {
	span, _ := opentracing.StartSpanFromContext(ctx, "Response")
	span.SetTag("Method", "ShowHighScores")

	response, _ := json.Marshal(payload)
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(code)
	w.Write(response)
	span.LogFields(
		openlog.String("http_status_code", strconv.Itoa(code)),
		openlog.String("body", string(response)),
	)
	defer span.Finish()
}