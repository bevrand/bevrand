package recommendation

import (
	"net/http"
)

// InitRoutes to start up a mux router and return the routes
func InitRoutes() *http.ServeMux {
	serveMux := http.NewServeMux()

	//pingpong
	serveMux.HandleFunc("/ping", PingPong)

	serveMux.HandleFunc("/api/v1/categories", CategorieHandler)
	serveMux.HandleFunc("/api/v1/cocktails", CocktailHandler)
	serveMux.HandleFunc("/api/v1/beverages", BeverageHandler)
	serveMux.HandleFunc("/api/v1/beveragegroups/", BeverageGroupHandler)

	return serveMux
}
