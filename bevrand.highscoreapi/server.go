package main

import (
	"bevrand.highscoreapi/jaeger"
	"context"
	"flag"
	"fmt"
	"github.com/joho/godotenv"
	"github.com/mediocregopher/radix.v2/pool"
	"github.com/opentracing/opentracing-go"
	"github.com/streadway/amqp"
	"log"
	"os"
	"time"
)

var db *pool.Pool
var amqpUri = flag.String("r", "amqp://rabbitmq:rabbitmq@localhost:5672/", "If rabbit url is not set")

var (
	rabbitConn       *amqp.Connection
	rabbitCloseError chan *amqp.Error
)

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

// Connect to rabbitmq with a retry
func connectToRabbitMQ(rabbitUrl string) *amqp.Connection {
	for {
		conn, err := amqp.Dial(rabbitUrl)

		if err == nil {
			return conn
		}

		time.Sleep(500 * time.Millisecond)
	}
}

// re-establish the connection to RabbitMQ in case
// the connection has died
//
func rabbitConnector(uri string) {
	var rabbitErr *amqp.Error

	for {
		rabbitErr = <-rabbitCloseError
		if rabbitErr != nil {
			rabbitUrl := os.Getenv("RABBIT_URL")
			if rabbitUrl == "" {
				rabbitUrl = uri
			}

			rabbitConn = connectToRabbitMQ(rabbitUrl)
			// start reading Queue
			go ReadQueue()
			rabbitCloseError = make(chan *amqp.Error)
			rabbitConn.NotifyClose(rabbitCloseError)
		}
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

	tracer, closer := jaeger.InitJaeger("HighScoreApi", jaegerConfig)
	defer closer.Close()
	opentracing.SetGlobalTracer(tracer)

	span := tracer.StartSpan("StartingServer")
	span.SetTag("event", "Starting GINGONIC")
	defer span.Finish()

	ctx := context.Background()
	ctx = opentracing.ContextWithSpan(ctx, span)

	logValue := fmt.Sprintf("Starting server for HighScores!")
	jaeger.PrintServerInfo(ctx, logValue)
	span.Finish()

	flag.Parse()

	// create the rabbitmq error channel
	rabbitCloseError = make(chan *amqp.Error)

	// goroutine to connect to rabbit
	go rabbitConnector(*amqpUri)

	// establish the rabbitmq connection by sending
	// an error and thus calling the error callback
	rabbitCloseError <- amqp.ErrClosed

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
		log.Panic(err)
	}
}

