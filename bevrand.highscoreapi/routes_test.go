package main

import (
	"encoding/json"
	"github.com/alicebob/miniredis"
	"github.com/gin-gonic/gin"
	"github.com/mediocregopher/radix.v2/pool"
	"github.com/stretchr/testify/assert"
	"log"
	"net/http"
	"net/http/httptest"
	"testing"
)

const message = "message"

func TestPingPong(t *testing.T) {
	// Build our expected body
	body := gin.H{
		message: "pong",
	}

	router := InitRoutes()

	w := performRequest(router, "GET", "/ping")
	assert.Equal(t, http.StatusOK, w.Code)

	// Convert the JSON response to a map
	var response map[string]string
	err := json.Unmarshal([]byte(w.Body.String()), &response)

	// Grab the value & whether or not it exists
	value, exists := response[message]

	// Make some assertions on the correctness of the response.
	assert.Nil(t, err)
	assert.True(t, exists)
	assert.Equal(t, body[message], value)
}

func TestRouteShowAllHighScore(t *testing.T) {
	s, err := miniredis.Run()
	if err != nil {
		panic(err)
	}
	defer s.Close()

	// create a new pool
	db, err =  pool.New("tcp", s.Addr(), 2)
	if err != nil {
		panic(err)
	}

	key := GLOBALNAME + ":" + GLOBALLIST
	drinks := [3]string{"beer", "wine", "coke"}

	for _, drink := range drinks {
		// set key that will be expected
		err = db.Cmd(keySet, key, drink, 1).Err
		if err != nil {
			log.Fatal(err)
		}
	}

	router := InitRoutes()

	w := performRequest(router, "GET", "/api/v1/highscores/")
	assert.Equal(t, http.StatusOK, w.Code)

	// Convert the JSON response to a map
	var response []Score
	err = json.Unmarshal([]byte(w.Body.String()), &response)

	// Make some assertions on the correctness of the response.
	for _, resp := range response {
		assert.Contains(t, drinks, resp.Drink)
	}
}

func TestRouteShowHighScoreNonExistent(t *testing.T) {
	s, err := miniredis.Run()
	if err != nil {
		panic(err)
	}
	defer s.Close()

	// create a new pool
	db, err =  pool.New("tcp", s.Addr(), 2)
	if err != nil {
		panic(err)
	}

	router := InitRoutes()

	w := performRequest(router, "GET", "/api/v1/highscores/marvin/paranoid/")
	assert.Equal(t, http.StatusNotFound, w.Code)
}

func TestRouteShowHighScore(t *testing.T) {
	s, err := miniredis.Run()
	if err != nil {
		panic(err)
	}
	defer s.Close()

	// create a new pool
	db, err =  pool.New("tcp", s.Addr(), 2)
	if err != nil {
		panic(err)
	}

	key := "marvin:paranoid"
	drinks := [3]string{"beer", "wine", "coke"}

	for _, drink := range drinks {
		// set key that will be expected
		err = db.Cmd(keySet, key, drink, 1).Err
		if err != nil {
			log.Fatal(err)
		}
	}

	router := InitRoutes()

	w := performRequest(router, "GET", "/api/v1/highscores/marvin/paranoid/")
	assert.Equal(t, http.StatusOK, w.Code)

	// Convert the JSON response to a map
	var response []Score
	err = json.Unmarshal([]byte(w.Body.String()), &response)

	// Make some assertions on the correctness of the response.
	for _, resp := range response {
		assert.Contains(t, drinks, resp.Drink)
	}
}

func performRequest(r http.Handler, method, path string) *httptest.ResponseRecorder {
	req, _ := http.NewRequest(method, path, nil)
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	return w
}
