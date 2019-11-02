package main

import (
	"bytes"
	"encoding/json"
	"github.com/stretchr/testify/assert"
	"net/http"
	"net/http/httptest"
	"testing"
)

var drinkList = []string{"beer", "wine", "coke"}
const user = "marvin"
const playlistUser = "paranoid"

func TestPingPongRoute(t *testing.T) {
	router := InitRoutes()
	queueDrinks = false

	w := performGetRequest(router, "/api/ping")
	assert.Equal(t, http.StatusOK, w.Code)
	assert.Equal(t, "pong", w.Body.String())
}

func TestRandomizeRoute(t *testing.T) {
	router := InitRoutes()
	queueDrinks = false

	requestBody := RandomizeRequest{drinkList, playlistUser, user }
	body, _ := json.Marshal(requestBody)

	w := performPostRequest(router, "/api/v1/randomize", body)
	var result ResultModel
	err := json.Unmarshal(w.Body.Bytes(), &result)

	assert.Nil(t, err)
	assert.Contains(t, drinkList, result.Result)
	assert.Equal(t, 200, w.Code)
}

func TestRandomizeRouteWrongMethod(t *testing.T) {
	router := InitRoutes()
	queueDrinks = false

	w := performGetRequest(router, "/api/v1/randomize")
	var result MethodError
	err := json.Unmarshal(w.Body.Bytes(), &result)

	assert.Nil(t, err)
	assert.Equal(t, 405, w.Code)
	assert.Equal(t, "POST", result.Messages[0].Methods)
	assert.Contains(t, result.Messages[0].Message, "GET")
}

func TestRandomizeRouteInvalidUser(t *testing.T) {
	router := InitRoutes()
	queueDrinks = false

	requestBody := RandomizeRequest{drinkList, playlistUser, invalidUser }
	body, _ := json.Marshal(requestBody)

	w := performPostRequest(router, "/api/v1/randomize", body)
	var result ValidationError
	err := json.Unmarshal(w.Body.Bytes(), &result)

	assert.Nil(t, err)
	assert.Equal(t, 400, w.Code)
	assert.Equal(t, usernameField, result.Messages[0].Field)
	assert.Contains(t, result.Messages[0].Message, invalidUser)
}

func TestRandomizeRouteInvalidPlaylist(t *testing.T) {
	router := InitRoutes()

	requestBody := RandomizeRequest{drinkList, invalidPlayList, user }
	body, _ := json.Marshal(requestBody)

	w := performPostRequest(router, "/api/v1/randomize", body)
	var result ValidationError
	err := json.Unmarshal(w.Body.Bytes(), &result)

	assert.Nil(t, err)
	assert.Equal(t, 400, w.Code)
	assert.Equal(t, playlistField, result.Messages[0].Field)
	assert.Contains(t, result.Messages[0].Message, invalidPlayList)
}

func performGetRequest(r http.Handler, path string) *httptest.ResponseRecorder {
	req, _ := http.NewRequest("GET", path, nil)
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	return w
}

func performPostRequest(r http.Handler, path string, body []byte) *httptest.ResponseRecorder {
	req, _ := http.NewRequest("POST", path, bytes.NewBuffer(body))
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	return w
}