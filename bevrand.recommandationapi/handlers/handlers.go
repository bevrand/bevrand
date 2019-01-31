package handlers

import (
	"bevrand.recommandationapi/models"
	"context"
	"encoding/json"
	"github.com/opentracing/opentracing-go"
	"io"
	"log"
	"net/http"
	"strconv"
	openlog "github.com/opentracing/opentracing-go/log"
	driver "github.com/johnnadratowski/golang-neo4j-bolt-driver"
)

var (
	Neo4jURL = ""
)

func SearchHandler(w http.ResponseWriter, req *http.Request) {
	tracer:= opentracing.GlobalTracer()
	span := tracer.StartSpan("searchHandler")
	span.SetTag("Method", "searchHandler")
	span.LogFields(
		openlog.String("method", req.Method),
		openlog.String("path", req.URL.Path),
		openlog.String("host", req.Host),
	)
	ctx := context.Background()
	ctx = opentracing.ContextWithSpan(ctx, span)
	defer span.Finish()

	w.Header().Set("Content-Type", "application/json")

	query := req.URL.Query()["q"][0]
	cypher := `
	MATCH
		(movie:Movie)
	WHERE
		movie.title =~ {query}
	RETURN
		movie.title as title, movie.tagline as tagline, movie.released as released`

	db, err := driver.NewDriver().OpenNeo(Neo4jURL)
	if err != nil {
		span.LogFields(
			openlog.String("http_status_code", "500"),
			openlog.String("body", "error connecting to neo4j:"),
		)
		w.WriteHeader(500)
		w.Write([]byte("An error occurred connecting to the DB"))
		return
	}
	defer db.Close()

	param := "(?i).*" + query + ".*"
	data, _, _, err := db.QueryNeoAll(cypher, map[string]interface{}{"query": param})
	if err != nil {
		span.LogFields(
			openlog.String("http_status_code", "500"),
			openlog.String("body", "eeror querying search:"),
		)
		w.WriteHeader(500)
		w.Write([]byte("An error occurred querying the DB"))
		return
	} else if len(data) == 0 {
		span.LogFields(
			openlog.String("http_status_code", "404"),
		)
		w.WriteHeader(404)
		return
	}

	results := make([]models.MovieResult, len(data))
	for idx, row := range data {
		results[idx] = models.MovieResult{
		models.Movie{
				Title:    row[0].(string),
				Tagline:  row[1].(string),
				Released: int(row[2].(int64)),
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

func MovieHandler(w http.ResponseWriter, req *http.Request) {
	tracer:= opentracing.GlobalTracer()
	span := tracer.StartSpan("movieHandler")
	span.SetTag("Method", "movieHandler")
	span.LogFields(
		openlog.String("method", req.Method),
		openlog.String("path", req.URL.Path),
		openlog.String("host", req.Host),
	)
	ctx := context.Background()
	ctx = opentracing.ContextWithSpan(ctx, span)
	defer span.Finish()
	w.Header().Set("Content-Type", "application/json")

	query := req.URL.Path[len("/movie/"):]
	cypher := `
	MATCH
		(movie:Movie {title:{title}})
	OPTIONAL MATCH
		(movie)<-[r]-(person:Person)
	WITH
		movie.title as title,
		collect({name:person.name, job:head(split(lower(type(r)),'_')), role:r.roles}) as cast
	LIMIT 1
	UNWIND cast as c
	RETURN title, c.name as name, c.job as job, c.role as role`

	db, err := driver.NewDriver().OpenNeo(Neo4jURL)
	if err != nil {
		span.LogFields(
			openlog.String("http_status_code", "500"),
			openlog.String("body", "error connecting to neo4j:"),
		)
		w.WriteHeader(500)
		w.Write([]byte("An error occurred connecting to the DB"))
		return
	}
	defer db.Close()

	data, _, _, err := db.QueryNeoAll(cypher, map[string]interface{}{"title": query})
	if err != nil {
		span.LogFields(
			openlog.String("http_status_code", "500"),
			openlog.String("body", "error querying movie:"),
		)
		log.Println("error querying movie:", err)
		w.WriteHeader(500)
		w.Write([]byte("An error occurred querying the DB"))
		return
	} else if len(data) == 0 {
		span.LogFields(
			openlog.String("http_status_code", "404"),
		)
		w.WriteHeader(404)
		return
	}

	movie := models.Movie{
		Title: data[0][0].(string),
		Cast:  make([]models.Person, len(data)),
	}

	for idx, row := range data {
		movie.Cast[idx] = models.Person{
			Name: row[1].(string),
			Job:  row[2].(string),
		}
		if row[3] != nil {
			movie.Cast[idx].Role = interfaceSliceToString(row[3].([]interface{}))
		}
	}

	err = json.NewEncoder(w).Encode(movie)
	if err != nil {
		span.LogFields(
			openlog.String("http_status_code", "500"),
			openlog.String("body", "error writing movie response:"),
		)
		w.WriteHeader(500)
		w.Write([]byte("An error occurred writing response"))
	}
}

func GraphHandler(w http.ResponseWriter, req *http.Request) {
	tracer:= opentracing.GlobalTracer()
	span := tracer.StartSpan("graphHandler")
	span.SetTag("Method", "graphHandler")
	span.LogFields(
		openlog.String("method", req.Method),
		openlog.String("path", req.URL.Path),
		openlog.String("host", req.Host),
	)
	ctx := context.Background()
	ctx = opentracing.ContextWithSpan(ctx, span)
	defer span.Finish()


	w.Header().Set("Content-Type", "application/json")

	limits := req.URL.Query()["limit"]
	limit := 50
	var err error
	if len(limits) > 0 {
		limit, err = strconv.Atoi(limits[0])
		if err != nil {
			span.LogFields(
				openlog.String("http_status_code", "400"),
				openlog.String("body", "Limit must be an integer"),
			)
			w.WriteHeader(400)
			w.Write([]byte("Limit must be an integer"))
		}
	}

	cypher := `
	MATCH
		(m:Movie)<-[:ACTED_IN]-(a:Person)
	RETURN
		m.title as movie, collect(a.name) as cast
	LIMIT
		{limit}`

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
		span.LogFields(
			openlog.String("http_status_code", "500"),
			openlog.String("body", "error preparing graph:"),
		)
		w.WriteHeader(500)
		w.Write([]byte("An error occurred querying the DB"))
		return
	}
	defer stmt.Close()

	rows, err := stmt.QueryNeo(map[string]interface{}{"limit": limit})
	if err != nil {
		span.LogFields(
			openlog.String("http_status_code", "500"),
			openlog.String("body", "error querying neo4j:"),
		)
		w.WriteHeader(500)
		w.Write([]byte("An error occurred querying the DB"))
		return
	}

	d3Resp := models.D3Response{}
	row, _, err := rows.NextNeo()
	for row != nil && err == nil {
		title := row[0].(string)
		actors := interfaceSliceToString(row[1].([]interface{}))
		d3Resp.Nodes = append(d3Resp.Nodes, models.Node{Title: title, Label: "movie"})
		movIdx := len(d3Resp.Nodes) - 1
		for _, actor := range actors {
			idx := -1
			for i, node := range d3Resp.Nodes {
				if actor == node.Title && node.Label == "actor" {
					idx = i
					break
				}
			}
			if idx == -1 {
				d3Resp.Nodes = append(d3Resp.Nodes, models.Node{Title: actor, Label: "actor"})
				d3Resp.Links = append(d3Resp.Links, models.Link{Source: len(d3Resp.Nodes) - 1, Target: movIdx})
			} else {
				d3Resp.Links = append(d3Resp.Links, models.Link{Source: idx, Target: movIdx})
			}
		}
		row, _, err = rows.NextNeo()
	}

	if err != nil && err != io.EOF {
		span.LogFields(
			openlog.String("http_status_code", "500"),
			openlog.String("body", "error querying graph:"),
		)
		w.WriteHeader(500)
		w.Write([]byte("An error occurred querying the DB"))
		return
	} else if len(d3Resp.Nodes) == 0 {
		span.LogFields(
			openlog.String("http_status_code", "404"),
		)
		w.WriteHeader(404)
		return
	}

	err = json.NewEncoder(w).Encode(d3Resp)
	if err != nil {
		span.LogFields(
			openlog.String("http_status_code", "500"),
			openlog.String("body", "error writing graph response:"),
		)
		w.WriteHeader(500)
		w.Write([]byte("An error occurred writing response"))
	}
}

func interfaceSliceToString(s []interface{}) []string {
	o := make([]string, len(s))
	for idx, item := range s {
		o[idx] = item.(string)
	}
	return o
}

