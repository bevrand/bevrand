package main

import (
	"context"
	"encoding/json"
	"fmt"
	"github.com/opentracing/opentracing-go"
	openlog "github.com/opentracing/opentracing-go/log"
	"gopkg.in/oauth2.v3/utils/uuid"
	"net/http"
	"strconv"
)

// key used when setting and getting requests from context
const ContextKey  = "randomizeRequest"

// middleware to validate proper methods
func ValidateRestMethod(method string) Adapter {

	return func(f http.HandlerFunc) http.HandlerFunc {

		return func(w http.ResponseWriter, r *http.Request) {
			tracer := opentracing.GlobalTracer()
			span := tracer.StartSpan("ValidateRestMethod")
			span.SetTag("Method", "Validation")
			span.LogFields(
				openlog.String("method", r.Method),
				openlog.String("path", r.URL.Path),
				openlog.String("host", r.Host),
			)
			ctx := context.Background()
			ctx = opentracing.ContextWithSpan(ctx, span)

			if r.Method != method {
				var err MethodError
				e := MethodMessages{method, "Method " + r.Method + " not allowed at this endpoint"}
				err = MethodError{ErrorModel{CreateGUID()}, append(err.Messages, e)}
				ResponseWithJson(ctx, w, err)
				return
			}
			f(w, r)
		}
	}
}

// middleware to validate valid payload
func ValidatePayload() Adapter {

	return func(f http.HandlerFunc) http.HandlerFunc {

		return func(w http.ResponseWriter, r *http.Request) {
			tracer := opentracing.GlobalTracer()
			span := tracer.StartSpan("ValidateRestMethod")
			span.SetTag("Method", "Validation")
			ctxRequest := r.Context()
			ctx := context.Background()
			ctx = opentracing.ContextWithSpan(ctx, span)

			decoder := json.NewDecoder(r.Body)
			var randomizeRequest RandomizeRequest

			err := decoder.Decode(&randomizeRequest)
			if err != nil {
				ResponseWithJson(ctx, w, err)
				return
			}

			ctxRequest = context.WithValue(r.Context(), ContextKey, randomizeRequest)

			valid, err := ValidateRequest(randomizeRequest)
			if err != nil {
				ResponseWithJson(ctx, w, valid)
				return
			}
		f(w, r.WithContext(ctxRequest))
		}
	}
}

// ResponseWithJson returns formed JSON
func ResponseWithJson(ctx context.Context, w http.ResponseWriter, payload interface{}) {
	span, _ := opentracing.StartSpanFromContext(ctx, "Response")
	span.SetTag("Method", "ResponseWriter")

	code := 500

	switch payload.(type) {
	case ResultModel:
		code = 200
	case ValidationError:
		code = 400
	case MethodError:
		code = 405
	default:
		code = 500
	}

	response, _ := json.Marshal(payload)
	resp := string(response)
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(code)
	w.Write([]byte(resp))
	span.LogFields(
		openlog.String("StatusCode", strconv.Itoa(code)),
		openlog.String("Body", resp),
	)
	defer span.Finish()
}

// creates a Guid for error tracing
func CreateGUID() string {
	b, _ := uuid.NewRandom()
	uuid := fmt.Sprintf("%x-%x-%x-%x-%x",
		b[0:4], b[4:6], b[6:8], b[8:10], b[10:])

	return uuid
}
