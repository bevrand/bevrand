package main

import (
	"fmt"
	"github.com/bevrand/bevrand/bevrand.highscoreapi/routes"
	"github.com/joho/godotenv"
	"github.com/opentracing/opentracing-go"
	"github.com/uber/jaeger-client-go"
	"github.com/uber/jaeger-client-go/config"
	"io"
	"log"
	"os"
)

func main() {
	GetEnvFile()
	//init jaeger
	tracer, closer := initJaeger("HighScoreApi")
	defer closer.Close()
	opentracing.SetGlobalTracer(tracer)

	//init router
	r := routes.InitRoutes()
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
// initJaeger returns an instance of Jaeger Tracer that samples 100% of traces and logs all spans to stdout.
func initJaeger(service string) (opentracing.Tracer, io.Closer) {
	cfg := &config.Configuration{
		Sampler: &config.SamplerConfig{
			Type:  "const",
			Param: 1,
		},
		Reporter: &config.ReporterConfig{
			LogSpans: true,
		},
	}
	tracer, closer, err := cfg.New(service, config.Logger(jaeger.StdLogger))
	if err != nil {
		panic(fmt.Sprintf("ERROR: cannot init Jaeger: %v\n", err))
	}
	return tracer, closer
}

