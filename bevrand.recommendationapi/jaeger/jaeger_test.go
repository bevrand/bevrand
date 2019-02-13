package jaeger

import (
	"context"
	"github.com/opentracing/opentracing-go"
	"github.com/stretchr/testify/assert"
	"github.com/uber/jaeger-client-go"
	"github.com/uber/jaeger-client-go/config"
	"testing"
)

func TestInitJaeger(t *testing.T) {
	jaegerConfig := "localhost:4580"

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
	expectedName := "testjaeger"
	tracer, closer, err := InitJaeger(expectedName, cfg)

	assert.NoError(t, err)
	defer closer.Close()

	if tracer == nil {
		t.Errorf("tracer not returned")
	}

	assert.Equal(t, "const", cfg.Sampler.Type)
	assert.Equal(t, jaegerConfig, cfg.Reporter.LocalAgentHostPort)
}

func TestPrintServerInfo(t *testing.T) {
	c := &config.Configuration{
		Sampler: &config.SamplerConfig{
			Type:  "const",
			Param: 1,
		},
	}
	r := jaeger.NewInMemoryReporter()
	tracer, closer, err := c.New("test", config.Reporter(r))
	opentracing.SetGlobalTracer(tracer)
	assert.NoError(t, err)
	defer closer.Close()

	ctx := context.Background()
	logValue := "This is some test"
	PrintServerInfo(ctx, logValue)

	assert.Len(t, r.GetSpans(), 1)
}
