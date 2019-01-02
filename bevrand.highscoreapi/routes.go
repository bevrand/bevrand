package main

import (
	"context"
	"encoding/json"
	"fmt"
	"github.com/gin-gonic/gin"
	"github.com/opentracing/opentracing-go"
	"github.com/opentracing/opentracing-go/ext"
	openlog "github.com/opentracing/opentracing-go/log"
	"gopkg.in/oauth2.v3/utils/uuid"
	"net/http"
	"strconv"
	"strings"
)


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

func RouteShowAllHighScore(c *gin.Context) {
	spanCtx, _ := opentracing.GlobalTracer().Extract(opentracing.HTTPHeaders, opentracing.HTTPHeadersCarrier(c.Request.Header))
	span := opentracing.GlobalTracer().StartSpan("ShowGlobalHighScore", ext.RPCServerOption(spanCtx))
	defer span.Finish()

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
	spanCtx, _ := opentracing.GlobalTracer().Extract(opentracing.HTTPHeaders, opentracing.HTTPHeadersCarrier(c.Request.Header))
	span := opentracing.GlobalTracer().StartSpan("ShowHighScore", ext.RPCServerOption(spanCtx))
	defer span.Finish()

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
	spanCtx, _ := opentracing.GlobalTracer().Extract(opentracing.HTTPHeaders, opentracing.HTTPHeadersCarrier(c.Request.Header))
	span := opentracing.GlobalTracer().StartSpan("IncrementHighScore", ext.RPCServerOption(spanCtx))
	defer span.Finish()

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

	if po.Drink == "" {
		b, _ := uuid.NewRandom()
		localUuid := fmt.Sprintf("%x-%x-%x-%x-%x",
			b[0:4], b[4:6], b[6:8], b[8:10], b[10:])
		emptyBodyError := ErrorModel{
			Message: "You have to provide a body with this request",
			UniqueCode: localUuid}

		respondWithJson(c, http.StatusBadRequest, emptyBodyError, ctx)
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

	if strings.ToLower(user) == "global" {
		b, _ := uuid.NewRandom()
		localUuid := fmt.Sprintf("%x-%x-%x-%x-%x",
			b[0:4], b[4:6], b[6:8], b[8:10], b[10:])
		restrictedUserError := ErrorModel{
			Message: "Global is a restricted user and cannot be used",
			UniqueCode: localUuid}

		respondWithJson(c, http.StatusBadRequest, restrictedUserError, ctx)
	}

	CreateNewHighScore(user, playlist, po.Drink, ctx)

	c.Writer.WriteHeader(http.StatusCreated)
	span.Finish()
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
