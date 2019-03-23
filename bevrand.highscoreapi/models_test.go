package main

import (
	"encoding/json"
	"github.com/stretchr/testify/assert"
	"testing"
)

func TestModelsCanBeConvertedToProperJson(t *testing.T) {
	expected := "{\"drink\":\"beer\",\"rolled\":2}"
	redisResult := &Score{
		Drink:  "beer",
		Rolled: 2,
	}

	body, err := json.Marshal(redisResult)
	result := string(body)

	assert.Nil(t, err)
	assert.Equal(t, result, expected)
}

func TestErrorModel(t *testing.T) {
	expected := "{\"errorMessage\":\"Could not find combination of user: joeri list: joeri\",\"uniqueCode\":\"someuuid\"}"

	notFoundError := &ErrorModel{
		Message:    "Could not find combination of user: joeri list: joeri",
		UniqueCode: "someuuid"}
	body, err := json.Marshal(notFoundError)
	result := string(body)

	assert.Nil(t, err)
	assert.Equal(t, result, expected)
}
