package main

import (
	"bevrand.recommendationapi/jaeger"
	"context"
	"fmt"
	bolt "github.com/johnnadratowski/golang-neo4j-bolt-driver"
	"github.com/joho/godotenv"
	"github.com/opentracing/opentracing-go"
	"github.com/uber/jaeger-client-go/config"
	"github.com/urfave/negroni"
	"os"
)

var db bolt.Conn

func main() {
	getEnvFile()
	createConnection()

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

	tracer, closer, err := jaeger.InitJaeger("RecommendationApi", cfg)
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

	logValue := fmt.Sprintf("Starting server on port with neo4j")
	jaeger.PrintServerInfo(ctx, logValue)
	span.Finish()

	serveMux := InitRoutes()

	n := negroni.Classic()
	n.UseHandler(serveMux)
	n.Run(":5000")
}

// GetEnvFile sets env files entries to environment
func getEnvFile() {
	env := os.Getenv("GO_ENV")
	if "" == env {
		env = "development"
	}

	err := godotenv.Load(".env." + env)
	handleError(err)
}

func createConnection() {
	var err error
	neo4jUrl := os.Getenv("NEO4J_URL")
	driver, err := bolt.NewDriverPool(neo4jUrl, 10)
	db, err = driver.OpenPool()
	handleError(err)
}

// simple function to handle errors
// should be rewritten to throw 502
func handleError(err error) {
	if err != nil {
		panic(err)
	}
}
