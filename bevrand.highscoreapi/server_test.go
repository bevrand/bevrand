package main

import (
	"github.com/stretchr/testify/assert"
	"os"
	"testing"
)

func TestGetEmptyEnvFile(t *testing.T) {
	err := os.Setenv("GO_ENV", "")
	if err != nil {
		assert.Fail(t, err.Error(), "Failed setting env")
	}
	GetEnvFile()
	redisURL := os.Getenv("REDIS_URL")
	expectedURL := "localhost"

	assert.Equal(t, expectedURL, redisURL)
}

func TestGetBadEnvFile(t *testing.T) {
	err := os.Setenv("GO_ENV", "test")
	if err != nil {
		assert.Equal(t, err.Error(), "done")
	}

	assert.Panics(t, func() { GetEnvFile() })
}

func TestConnectRedis(t *testing.T) {
	err := os.Setenv("REDIS_URL", "localhost")
	if err != nil {
		panic(err)
	}
	assert.Panics(t, func() { ConnectRedis() })
}