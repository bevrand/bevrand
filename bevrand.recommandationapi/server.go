package main

import (
	"bevrand.recommandationapi/handlers"
	"bevrand.recommandationapi/services/jaeger"
	"context"
	"fmt"
	"github.com/joho/godotenv"
	"github.com/opentracing/opentracing-go"
	"log"
	"net/http"
	"os"
)

func init() {
	env := os.Getenv("GO_ENV")
	println(env)

	err := godotenv.Load(".env." + env)
	if err != nil {
		log.Fatal("Error loading .env file")
	}

	if os.Getenv("NEO4J_URL") != "" {
		handlers.Neo4jURL = os.Getenv("NEO4J_URL")
	}
}


func main() {
	jaegerUrl := os.Getenv("JAEGER_AGENT_HOST")
	jaegerPort :=  os.Getenv("JAEGER_AGENT_PORT")
	jaegerConfig := jaegerUrl + ":" + jaegerPort
	println(jaegerConfig)

	tracer, closer := jaeger.InitJaeger("RecommendationApi", jaegerConfig)
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

	logValue := fmt.Sprintf("Starting server on port %s with neo4j %s", port, handlers.Neo4jURL)
	jaeger.PrintServerInfo(ctx, logValue)
	span.Finish()


	serveMux := http.NewServeMux()
	serveMux.HandleFunc("api/v1/search", handlers.SearchHandler)
	serveMux.HandleFunc("api/v1/movie/", handlers.MovieHandler)
	serveMux.HandleFunc("api/v1/graph", handlers.GraphHandler)

	panic(http.ListenAndServe(":"+port, serveMux))

}


