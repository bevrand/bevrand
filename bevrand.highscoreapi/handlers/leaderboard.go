package handlers

import (
	"context"
	"encoding/json"
	"fmt"
	"github.com/gin-gonic/gin"
	"github.com/mediocregopher/radix.v2/pool"
	"github.com/opentracing/opentracing-go"
	openlog "github.com/opentracing/opentracing-go/log"
	"highscore_api/models"
	"log"
	"os"
	"strconv"
)

var db *pool.Pool

func init() {
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


func ShowHighScores(user string, playlist string, c *gin.Context, ctx context.Context) ([]models.Score) {
	span, _ := opentracing.StartSpanFromContext(ctx, "ShowHighScores")
	span.SetTag("Method", "ShowHighScores")
	defer span.Finish()
	key := user + ":" + playlist

	res, err := db.Cmd("EXISTS", key).Int()
	if err != nil {
		log.Fatal(err)
	}
	exists := res != 0

	//todo: add this to middleware
	if !exists {
		span.LogFields(
			openlog.String("http_status_code", "404"),
			openlog.String("body", "not found"),
		)
		span.Finish()
		c.JSON(404, gin.H{
			"error": "pong",
		})
		return nil
	}

	result, err := db.Cmd("HGETALL", key).Map()
	if err != nil {
		log.Fatal(err)
	}
	var redisResult []models.Score
	for drink, score := range result{
		i, err := strconv.Atoi(score)
		if err != nil {
			log.Fatal("cannot convert string to int")
		}
		 newScore := models.Score{
			Drink: drink,
			Rolled: i}
		redisResult = append(redisResult, newScore)
	}
	body, _ := json.Marshal(redisResult)

	span.LogFields(
		openlog.String("http_status_code", "200"),
		openlog.String("body", string(body)),
	)

	return redisResult
}

func CreateNewHighScore(user string, playlist string, drink string, ctx context.Context) {
	span, _ := opentracing.StartSpanFromContext(ctx, "CreateNewHighScore")
	span.SetTag("Method", "ShowHighScores")

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
	return
}