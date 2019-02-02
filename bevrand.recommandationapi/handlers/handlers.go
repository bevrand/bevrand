package handlers

import (
	"bevrand.recommandationapi/models"
	"context"
	"encoding/json"
	driver "github.com/johnnadratowski/golang-neo4j-bolt-driver"
	"github.com/opentracing/opentracing-go"
	openlog "github.com/opentracing/opentracing-go/log"
	"log"
	"net/http"
	"strconv"
	"strings"
)

var (
	Neo4jURL = "bolt://localhost:7687"
)


func CategorieHandler(w http.ResponseWriter, req *http.Request) {
	tracer:= opentracing.GlobalTracer()
	span := tracer.StartSpan("CategorieHandler")
	span.SetTag("Method", "Categories")
	span.LogFields(
		openlog.String("method", req.Method),
		openlog.String("path", req.URL.Path),
		openlog.String("host", req.Host),
	)
	ctx := context.Background()
	ctx = opentracing.ContextWithSpan(ctx, span)
	defer span.Finish()

	v := req.URL.Query()
	kindQuery := v.Get("kind")

	if kindQuery == "" {
		kindQuery = "Beer"
	}

	cypher := `
	MATCH (drink:Beverage)-[:KIND_OF]->(group:BevGroup) WHERE group.name =~ {kindOf} return drink.name, drink.perc, drink.type, drink.country
	`

	db, err := driver.NewDriver().OpenNeo(Neo4jURL)
	if err != nil {
		span.LogFields(
			openlog.String("http_status_code", "500"),
			openlog.String("body", "error connecting to neo4j"),
		)
		w.WriteHeader(500)
		w.Write([]byte("An error occurred connecting to the DB"))
		return
	}
	defer db.Close()

	data, _, _, err := db.QueryNeoAll(cypher, map[string]interface{}{"kindOf": "(?i)" + kindQuery})
	if err != nil {
		span.LogFields(
			openlog.String("http_status_code", "500"),
			openlog.String("body", "error querying search:"),
		)
		w.WriteHeader(500)
		w.Write([]byte("An error occurred querying the DB"))
		return
	} else if len(data) == 0 {
		span.LogFields(
			openlog.String("http_status_code", "404"),
		)
		w.WriteHeader(404)
		w.Write([]byte("No results found for query"))
		return
	}

	results := make([]models.BeverageResult, len(data))
	for idx, row := range data {
		country := ""
		if row[3] != nil {
			country = row[3].(string)
		}
		results[idx] = models.BeverageResult{
			models.Beverage{
				Name:    row[0].(string),
				Perc: int(row[1].(int64)),
				Type: row[2].(string),
				Country: country,
			},
		}
	}

	body, err := json.MarshalIndent(results, "", "    ")
	if err != nil {
		log.Println(err)
	}
	span.LogFields(
		openlog.String("http_status_code", "200"),
		openlog.String("body", string(body)),
	)

	err = json.NewEncoder(w).Encode(results)
	if err != nil {
		span.LogFields(
			openlog.String("http_status_code", "500"),
			openlog.String("body", "error writing search response:"),
		)
		w.WriteHeader(500)
		w.Write([]byte("An error occurred writing response"))
	}
}

func BeverageHandler(w http.ResponseWriter, req *http.Request) {
	tracer := opentracing.GlobalTracer()
	span := tracer.StartSpan("Beverages")
	span.SetTag("Method", "Beverages")
	span.LogFields(
		openlog.String("method", req.Method),
		openlog.String("path", req.URL.Path),
		openlog.String("host", req.Host),
	)
	ctx := context.Background()
	ctx = opentracing.ContextWithSpan(ctx, span)
	defer span.Finish()

	v := req.URL.Query()

	limits := v.Get("limit")
	limit := 50
	var err error
	if len(limits) > 0 {
		limit, err = strconv.Atoi(limits)
		if err != nil {
			span.LogFields(
				openlog.String("http_status_code", "400"),
				openlog.String("body", "Limit must be an integer"),
			)
			w.WriteHeader(400)
			w.Write([]byte("Limit must be an integer"))
		}
	}

	cypher := `MATCH (n:Beverage) RETURN n.name, n.perc, n.type, n.country LIMIT {limit}`

	db, err := driver.NewDriver().OpenNeo(Neo4jURL)
	if err != nil {
		span.LogFields(
			openlog.String("http_status_code", "500"),
			openlog.String("body", "error connecting to neo4j"),
		)
		w.WriteHeader(500)
		w.Write([]byte("An error occurred connecting to the DB"))
		return
	}
	defer db.Close()

	data, _, _, err := db.QueryNeoAll(cypher, map[string]interface{}{"limit": limit})
	if err != nil {
		span.LogFields(
			openlog.String("http_status_code", "500"),
			openlog.String("body", "error querying search:"),
		)
		w.WriteHeader(500)
		w.Write([]byte("An error occurred querying the DB"))
		return
	} else if len(data) == 0 {
		span.LogFields(
			openlog.String("http_status_code", "404"),
		)
		w.WriteHeader(404)
		w.Write([]byte("No results found for query"))
		return
	}

	results := make([]models.BeverageResult, len(data))
	for idx, row := range data {
		country := ""
		if row[3] != nil {
			country = row[3].(string)
		}
		results[idx] = models.BeverageResult{
			models.Beverage{
				Name:    row[0].(string),
				Perc: int(row[1].(int64)),
				Type: row[2].(string),
				Country: country,
			},
		}
	}

	body, err := json.MarshalIndent(results, "", "    ")
	if err != nil {
		log.Println(err)
	}
	span.LogFields(
		openlog.String("http_status_code", "200"),
		openlog.String("body", string(body)),
	)

	err = json.NewEncoder(w).Encode(results)
	if err != nil {
		span.LogFields(
			openlog.String("http_status_code", "500"),
			openlog.String("body", "error writing search response:"),
		)
		w.WriteHeader(500)
		w.Write([]byte("An error occurred writing response"))
	}
}

func BeverageGroupHandler(w http.ResponseWriter, req *http.Request) {
	tracer:= opentracing.GlobalTracer()
	span := tracer.StartSpan("BeverageGroups")
	span.SetTag("Method", "BeverageGroups")
	span.LogFields(
		openlog.String("method", req.Method),
		openlog.String("path", req.URL.Path),
		openlog.String("host", req.Host),
	)
	ctx := context.Background()
	ctx = opentracing.ContextWithSpan(ctx, span)
	defer span.Finish()

	cypher := `
	MATCH (n:BevGroup) RETURN n.name
	`

	db, err := driver.NewDriver().OpenNeo(Neo4jURL)
	if err != nil {
		span.LogFields(
			openlog.String("http_status_code", "500"),
			openlog.String("body", "error connecting to neo4j"),
		)
		w.WriteHeader(500)
		w.Write([]byte("An error occurred connecting to the DB"))
		return
	}
	defer db.Close()

	stmt, err := db.PrepareNeo(cypher)
	if err != nil {

		w.WriteHeader(500)
		w.Write([]byte("An error occurred querying the DB"))
		return
	}
	defer stmt.Close()

	rows, err := stmt.QueryNeo(map[string]interface{}{})
	if err != nil {

		w.WriteHeader(500)
		w.Write([]byte("An error occurred querying the DB"))
		return
	}

	d3Resp := models.D3BevGroupResponse{}
	row, _, err := rows.NextNeo()
	for row != nil && err == nil {
		title := row[0].(string)
		println(row)
		d3Resp.Nodes = append(d3Resp.Nodes, models.Node{Title: title, Label: "Group"})

		row, _, err = rows.NextNeo()
	}

	err = json.NewEncoder(w).Encode(d3Resp)
}

func CocktailHandler(w http.ResponseWriter, req *http.Request) {
	tracer := opentracing.GlobalTracer()
	span := tracer.StartSpan("CocktailHandler")
	span.SetTag("Method", "Cocktails")
	span.LogFields(
		openlog.String("method", req.Method),
		openlog.String("path", req.URL.Path),
		openlog.String("host", req.Host),
	)
	ctx := context.Background()
	ctx = opentracing.ContextWithSpan(ctx, span)
	defer span.Finish()

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

	neoMap :=  map[string]interface{}{"name": "(?i)" + include}

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

		neoMap =  map[string]interface{}{"name": "(?i)" + include, "secondName": "(?i)" + secondDrink,
			"excludedName": strings.Title(exclude)}
	}

	if exclude != "" && secondDrink == "" {
		cypher = `
	MATCH 
		(drink:Beverage {name: {name}})-[:PART_OF]->(group:Cocktail), (drink2:Beverage {name: {excludedName}}) 
	WHERE NOT 
		(drink2)-[:PART_OF]->(group) 
	RETURN group.name, group.alcohol`
		neoMap =  map[string]interface{}{"name":  strings.Title(include), "excludedName": strings.Title(exclude)}
	}

	if secondDrink != "" && exclude == ""{
		cypher = `
	MATCH 
		(drink:Beverage)-[:PART_OF]->(group:Cocktail)<-[:PART_OF]-(drink2:Beverage) 
	WHERE
		drink.name =~ {name} AND drink2.name =~ {secondName} 
	RETURN 
		group.name, group.alcohol`

		neoMap =  map[string]interface{}{"name": "(?i)" + include, "secondName": "(?i)" + secondDrink}
	}

	db, err := driver.NewDriver().OpenNeo(Neo4jURL)
	data, _, _, err := db.QueryNeoAll(cypher, neoMap)
	if err != nil {
		span.LogFields(
			openlog.String("http_status_code", "500"),
			openlog.String("body", "error connecting to neo4j"),
		)
		w.WriteHeader(500)
		w.Write([]byte("An error occurred connecting to the DB"))
		return
	}
	defer db.Close()

	if err != nil {
		span.LogFields(
			openlog.String("http_status_code", "500"),
			openlog.String("body", "error querying search:"),
		)
		w.WriteHeader(500)
		w.Write([]byte("An error occurred querying the DB"))
		return
	} else if len(data) == 0 {
		span.LogFields(
			openlog.String("http_status_code", "404"),
		)
		w.WriteHeader(404)
		w.Write([]byte("No results found for query"))
		return
	}

	results := make([]models.CocktailResult, len(data))
	for idx, row := range data {
		results[idx] = models.CocktailResult{
			models.Cocktail{
				Name:    row[0].(string),
				Alcohol: row[1].(string),
			},
		}
	}

	body, err := json.MarshalIndent(results, "", "    ")
	if err != nil {
		log.Println(err)
	}
	span.LogFields(
		openlog.String("http_status_code", "200"),
		openlog.String("body", string(body)),
	)

	err = json.NewEncoder(w).Encode(results)
	if err != nil {
		span.LogFields(
			openlog.String("http_status_code", "500"),
			openlog.String("body", "error writing search response:"),
		)
		w.WriteHeader(500)
		w.Write([]byte("An error occurred writing response"))
	}
}

