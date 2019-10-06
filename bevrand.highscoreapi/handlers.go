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
	"sort"
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
		respondWithJSON(ctx, c, http.StatusNotFound, notFoundError)
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

	sort.Slice(redisResult, func(i, j int) bool {
		return redisResult[i].Rolled > redisResult[j].Rolled
	})

	return redisResult, http.StatusOK
}

// CreateNewHighScore creates a new highscore for a user and playlist combination
func CreateNewHighScore(user string, playlist string, drink string) {
	key := user + ":" + playlist

	exists := keyExistsInRedis(key)

	if !exists {
		err := db.Cmd(keySet, key, drink, 1).Err
		if err != nil {
			log.Fatal(err)
		}
		IncreaseGlobalCount(drink)
		return
	}

	err := db.Cmd(keyIncrease, key, drink, 1).Err
	if err != nil {
		log.Fatal(err)
	}

	go IncreaseGlobalCount(drink)
	return
}

// IncreaseGlobalCount global should be increased with every normal increase
func IncreaseGlobalCount(drink string) {
	key := GLOBALNAME + ":" + GLOBALLIST

	exists := keyExistsInRedis(key)

	if !exists {
		err := db.Cmd(keySet, key, drink, 1).Err
		if err != nil {
			log.Fatal(err)
		}
		return
	}

	err := db.Cmd(keyIncrease, key, drink, 1).Err
	if err != nil {
		log.Fatal(err)
	}
	return
}

func ReadQueue() {
	ch, _ := rabbitConn.Channel()

	q, _ := ch.QueueDeclare(
		"highscores", // name
		false,   // durable
		false,   // delete when unused
		false,   // exclusive
		false,   // no-wait
		nil,     // arguments
	)

	msgs, _ := ch.Consume(
		q.Name, // queue
		"",     // consumer
		true,   // auto-ack
		false,  // exclusive
		false,  // no-local
		false,  // no-wait
		nil,    // args
	)

	forever := make(chan bool)

	go func() {
		for msg := range msgs {
			var highscore HighScoreObject
			err := json.Unmarshal(msg.Body, &highscore)
			if err != nil {
				print(err)
			}
			go CreateNewHighScore(highscore.Username, highscore.Playlist, highscore.Result)
		}
	}()

	<-forever
}

func createGUID() string {
	b, _ := uuid.NewRandom()
	uuid := fmt.Sprintf("%x-%x-%x-%x-%x",
		b[0:4], b[4:6], b[6:8], b[8:10], b[10:])

	return uuid
}

func keyExistsInRedis(key string) bool {
	res, err := db.Cmd(keyExists, key).Int()
	if err != nil {
		log.Fatal(err)
	}
	exists := res != 0
	return exists
}
