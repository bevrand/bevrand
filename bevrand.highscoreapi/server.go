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
var GLOBALNAME = "global"
var GLOBALLIST = "globalhighscore"

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