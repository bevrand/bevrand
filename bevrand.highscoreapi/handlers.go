package main

import (
	"context"
	"encoding/json"
	"fmt"
	"github.com/gin-gonic/gin"
	"github.com/opentracing/opentracing-go"
	openlog "github.com/opentracing/opentracing-go/log"
	"gopkg.in/oauth2.v3/utils/uuid"
	"log"
	"net/http"
	"strconv"
)

// PingPong return a pong
func PingPong(c *gin.Context) {
	c.JSON(200, gin.H{
		"message": "pong",
	})
}

// ShowHighScores returns a specific user and playlist highscore
func ShowHighScores(ctx context.Context, user string, playlist string, c *gin.Context) ([]Score, int) {
	span, _ := opentracing.StartSpanFromContext(ctx, "ShowHighScores")
	span.SetTag(method, "ShowHighScores")
	defer span.Finish()
	key := user + ":" + playlist

	res, err := db.Cmd(keyExists, key).Int()
	if err != nil {
		log.Fatal(err)
	}
	exists := res != 0
	var redisResult []Score

	if !exists {
		span.LogFields(
			openlog.String(statusCode, "404"),
			openlog.String(spanBody, "not found"),
		)
		span.Finish()
		localUUID := createGUID()
		notFoundError := ErrorModel{
			Message:    "Could not find combination of user: " + user + " & list: " + playlist,
			UniqueCode: localUUID}
		respondWithJSON(c, http.StatusNotFound, notFoundError, ctx)
		return nil, 0
	}

	result, err := db.Cmd("HGETALL", key).Map()
	if err != nil {
		log.Fatal(err)
	}
	for drink, score := range result {
		i, err := strconv.Atoi(score)
		if err != nil {
			log.Fatal("cannot convert string to int")
		}
		newScore := Score{
			Drink:  drink,
			Rolled: i}
		redisResult = append(redisResult, newScore)
	}
	body, _ := json.Marshal(redisResult)

	span.LogFields(
		openlog.String(statusCode, "200"),
		openlog.String(spanBody, string(body)),
	)
	return redisResult, http.StatusOK
}

// CreateNewHighScore creates a new highscore for a user and playlist combination
func CreateNewHighScore(ctx context.Context, user string, playlist string, drink string) {
	span, _ := opentracing.StartSpanFromContext(ctx, "CreateNewHighScore")
	span.SetTag(method, "IncreaseHighScore")

	defer span.Finish()
	key := user + ":" + playlist

	res, err := db.Cmd(keyExists, key).Int()
	if err != nil {
		log.Fatal(err)
	}
	exists := res != 0

	if !exists {
		span.LogFields(
			openlog.String(statusCode, "200"),
			openlog.String(spanBody, "New entry, setting new key: "+key),
		)
		err = db.Cmd(keySet, key, drink, 1).Err
		if err != nil {
			log.Fatal(err)
		}
		return
	}

	err = db.Cmd(keyIncrease, key, drink, 1).Err
	if err != nil {
		log.Fatal(err)
	}
	span.LogFields(
		openlog.String(statusCode, "200"),
		openlog.String(spanBody, "Increased "+drink+" by 1"),
	)

	IncreaseGlobalCount(ctx, drink)
	return
}

// IncreaseGlobalCount global should be increased with every normal increase
func IncreaseGlobalCount(ctx context.Context, drink string) {
	span, _ := opentracing.StartSpanFromContext(ctx, "IncreaseGlobalCount")
	span.SetTag(method, "GlobalHighscore")

	defer span.Finish()
	key := GLOBALNAME + ":" + GLOBALLIST

	res, err := db.Cmd(keyExists, key).Int()
	if err != nil {
		log.Fatal(err)
	}
	exists := res != 0

	if !exists {
		span.LogFields(
			openlog.String(statusCode, "200"),
			openlog.String(spanBody, "New entry, setting new key: "+key),
		)
		err = db.Cmd(keySet, key, drink, 1).Err
		if err != nil {
			log.Fatal(err)
		}
		return
	}

	err = db.Cmd(keyIncrease, key, drink, 1).Err
	if err != nil {
		log.Fatal(err)
	}
	span.LogFields(
		openlog.String(statusCode, "200"),
		openlog.String(spanBody, "Increased "+drink+" by 1"),
	)
	return
}

func createGUID() string {
	b, _ := uuid.NewRandom()
	uuid := fmt.Sprintf("%x-%x-%x-%x-%x",
		b[0:4], b[4:6], b[6:8], b[8:10], b[10:])

	return uuid
}
