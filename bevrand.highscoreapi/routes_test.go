package main

import (
	"bytes"
	"encoding/json"
	"github.com/gin-gonic/gin"
	"github.com/stretchr/testify/assert"
	"log"
	"net/http"
	"net/http/httptest"
	"testing"
)

const message = "message"

var drinkList = [3]string{"beer", "wine", "coke"}

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
	createMockDatabase()

	key := GLOBALNAME + ":" + GLOBALLIST

	for _, drink := range drinkList {
		// set key that will be expected
		setDrinksInRedis(key, drink)
	}

	router := InitRoutes()

	w := performRequest(router, "GET", prefixURL)
	assert.Equal(t, http.StatusOK, w.Code)

	// Convert the JSON response to a map
	var response []Score
	err := json.Unmarshal([]byte(w.Body.String()), &response)
	if err != nil {
		log.Fatal(err)
	}

	// Make some assertions on the correctness of the response.
	for _, resp := range response {
		assert.Contains(t, drinkList, resp.Drink)
	}
}

func TestRouteShowHighScoreNonExistent(t *testing.T) {
	createMockDatabase()

	router := InitRoutes()

	w := performRequest(router, "GET", marvinURL)
	assert.Equal(t, http.StatusNotFound, w.Code)
}

func TestRouteShowHighScore(t *testing.T) {
	createMockDatabase()

	for _, drink := range drinkList {
		// set key that will be expected
		setDrinksInRedis(userKey, drink)
	}

	router := InitRoutes()

	w := performRequest(router, "GET", marvinURL)
	assert.Equal(t, http.StatusOK, w.Code)

	// Convert the JSON response to a map
	var response []Score
	err := json.Unmarshal([]byte(w.Body.String()), &response)
	if err != nil {
		log.Fatal(err)
	}

	// Make some assertions on the correctness of the response.
	for _, resp := range response {
		assert.Contains(t, drinkList, resp.Drink)
	}
}

func TestRouteIncrementHighscore(t *testing.T) {
	createMockDatabase()

	router := InitRoutes()

	drink := PostObject{drink}
	body, err := json.Marshal(drink)
	if err != nil {
		panic(err)
	}
	req, _ := http.NewRequest("POST", marvinURL, bytes.NewBuffer(body))
	w := httptest.NewRecorder()
	router.ServeHTTP(w, req)
	assert.Equal(t, http.StatusCreated, w.Code)
}

func TestRouteIncrementHighscoreWithBadBody(t *testing.T) {
	createMockDatabase()

	router := InitRoutes()

	errorDrink := ErrorModel{drink, "someuniquecode"}
	body, err := json.Marshal(errorDrink)
	if err != nil {
		panic(err)
	}
	req, _ := http.NewRequest("POST", marvinURL, bytes.NewBuffer(body))
	w := httptest.NewRecorder()
	router.ServeHTTP(w, req)
	assert.Equal(t, http.StatusBadRequest, w.Code)

	var response ErrorModel
	err = json.Unmarshal([]byte(w.Body.String()), &response)
	assert.Contains(t, response.Message, "have to provide a body")
}

func TestRouteIncrementHighscoreWithNilBody(t *testing.T) {
	createMockDatabase()

	router := InitRoutes()

	req, _ := http.NewRequest("POST", marvinURL, bytes.NewBuffer(nil))
	w := httptest.NewRecorder()
	router.ServeHTTP(w, req)
	assert.Equal(t, http.StatusBadRequest, w.Code)

	var response ErrorModel
	err := json.Unmarshal([]byte(w.Body.String()), &response)
	if err != nil {
		panic(err)
	}
	assert.Contains(t, response.Message, "EOF")
}

func TestRouteIncrementHighscoreGlobalUser(t *testing.T) {
	createMockDatabase()

	router := InitRoutes()

	errorDrink := PostObject{drink}
	body, err := json.Marshal(errorDrink)
	if err != nil {
		panic(err)
	}
	req, _ := http.NewRequest("POST", prefixURL+"global/paranoid/", bytes.NewBuffer(body))
	w := httptest.NewRecorder()
	router.ServeHTTP(w, req)
	assert.Equal(t, http.StatusBadRequest, w.Code)

	var response ErrorModel
	err = json.Unmarshal([]byte(w.Body.String()), &response)
	assert.Contains(t, response.Message, "is a restricted user")
}

func performRequest(r http.Handler, method, path string) *httptest.ResponseRecorder {
	req, _ := http.NewRequest(method, path, nil)
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	return w
}
