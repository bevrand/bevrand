package recommendation

import (
	"bevrand.recommendationapi/jaeger"
	"log"
	"net/http"
	"strconv"
	"strings"
)

const notFoundMessage = "No results found for query"

// PingPong pongs the ping
func PingPong(w http.ResponseWriter, req *http.Request) {
	ctx := jaeger.TraceHandler(req, "PingPong", "PingPongHandler")
	respondWithJSON(ctx, w, 200, "pong")
}

// CategorieHandler handles routes for categories of drinks takes a param named kind
func CategorieHandler(w http.ResponseWriter, req *http.Request) {
	ctx := jaeger.TraceHandler(req, "Categories", "CategorieHandler")

	v := req.URL.Query()
	kindQuery := v.Get("kind")

	if kindQuery == "" {
		kindQuery = "Beer"
	}

	cypher := `
	MATCH (drink:Beverage)-[:KIND_OF]->(group:BevGroup) WHERE group.name =~ {kindOf} return drink.name, drink.perc, drink.type, drink.country
	`

	data, _, _, err := db.QueryNeoAll(cypher, map[string]interface{}{"kindOf": "(?i)" + kindQuery})
	if err != nil {
		RespondWithAnError(502, err.Error(), w, ctx)
		return
	} else if len(data) == 0 {
		RespondWithAnError(404, notFoundMessage, w, ctx)
		return
	}

	results := make([]BeverageResult, len(data))
	for idx, row := range data {
		country := ""
		if row[3] != nil {
			country = row[3].(string)
		}
		results[idx] = BeverageResult{
			Beverage{
				Name:    row[0].(string),
				Perc:    int(row[1].(int64)),
				Type:    row[2].(string),
				Country: country,
			},
		}
	}

	respondWithJSON(ctx, w, 200, results)
}

// BeverageHandler handles routes for beverages only takes a limit for now
func BeverageHandler(w http.ResponseWriter, req *http.Request) {
	ctx := jaeger.TraceHandler(req, "Beverages", "BeverageHandler")

	v := req.URL.Query()

	limits := v.Get("limit")
	limit := 50
	var err error
	if len(limits) > 0 {
		limit, err = strconv.Atoi(limits)
		if err != nil {
			RespondWithAnError(400, "Limit must be an integer", w, ctx)
		}
	}

	cypher := `MATCH (n:Beverage) RETURN n.name, n.perc, n.type, n.country LIMIT {limit}`

	data, _, _, err := db.QueryNeoAll(cypher, map[string]interface{}{"limit": limit})
	if err != nil {
		RespondWithAnError(502, err.Error(), w, ctx)
		return
	} else if len(data) == 0 {
		RespondWithAnError(404, notFoundMessage, w, ctx)
		return
	}

	results := make([]BeverageResult, len(data))
	for idx, row := range data {
		country := ""
		if row[3] != nil {
			country = row[3].(string)
		}
		results[idx] = BeverageResult{
			Beverage{
				Name:    row[0].(string),
				Perc:    int(row[1].(int64)),
				Type:    row[2].(string),
				Country: country,
			},
		}
	}

	respondWithJSON(ctx, w, 200, results)
}

// BeverageGroupHandler handles routes for groups of drinks that have subsets of drinks
func BeverageGroupHandler(w http.ResponseWriter, req *http.Request) {
	ctx := jaeger.TraceHandler(req, "BeverageGroups", "BeverageGroupHandler")

	cypher := `
	MATCH (n:BevGroup) RETURN n.name
	`

	stmt, err := db.PrepareNeo(cypher)
	if err != nil {
		RespondWithAnError(502, err.Error(), w, ctx)
		return
	}
	defer stmt.Close()

	rows, err := stmt.QueryNeo(map[string]interface{}{})
	if err != nil {
		RespondWithAnError(502, err.Error(), w, ctx)
		return
	}

	results := D3BevGroupResponse{}
	row, _, err := rows.NextNeo()
	for row != nil && err == nil {
		title := row[0].(string)
		println(row)
		results.Nodes = append(results.Nodes, Node{Title: title, Label: "Group"})

		row, _, err = rows.NextNeo()
	}

	respondWithJSON(ctx, w, 200, results)
}

// CocktailHandler handles routes for cocktails ingredients can be in and excluded
func CocktailHandler(w http.ResponseWriter, req *http.Request) {
	ctx := jaeger.TraceHandler(req, "Cocktails", "CocktailHandler")

	v := req.URL.Query()

	drinks, _ := req.URL.Query()["include"]

	include := v.Get("include")
	exclude := v.Get("exclude")
	secondDrink := ""

	if len(drinks) > 1 {
		log.Println("Url Param 'key' is missing")
		secondDrink = drinks[1]
	}

	cypher := `
	MATCH 
		(drink:Beverage)-[:PART_OF]->(group:Cocktail) 
	WHERE 
		drink.name =~ {name}
	RETURN
		group.name, group.alcohol`

	neoMap := map[string]interface{}{"name": "(?i)" + include}

	if exclude != "" && secondDrink != "" {
		cypher =
			`MATCH
		(drink:Beverage)-[:PART_OF]->(group:Cocktail)<-[:PART_OF]-(drink2:Beverage),
		(drink3:Beverage {name: {excludedName}})
		WHERE
		drink.name =~ {name} AND drink2.name =~ {secondName} 
		AND NOT
		(drink3)-[:PART_OF]->(group)
		RETURN
		group.name, group.alcohol`

		neoMap = map[string]interface{}{"name": "(?i)" + include, "secondName": "(?i)" + secondDrink,
			"excludedName": strings.Title(exclude)}
	}

	if exclude != "" && secondDrink == "" {
		cypher = `
	MATCH 
		(drink:Beverage {name: {name}})-[:PART_OF]->(group:Cocktail), (drink2:Beverage {name: {excludedName}}) 
	WHERE NOT 
		(drink2)-[:PART_OF]->(group) 
	RETURN group.name, group.alcohol`
		neoMap = map[string]interface{}{"name": strings.Title(include), "excludedName": strings.Title(exclude)}
	}

	if secondDrink != "" && exclude == "" {
		cypher = `
	MATCH 
		(drink:Beverage)-[:PART_OF]->(group:Cocktail)<-[:PART_OF]-(drink2:Beverage) 
	WHERE
		drink.name =~ {name} AND drink2.name =~ {secondName} 
	RETURN 
		group.name, group.alcohol`

		neoMap = map[string]interface{}{"name": "(?i)" + include, "secondName": "(?i)" + secondDrink}
	}

	data, _, _, err := db.QueryNeoAll(cypher, neoMap)
	if err != nil {
		RespondWithAnError(502, err.Error(), w, ctx)
		return
	}

	if len(data) == 0 {
		RespondWithAnError(404, notFoundMessage, w, ctx)
		return
	}

	results := make([]CocktailResult, len(data))
	for idx, row := range data {
		results[idx] = CocktailResult{
			Cocktail{
				Name:    row[0].(string),
				Alcohol: row[1].(string),
			},
		}
	}

	respondWithJSON(ctx, w, 200, results)
}
