package main

import (
	"context"
	"encoding/json"
	"github.com/gin-gonic/gin"
	"github.com/opentracing/opentracing-go"
	"github.com/opentracing/opentracing-go/ext"
	openlog "github.com/opentracing/opentracing-go/log"
	"net/http"
	"strconv"
	"strings"
)

// InitRoutes creates a gin router
func InitRoutes() *gin.Engine {
	r := gin.Default()

	//pingpong
	r.GET("/ping", PingPong)
	//redis
	r.GET("/api/v1/highscores/:user/:playList/", RouteShowHighScore)
	r.GET("/api/v1/highscores/", RouteShowAllHighScore)
	r.POST("/api/v1/highscores/:user/:playList/", RouteIncrementHighscore)

	return r
}

// RouteShowAllHighScore route to get the global count
func RouteShowAllHighScore(c *gin.Context) {
	spanCtx, _ := opentracing.GlobalTracer().Extract(opentracing.HTTPHeaders, opentracing.HTTPHeadersCarrier(c.Request.Header))
	span := opentracing.GlobalTracer().StartSpan("ShowGlobalHighScore", ext.RPCServerOption(spanCtx))
	defer span.Finish()

	ctx := context.Background()
	ctx = opentracing.ContextWithSpan(ctx, span)

	span.LogFields(
		openlog.String(method, c.Request.Method),
		openlog.String(path, c.Request.URL.Path),
		openlog.String(host, c.Request.Host),
	)

	highScores, code := ShowHighScores(ctx, GLOBALNAME, GLOBALLIST, c)
	if highScores != nil {
		respondWithJSON(ctx, c, code, highScores)
	}
	span.Finish()
}

// RouteShowHighScore route for returning a user and playlist highscore
func RouteShowHighScore(c *gin.Context) {
	spanCtx, _ := opentracing.GlobalTracer().Extract(opentracing.HTTPHeaders, opentracing.HTTPHeadersCarrier(c.Request.Header))
	span := opentracing.GlobalTracer().StartSpan("ShowHighScore", ext.RPCServerOption(spanCtx))
	defer span.Finish()

	ctx := context.Background()
	ctx = opentracing.ContextWithSpan(ctx, span)

	span.LogFields(
		openlog.String(method, c.Request.Method),
		openlog.String(path, c.Request.URL.Path),
		openlog.String(host, c.Request.Host),
	)

	user := c.Param("user")
	playlist := c.Param("playList")
	highScores, code := ShowHighScores(ctx, user, playlist, c)
	if highScores != nil {
		respondWithJSON(ctx, c, code, highScores)
	}
	span.Finish()
}

// RouteIncrementHighscore route for increasing a highscore and also increases global count
func RouteIncrementHighscore(c *gin.Context) {
	spanCtx, _ := opentracing.GlobalTracer().Extract(opentracing.HTTPHeaders, opentracing.HTTPHeadersCarrier(c.Request.Header))
	span := opentracing.GlobalTracer().StartSpan("IncrementHighScore", ext.RPCServerOption(spanCtx))
	defer span.Finish()

	ctx := context.Background()
	ctx = opentracing.ContextWithSpan(ctx, span)

	var po PostObject
	decoder := json.NewDecoder(c.Request.Body)
	if err := decoder.Decode(&po); err != nil {
		localUUID := createGUID()
		decodingError := ErrorModel{
			Message:    err.Error(),
			UniqueCode: localUUID}

		respondWithJSON(ctx, c, http.StatusBadRequest, decodingError)
		return
	}

	if po.Drink == "" {
		localUUID := createGUID()
		emptyBodyError := ErrorModel{
			Message:    "You have to provide a body with this request",
			UniqueCode: localUUID}

		respondWithJSON(ctx, c, http.StatusBadRequest, emptyBodyError)
	}

	body, _ := json.Marshal(po)

	span.LogFields(
		openlog.String(method, c.Request.Method),
		openlog.String(path, c.Request.URL.Path),
		openlog.String(spanBody, string(body)),
		openlog.String(host, c.Request.Host),
	)

	user := c.Param("user")
	playlist := c.Param("playList")

	if strings.ToLower(user) == "global" {
		localUUID := createGUID()
		restrictedUserError := ErrorModel{
			Message:    "Global is a restricted user and cannot be used",
			UniqueCode: localUUID}

		respondWithJSON(ctx, c, http.StatusBadRequest, restrictedUserError)
	}

	CreateNewHighScore(ctx, user, playlist, po.Drink)

	c.Writer.WriteHeader(http.StatusCreated)
	span.Finish()
}

// respondWithJSON returns formed JSON
func respondWithJSON(ctx context.Context, c *gin.Context, code int, payload interface{}) {
	span, _ := opentracing.StartSpanFromContext(ctx, "Response")
	span.SetTag(method, "ResponseWriter")

	response, _ := json.Marshal(payload)
	c.Writer.Header().Set("Content-Type", "application/json")
	c.Writer.WriteHeader(code)
	c.JSON(code, payload)
	span.LogFields(
		openlog.String(statusCode, strconv.Itoa(code)),
		openlog.String(spanBody, string(response)),
	)
	defer span.Finish()
}
