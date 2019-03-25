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
	db, err =  pool.New("tcp", s.Addr(), 2)
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