package bevrand_highscoreapi

import (
	"fmt"
	"github.com/joho/godotenv"
	"github.com/opentracing/opentracing-go"
	"github.com/uber/jaeger-client-go"
	"github.com/uber/jaeger-client-go/config"
	"github.com/bevrand/bevrand/bevrand.highscoreapi/routes"
	"io"
	"log"
	"os"
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

	err := godotenv.Load("./src/highscore_api/.env." + env)
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

