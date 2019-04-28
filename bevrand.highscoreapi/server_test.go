package main

import (
	"github.com/stretchr/testify/assert"
	"os"
	"testing"
)

const localURL = "localhost"
const redisURL = "REDIS_URL"

func TestGetEmptyEnvFile(t *testing.T) {
	err := os.Setenv("GO_ENV", "")
	if err != nil {
		assert.Fail(t, err.Error(), "Failed setting env")
	}
	GetEnvFile()
	expectedURL := os.Getenv(redisURL)

	assert.Equal(t, localURL, expectedURL)
}

func TestGetBadEnvFile(t *testing.T) {
	err := os.Setenv("GO_ENV", "test")
	if err != nil {
		assert.Equal(t, err.Error(), "done")
	}

	assert.Panics(t, func() { GetEnvFile() })
}

func TestConnectRedis(t *testing.T) {
	err := os.Setenv(redisURL, localURL)
	if err != nil {
		panic(err)
	}
	assert.Panics(t, func() { ConnectRedis() })
}
