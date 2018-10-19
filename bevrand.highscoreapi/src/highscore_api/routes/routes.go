package routes

import (
	"context"
	"encoding/json"
	"github.com/gin-gonic/gin"
	"github.com/opentracing/opentracing-go"
	openlog "github.com/opentracing/opentracing-go/log"
	"github.com/swaggo/gin-swagger"
	"github.com/swaggo/gin-swagger/swaggerFiles"
	"log"
	"net/http"
	"highscore_api/docs"
	"highscore_api/handlers"
	"highscore_api/models"
)

func InitRoutes() *gin.Engine {
	r := gin.Default()

	// programatically set swagger info
	docs.SwaggerInfo.Title = "Swagger Example API"
	docs.SwaggerInfo.Description = "This is a sample server Golang server."
	docs.SwaggerInfo.Version = "1.0"
	docs.SwaggerInfo.Host = "localhost"
	docs.SwaggerInfo.BasePath = "/v2"

	//pingpong
	r.GET("/ping", PingPong)
	//redis
	r.GET("/api/v1/redis/:user/:playList",  RouteShowHighScore)
	r.POST("/api/v1/redis/:user/:playList", RouteIncrementHighscore)

	// use ginSwagger middleware to serve the API docs
	r.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))

	return r
}


// @Summary Ping Pong
// @Description Is the api up?
// @ID ping-pong
// @Accept  json
// @Produce  json
// @Success 200 {string} string	"ok"
// @Router /ping [get]
func PingPong(c *gin.Context) {
	c.JSON(200, gin.H{
		"message": "pong",
	})
}

// @Summary Show the high scores
// @Description get list by user and playlistnames
// @ID get-high-scores
// @Accept  json
// @Produce  json
// @Param user path string true "user"
// @Param playList path string true "playlist"
// @Success 200 {array} models.Score
// @Failure 400 {object} models.ErrorModel
// @Failure 404 {object} models.ErrorModel
// @Failure 500 {object} models.ErrorModel
// @Router /api/v1/redis/{user}/{playList} [get]
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

// @Summary Up or create a highscore
// @Description Increase the scores
// @ID post-high-scores
// @Accept  json
// @Produce  json
// @Param Body body models.PostObject true "Up highscrore"
// @Success 200 {string} string "success"
// @Failure 400 {object} models.ErrorModel
// @Failure 404 {object} models.ErrorModel
// @Failure 500 {object} models.ErrorModel
// @Router /api/v1/redis/{user}/{playList} [post]
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