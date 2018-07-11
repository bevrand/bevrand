package handlers

import "net/http"

type Route struct {
	Name        string
	Method      string
	Pattern     string
	HandlerFunc http.HandlerFunc
}

type Routes []Route

var routes = Routes{
	Route{
		"Index",
		"GET",
		"/",
		Index,
	},
	Route{
		"RedisTopFive",
		"GET",
		"/api/redis",
		RedisTopFive,
	},
	Route{
		"RandomizeDrink",
		"POST",
		"/api/randomize",
		RandomizeDrink,
	},
	Route{
		"AllPlayLists",
		"GET",
		"/api/frontpage",
		AllPlayLists,
	},
}
