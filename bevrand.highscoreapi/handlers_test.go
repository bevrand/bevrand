package main

import (
	"encoding/json"
	"github.com/alicebob/miniredis"
	"github.com/appleboy/gofight/v2"
	"github.com/mediocregopher/radix.v2/pool"
	"github.com/stretchr/testify/assert"
	"log"
	"net/http"
	"testing"
)

const drink = "beer"
const user = "marvin"
const playlistUser = "paranoid"
const userKey = user + ":" + playlistUser
const prefixURL = "/api/v1/highscores/"
const marvinURL = prefixURL + user + "/" + playlistUser + "/"

func TestIncreaseGlobalCount(t *testing.T) {
	createMockDatabase()

	// increase count to 1 so when we post we get > 1 for both globaluser
	key := GLOBALNAME + ":" + GLOBALLIST

	setDrinksInRedis(key, drink)

	// get scores after redis insert
	scores := getHandler(prefixURL, t)
	assert.Equal(t, drink, scores[0].Drink)
	assert.Equal(t, 1, scores[0].Rolled)
}

func TestIncreaseCountExists(t *testing.T) {
	createMockDatabase()

	// increase count to 1 so when we post we get > 1 for both global and user
	key := GLOBALNAME + ":" + GLOBALLIST

	setDrinksInRedis(key, drink)
	setDrinksInRedis(userKey, drink)

	// post drink to user url
	postHandler(marvinURL, drink, t)

	// get scores after post
	scores := getHandler(marvinURL, t)
	assert.Equal(t, drink, scores[0].Drink)
	assert.Equal(t, 2, scores[0].Rolled)
}

func TestIncreaseGlobalCountExists(t *testing.T) {
	createMockDatabase()

	// increase count to 1 so when we post we get > 1 for both global and user
	key := GLOBALNAME + ":" + GLOBALLIST

	setDrinksInRedis(key, drink)
	setDrinksInRedis(userKey, drink)

	// post drink to user url
	postHandler(marvinURL, drink, t)

	// get scores after post
	scores := getHandler(prefixURL, t)
	assert.Equal(t, drink, scores[0].Drink)
	assert.Equal(t, 2, scores[0].Rolled)
}

func TestIncreaseCountDoesNotExist(t *testing.T) {
	createMockDatabase()

	// post drink to user url
	postHandler(marvinURL, drink, t)

	// get scores after post
	scores := getHandler(marvinURL, t)
	assert.Equal(t, drink, scores[0].Drink)
	assert.Equal(t, 1, scores[0].Rolled)
}

func TestIncreaseGlobalCountDoesNotExist(t *testing.T) {
	// create a new pool
	createMockDatabase()

	// post drink to user url
	postHandler(marvinURL, drink, t)

	// get scores after post
	scores := getHandler(prefixURL, t)
	assert.Equal(t, drink, scores[0].Drink)
	assert.Equal(t, 1, scores[0].Rolled)
}

func createMockDatabase() {
	var err error
	// Establish a pool of 10 connections to the Redis server listening on
	// port 6379 of the variable that has been used
	s, err := miniredis.Run()
	if err != nil {
		panic(err)
	}
	db, err = pool.New("tcp", s.Addr(), 2)
	if err != nil {
		panic(err)
	}
}

func setDrinksInRedis(key string, drink string) {
	err := db.Cmd(keySet, key, drink, 1).Err
	if err != nil {
		log.Fatal(err)
	}
}

func postHandler(url string, drink string, t *testing.T) {
	r := gofight.New()

	r.POST(url).
		SetJSON(gofight.D{
			"drink": drink,
		}).
		SetDebug(true).
		Run(InitRoutes(), func(r gofight.HTTPResponse, rq gofight.HTTPRequest) {
			assert.Equal(t, http.StatusCreated, r.Code)
			assert.NotEqual(t, http.NoBody, rq.Body)
		})
}

func getHandler(url string, t *testing.T) []Score {
	r := gofight.New()
	var scores []Score
	r.GET(url).
		SetDebug(true).
		Run(InitRoutes(), func(r gofight.HTTPResponse, rq gofight.HTTPRequest) {
			err := json.Unmarshal([]byte(r.Body.String()), &scores)
			if err != nil {
				panic(err)
			}

			assert.Equal(t, http.StatusOK, r.Code)
			assert.Equal(t, http.NoBody, rq.Body)
		})

	return scores
}
