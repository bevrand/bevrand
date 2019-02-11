package main

import (
	"bevrand.recommandationapi/jaeger"
	"context"
	"fmt"
	"github.com/joho/godotenv"
	"github.com/opentracing/opentracing-go"
	"github.com/uber/jaeger-client-go/config"
	"github.com/urfave/negroni"
	"log"
	"os"
)

var (
	// Neo4jURL is the connection string for neo4j
	Neo4jURL = "bolt://localhost:7687"
)

func init() {
	env := os.Getenv("GO_ENV")
	println(env)

	err := godotenv.Load(".env." + env)
	if err != nil {
		log.Fatal("Error loading .env file")
	}

	if os.Getenv("NEO4J_URL") != "" {
		Neo4jURL = os.Getenv("NEO4J_URL")
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

	tracer, closer, err := jaeger.InitJaeger("RecommendationApi", cfg)
	if err != nil {
		panic(fmt.Sprintf("ERROR: cannot init Jaeger: %v\n", err))
	}
	defer closer.Close()
	opentracing.SetGlobalTracer(tracer)

	port := os.Getenv("PORT")
	if port == "" {
		port = "3220"
	}

	span := tracer.StartSpan("StartingServer")
	span.SetTag("event", "Starting MUX")
	defer span.Finish()

	ctx := context.Background()
	ctx = opentracing.ContextWithSpan(ctx, span)

	logValue := fmt.Sprintf("Starting server on port %s with neo4j %s", port, Neo4jURL)
	jaeger.PrintServerInfo(ctx, logValue)
	span.Finish()

	serveMux := InitRoutes()

	n := negroni.Classic()
	n.UseHandler(serveMux)
	n.Run(":5000")
}
