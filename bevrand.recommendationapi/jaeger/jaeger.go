package jaeger

import (
	"context"
	"github.com/opentracing/opentracing-go"
	openlog "github.com/opentracing/opentracing-go/log"
	"github.com/uber/jaeger-client-go"
	"github.com/uber/jaeger-client-go/config"
	"io"
	"net/http"
)

const method = "method"
const path = "path"
const host = "host"

// InitJaeger returns a new tracer
func InitJaeger(service string, cfg *config.Configuration) (opentracing.Tracer, io.Closer, error) {
	tracer, closer, err := cfg.New(service, config.Logger(jaeger.StdLogger))
	return tracer, closer, err
}

// You can send your startup method here so it gets logged
func TraceHandler(req *http.Request, methodName string, operationName string) context.Context {
	tracer := opentracing.GlobalTracer()
	span := tracer.StartSpan(operationName)
	span.SetTag(method, methodName)
	span.LogFields(
		openlog.String(method, req.Method),
		openlog.String(path, req.URL.Path),
		openlog.String(host, req.Host),
	)
	ctx := context.Background()
	ctx = opentracing.ContextWithSpan(ctx, span)
	defer span.Finish()

	return ctx
}

// PrintServerInfo logs a span to jaeger that gives basic information about this service at startup
func PrintServerInfo(ctx context.Context, serverInfo string) {
	span, _ := opentracing.StartSpanFromContext(ctx, "ServerInfo")
	defer span.Finish()

	span.LogKV("event", serverInfo)
}
