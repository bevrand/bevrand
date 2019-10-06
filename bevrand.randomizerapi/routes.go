package main

import (
	"net/http"
)

type Adapter func(http.HandlerFunc) http.HandlerFunc

// InitRoutes to start up a mux router and return the routes
func InitRoutes() *http.ServeMux {
	serveMux := http.NewServeMux()

	//pingpong
	serveMux.HandleFunc("/ping", Adapt(PingPong, ValidateRestMethod("GET")))
	serveMux.HandleFunc("/api/ping", Adapt(PingPong, ValidateRestMethod("GET")))

	//randomizer
	serveMux.HandleFunc("/api/v1/randomize", Adapt(RandomizeHandler, ValidatePayload(), ValidateRestMethod("POST")))
	serveMux.HandleFunc("/api/randomize", Adapt(RandomizeHandler, ValidatePayload(), ValidateRestMethod("POST")))

	return serveMux
}

// PingPong pongs the ping
func PingPong(w http.ResponseWriter, req *http.Request) {
	w.WriteHeader(200)
	w.Write([]byte("pong"))
}

// Iterate over adapters and run them one by one
func Adapt(h http.HandlerFunc, adapters ...Adapter) http.HandlerFunc {
	for _, adapter := range adapters {
		h = adapter(h)
	}
	return h
}
