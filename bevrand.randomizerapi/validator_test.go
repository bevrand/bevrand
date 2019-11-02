package main

import (
	"github.com/stretchr/testify/assert"
	"testing"
)

const invalidUser = "m"
const invalidPlayList = "p"
var invalidDrinklist = []string{"beer"}

func TestValidateUser(t *testing.T) {
	result := validateUsername(invalidUser)

	assert.Equal(t, usernameField, result.Field)
	assert.Contains(t, result.Message, invalidUser)
}

func TestValidatePlaylist(t *testing.T) {
	result := validatePlaylist(invalidPlayList)

	assert.Equal(t, playlistField, result.Field)
	assert.Contains(t, result.Message, invalidPlayList)
}

func TestValidateBeveragelist(t *testing.T) {
	result := validateBeverages(invalidDrinklist)

	assert.Equal(t, beverageField, result.Field)
}
