package main

import (
	"context"
	"fmt"
	"github.com/joho/godotenv"
	"github.com/mediocregopher/radix.v2/pool"
	"github.com/opentracing/opentracing-go"
	"log"
	"os"
)

var db *pool.Pool
// GLOBALNAME is the user name for the global count
var GLOBALNAME = "global"
// GLOBALLIST is the playlist name for the global count
var GLOBALLIST = "globalhighscore"

const method = "Method"
const path = "Path"
const host = "Host"
const statusCode = "httpStatusCode"
const spanBody = "Body"

const keyExists = "EXISTS"
const keySet = "HMSET"
const keyIncrease = "HINCRBY"

// ConnectRedis creates a connection to Redis
func ConnectRedis() {
	var err error
	// Establish a pool of 10 connections to the Redis server listening on
	// port 6379 of the variable that has been used
	redisURL := os.Getenv("REDIS_URL") + ":6379"
	fmt.Println(redisURL)
	db, err = pool.New("tcp", redisURL, 10)
	if err != nil {
		log.Panic(err)
	}
}

func main() {
	GetEnvFile()
	ConnectRedis()
	//init jaeger
	jaegerURL := os.Getenv("JAEGER_AGENT_HOST")
	jaegerPort := os.Getenv("JAEGER_AGENT_PORT")
	jaegerConfig := jaegerURL + ":" + jaegerPort
	println(jaegerConfig)

	tracer, closer := InitJaeger("HighScoreApi", jaegerConfig)
	defer closer.Close()
	opentracing.SetGlobalTracer(tracer)

	span := tracer.StartSpan("StartingServer")
	span.SetTag("event", "Starting GINGONIC")
	defer span.Finish()

	ctx := context.Background()
	ctx = opentracing.ContextWithSpan(ctx, span)

	logValue := fmt.Sprintf("Starting server for HighScores!")
	PrintServerInfo(ctx, logValue)
	span.Finish()

	//init router
	r := InitRoutes()
	r.Run(":5000")
}

// GetEnvFile sets env files entries to environment
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
