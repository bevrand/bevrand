package jaeger

import (
	"context"
	"github.com/opentracing/opentracing-go"
	"github.com/uber/jaeger-client-go"
	"github.com/uber/jaeger-client-go/config"
	"io"
)

// InitJaeger returns a new tracer
func InitJaeger(service string, cfg *config.Configuration) (opentracing.Tracer, io.Closer, error) {
	tracer, closer, err := cfg.New(service, config.Logger(jaeger.StdLogger))
	return tracer, closer, err
}

// PrintServerInfo logs a span to jaeger that gives basic information about this service at startup
func PrintServerInfo(ctx context.Context, serverInfo string) {
	span, _ := opentracing.StartSpanFromContext(ctx, "ServerInfo")
	defer span.Finish()

	span.LogKV("event", serverInfo)
}
