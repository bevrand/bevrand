package main

import (
	"github.com/stretchr/testify/assert"
	"os"
	"testing"
)

func TestEnvSetting(t *testing.T) {
	env := os.Getenv("GO_ENV")

	assert.Equal(t, "development", env)
	neoURL := os.Getenv("NEO4J_URL")
	assert.Equal(t, "bolt://testuser:testuser@localhost:7687", neoURL)
}
