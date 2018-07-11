package handlers

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
)

type RandomDrink struct {
	Drink string `json:"result"`
}

type RedisList struct {
	List []RedisDrink `json:"frontpage:tgif"`
}

type RedisDrink struct {
	Drink  string `json:"drink"`
	Rolled int    `json:"rolled"`
}

func Index(w http.ResponseWriter, r *http.Request) {
	fmt.Fprint(w, "Welcome!\n")
}

func RandomizeDrink(w http.ResponseWriter, r *http.Request) {
	result := RandomDrink{Drink: "beer"}
	fmt.Println(result)
	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(result)
}

func RedisTopFive(w http.ResponseWriter, r *http.Request) {
	drinkOne := RedisDrink{Drink: "beer", Rolled: 1}
	drinkTwo := RedisDrink{Drink: "beer", Rolled: 2}
	drinkThree := RedisDrink{Drink: "beer", Rolled: 3}
	result := RedisList{List: []RedisDrink{drinkOne, drinkTwo, drinkThree}}
	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	w.WriteHeader(http.StatusOK)
	if err := json.NewEncoder(w).Encode(result); err != nil {
		panic(err)
	}
}

func AllPlayLists(w http.ResponseWriter, r *http.Request) {
	jsonFile, err := ioutil.ReadFile("json_files/allPlayLists.json")
	if err != nil {
		fmt.Println(err)
	}
	result := string(jsonFile)
	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	w.WriteHeader(http.StatusOK)
	if err := json.NewEncoder(w).Encode(json.RawMessage(result)); err != nil {
		panic(err)
	}
}
