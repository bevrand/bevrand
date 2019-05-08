package recommendation

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

const method = "Method"
const statusCode = "httpStatusCode"
const spanBody = "Body"

// Create guids
func createGUID() string {
	b, _ := uuid.NewRandom()
	uuid := fmt.Sprintf("%x-%x-%x-%x-%x",
		b[0:4], b[4:6], b[6:8], b[8:10], b[10:])

	return uuid
}

// can be used to send an error response
func RespondWithAnError(status int, errorMessage string, w http.ResponseWriter, ctx context.Context) {
	localUUID := createGUID()
	error := ErrorModel{
		Message:    errorMessage,
		UniqueCode: localUUID}
	respondWithJSON(ctx, w, status, error)
}

// respondWithJSON returns formed JSON
func respondWithJSON(ctx context.Context, w http.ResponseWriter, code int, payload interface{}) {
	span, _ := opentracing.StartSpanFromContext(ctx, "Response")
	span.SetTag(method, "ResponseWriter")

	response, _ := json.Marshal(payload)
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(code)

	_ = json.NewEncoder(w).Encode(payload)

	span.LogFields(
		openlog.String(statusCode, strconv.Itoa(code)),
		openlog.String(spanBody, string(response)),
	)
	defer span.Finish()
}
