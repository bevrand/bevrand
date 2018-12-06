package routes

import (
	"context"
	"encoding/json"
	"github.com/bevrand/bevrand/bevrand.highscoreapi/handlers"
	"github.com/bevrand/bevrand/bevrand.highscoreapi/models"
	"github.com/gin-gonic/gin"
	"github.com/opentracing/opentracing-go"
	openlog "github.com/opentracing/opentracing-go/log"
	"log"
	"net/http"
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
		respondWithJSON(c.Writer, c.Request, "sdf", http.StatusBadRequest)
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

func respondWithJSON(w http.ResponseWriter, r *http.Request, model string, code int) {
	body, err := json.MarshalIndent(model, "", "    ")
	if err != nil {
		log.Println(err)
	}
	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	w.WriteHeader(code)
	w.Write(body)
}