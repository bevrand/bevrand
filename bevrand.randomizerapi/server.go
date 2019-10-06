package main

import (
	"context"
	"flag"
	"fmt"
	"github.com/opentracing/opentracing-go"
	"github.com/streadway/amqp"
	"github.com/uber/jaeger-client-go"
	"github.com/uber/jaeger-client-go/config"
	"github.com/urfave/negroni"
	"io"
	"log"
	"os"
	"time"
)

var amqpUri = flag.String("r", "amqp://rabbitmq:rabbitmq@localhost:5672/", "If rabbit url is not set")

var (
	rabbitConn       *amqp.Connection
	rabbitCloseError chan *amqp.Error
)

// Connect to rabbitmq with a retry
func connectToRabbitMQ(uri string) *amqp.Connection {
	for {
		rabbitUrl := os.Getenv("RABBIT_URL")
		if rabbitUrl == "" {
			rabbitUrl = uri
		}
		conn, err := amqp.Dial(rabbitUrl)

		if err == nil {
			return conn
		}

		log.Println(err)
		log.Printf("Trying to reconnect to RabbitMQ at %s\n", rabbitUrl)
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
			log.Printf("Connecting to %s\n", *amqpUri)

			rabbitConn = connectToRabbitMQ(uri)
			rabbitCloseError = make(chan *amqp.Error)
			rabbitConn.NotifyClose(rabbitCloseError)
		}
	}
}

func main() {
	jaegerURL := os.Getenv("JAEGER_AGENT_HOST")
	jaegerPort := os.Getenv("JAEGER_AGENT_PORT")
	jaegerConfig := jaegerURL + ":" + jaegerPort
	println(jaegerConfig)

	cfg := &config.Configuration{
		Sampler: &config.SamplerConfig{
			Type:  "const",
			Param: 1,
		},
		Reporter: &config.ReporterConfig{
			LogSpans:           true,
			LocalAgentHostPort: jaegerConfig,
		},
	}

	tracer, closer, err := initJaeger("RandomizerApi", cfg)
	if err != nil {
		panic(fmt.Sprintf("ERROR: cannot init Jaeger: %v\n", err))
	}
	defer closer.Close()
	opentracing.SetGlobalTracer(tracer)

	span := tracer.StartSpan("StartingServer")
	span.SetTag("event", "Starting MUX")
	defer span.Finish()

	ctx := context.Background()
	ctx = opentracing.ContextWithSpan(ctx, span)

	logValue := fmt.Sprintf("Starting server on port 5000")
	printServerInfo(ctx, logValue)
	span.Finish()

	flag.Parse()

	// create the rabbitmq error channel
	rabbitCloseError = make(chan *amqp.Error)

	// goroutine to connect to rabbit
	go rabbitConnector(*amqpUri)

	// establish the rabbitmq connection by sending
	// an error and thus calling the error callback
	rabbitCloseError <- amqp.ErrClosed

	serveMux := InitRoutes()

	n := negroni.Classic()
	n.UseHandler(serveMux)
	n.Run(":5000")
}

// InitJaeger returns a new tracer
func initJaeger(service string, cfg *config.Configuration) (opentracing.Tracer, io.Closer, error) {
	tracer, closer, err := cfg.New(service, config.Logger(jaeger.StdLogger))
	return tracer, closer, err
}

// PrintServerInfo logs a span to jaeger that gives basic information about this service at startup
func printServerInfo(ctx context.Context, serverInfo string) {
	span, _ := opentracing.StartSpanFromContext(ctx, "ServerInfo")
	defer span.Finish()

	span.LogKV("event", serverInfo)
}
