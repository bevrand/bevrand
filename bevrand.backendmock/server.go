package main

import (
	"./handlers"
	"github.com/rs/cors"
	"github.com/urfave/negroni"
)

func main() {
	router := handlers.NewRouter()
	handler := cors.Default().Handler(router)
	n := negroni.Classic()
	n.UseHandler(handler)
	n.Run(":4540")
}
