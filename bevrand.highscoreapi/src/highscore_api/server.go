package main

import (
	"fmt"
	"github.com/mediocregopher/radix.v2/redis"
	"github.com/opentracing/opentracing-go"
	"github.com/uber/jaeger-client-go"
	"github.com/uber/jaeger-client-go/config"
	"io"
	"log"
	"highscore_api/routes"
)

// @title Swagger Example API
// @version 1.0
// @description This is a sample server Petstore server.
// @termsOfService http://swagger.io/terms/

// @contact.name API Support
// @contact.url http://www.swagger.io/support
// @contact.email support@swagger.io

// @license.name Apache 2.0
// @license.url http://www.apache.org/licenses/LICENSE-2.0.html

// @host petstore.swagger.io
// @BasePath /v2

func main() {
	SeedSomeData()
	//init jaeger
	tracer, closer := initJaeger("HighScoreApi")
	defer closer.Close()
	opentracing.SetGlobalTracer(tracer)


	//init router
	r := routes.InitRoutes()
	r.Run(":3000")
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

func SeedSomeData() {
	conn, err := redis.Dial("tcp", "localhost:6379")
	if err != nil {
		log.Fatal(err)
	}

	defer conn.Close()

	err = conn.Cmd("HMSET", "frontpage:tgif", "wine", 2, "beer", 1, "coke", 1, "whiskey", 24).Err
	if err != nil {
		log.Fatal(err)
	}
	err = conn.Cmd("HMSET", "frontpage:tgiff", "wine", 2, "beer", 1, "coke", 1, "whiskey", 24).Err
	if err != nil {
		log.Fatal(err)
	}

	title, err := conn.Cmd("HGETALL", "frontpage:tgif").Map()
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("tgif added")
	fmt.Println(title)

	err = conn.Cmd("MULTI").Err
	if err != nil {
		log.Fatal(err)
	}

	err = conn.Cmd("HINCRBY", "frontpage:tgif", "wine", 1).Err
	if err != nil {
		log.Fatal(err)
	}

	// Execute both commands in our transaction together as an atomic group.
	// EXEC returns the replies from both commands as an array reply but,
	// because we're not interested in either reply in this example, it
	// suffices to simply check the reply's Err field for any errors.
	err = conn.Cmd("EXEC").Err
	if err != nil {
		log.Fatal(err)

	}

	new_title, err := conn.Cmd("HGETALL", "frontpage:tgif").Map()
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(new_title)

	return
}
