package main

import (
	"encoding/json"
	"github.com/alicebob/miniredis"
	"github.com/appleboy/gofight"
	"github.com/mediocregopher/radix.v2/pool"
	"github.com/stretchr/testify/assert"
	"log"
	"net/http"
	"testing"
)

func TestIncreaseGlobalCount(t *testing.T) {
	s, err := miniredis.Run()
	if err != nil {
		panic(err)
	}
	defer s.Close()

	// create a new pool
	db, err = pool.New("tcp", s.Addr(), 2)
	if err != nil {
		panic(err)
	}

	key := GLOBALNAME + ":" + GLOBALLIST
	drink := "beer"

	// set key that will be expected
	err = db.Cmd(keySet, key, drink, 1).Err
	if err != nil {
		log.Fatal(err)
	}

	r := gofight.New()

	r.GET("/api/v1/highscores/").
		SetDebug(true).
		Run(InitRoutes(), func(r gofight.HTTPResponse, rq gofight.HTTPRequest) {
			var scores []Score
			err = json.Unmarshal([]byte(r.Body.String()), &scores)
			if err != nil {
				panic(err)
			}

			assert.Equal(t, drink, scores[0].Drink)
			assert.Equal(t, 1, scores[0].Rolled)
			assert.Equal(t, http.StatusOK, r.Code)
		})
}

func TestIncreaseCountExists(t *testing.T) {
	s, err := miniredis.Run()
	if err != nil {
		panic(err)
	}
	defer s.Close()

	// create a new pool
	db, err = pool.New("tcp", s.Addr(), 2)
	if err != nil {
		panic(err)
	}

	key := GLOBALNAME + ":" + GLOBALLIST
	drink := "beer"

	user := "marvin"
	playlist := "paranoid"

	keyUser := user + ":" + playlist

	// set key that will be expected
	err = db.Cmd(keySet, key, drink, 1).Err
	if err != nil {
		log.Fatal(err)
	}

	// set key that will be expected
	err = db.Cmd(keySet, keyUser, drink, 1).Err
	if err != nil {
		log.Fatal(err)
	}

	r := gofight.New()

	r.POST("/api/v1/highscores/"+user+"/"+playlist+"/").
		SetJSON(gofight.D{
			"drink": drink,
		}).
		SetDebug(true).
		Run(InitRoutes(), func(r gofight.HTTPResponse, rq gofight.HTTPRequest) {
			assert.Equal(t, http.StatusCreated, r.Code)
		})

	r.GET("/api/v1/highscores/"+user+"/"+playlist+"/").
		SetDebug(true).
		Run(InitRoutes(), func(r gofight.HTTPResponse, rq gofight.HTTPRequest) {
			var scores []Score
			err = json.Unmarshal([]byte(r.Body.String()), &scores)
			if err != nil {
				panic(err)
			}

			assert.Equal(t, drink, scores[0].Drink)
			assert.Equal(t, 2, scores[0].Rolled)
			assert.Equal(t, http.StatusOK, r.Code)
		})
}

func TestIncreaseGlobalCountExists(t *testing.T) {
	s, err := miniredis.Run()
	if err != nil {
		panic(err)
	}
	defer s.Close()

	// create a new pool
	db, err = pool.New("tcp", s.Addr(), 2)
	if err != nil {
		panic(err)
	}

	key := GLOBALNAME + ":" + GLOBALLIST
	drink := "beer"

	user := "marvin"
	playlist := "paranoid"

	keyUser := user + ":" + playlist

	// set key that will be expected
	err = db.Cmd(keySet, key, drink, 1).Err
	if err != nil {
		log.Fatal(err)
	}

	// set key that will be expected
	err = db.Cmd(keySet, keyUser, drink, 1).Err
	if err != nil {
		log.Fatal(err)
	}

	r := gofight.New()

	r.POST("/api/v1/highscores/"+user+"/"+playlist+"/").
		SetJSON(gofight.D{
			"drink": drink,
		}).
		SetDebug(true).
		Run(InitRoutes(), func(r gofight.HTTPResponse, rq gofight.HTTPRequest) {
			assert.Equal(t, http.StatusCreated, r.Code)
		})

	r.GET("/api/v1/highscores/").
		SetDebug(true).
		Run(InitRoutes(), func(r gofight.HTTPResponse, rq gofight.HTTPRequest) {
			var scores []Score
			err = json.Unmarshal([]byte(r.Body.String()), &scores)
			if err != nil {
				panic(err)
			}

			assert.Equal(t, drink, scores[0].Drink)
			assert.Equal(t, 2, scores[0].Rolled)
			assert.Equal(t, http.StatusOK, r.Code)
		})
}

func TestIncreaseCountDoesNotExist(t *testing.T) {
	s, err := miniredis.Run()
	if err != nil {
		panic(err)
	}
	defer s.Close()

	// create a new pool
	db, err = pool.New("tcp", s.Addr(), 2)
	if err != nil {
		panic(err)
	}

	drink := "beer"

	user := "marvin"
	playlist := "paranoid"

	r := gofight.New()

	r.POST("/api/v1/highscores/"+user+"/"+playlist+"/").
		SetJSON(gofight.D{
			"drink": drink,
		}).
		SetDebug(true).
		Run(InitRoutes(), func(r gofight.HTTPResponse, rq gofight.HTTPRequest) {
			assert.Equal(t, http.StatusCreated, r.Code)
		})

	r.GET("/api/v1/highscores/"+user+"/"+playlist+"/").
		SetDebug(true).
		Run(InitRoutes(), func(r gofight.HTTPResponse, rq gofight.HTTPRequest) {
			var scores []Score
			err = json.Unmarshal([]byte(r.Body.String()), &scores)
			if err != nil {
				panic(err)
			}

			assert.Equal(t, drink, scores[0].Drink)
			assert.Equal(t, 1, scores[0].Rolled)
			assert.Equal(t, http.StatusOK, r.Code)
		})
}

func TestIncreaseGlobalCountDoesNotExist(t *testing.T) {
	s, err := miniredis.Run()
	if err != nil {
		panic(err)
	}
	defer s.Close()

	// create a new pool
	db, err = pool.New("tcp", s.Addr(), 2)
	if err != nil {
		panic(err)
	}

	drink := "beer"

	user := "marvin"
	playlist := "paranoid"

	r := gofight.New()

	r.POST("/api/v1/highscores/"+user+"/"+playlist+"/").
		SetJSON(gofight.D{
			"drink": drink,
		}).
		SetDebug(true).
		Run(InitRoutes(), func(r gofight.HTTPResponse, rq gofight.HTTPRequest) {
			assert.Equal(t, http.StatusCreated, r.Code)
		})

	r.GET("/api/v1/highscores/").
		SetDebug(true).
		Run(InitRoutes(), func(r gofight.HTTPResponse, rq gofight.HTTPRequest) {
			var scores []Score
			err = json.Unmarshal([]byte(r.Body.String()), &scores)
			if err != nil {
				panic(err)
			}

			assert.Equal(t, drink, scores[0].Drink)
			assert.Equal(t, 1, scores[0].Rolled)
			assert.Equal(t, http.StatusOK, r.Code)
		})
}
