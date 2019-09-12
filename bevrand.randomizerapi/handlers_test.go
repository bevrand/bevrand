package main

import (
	"github.com/stretchr/testify/assert"
	"testing"
)

func TestRandomizeList(t *testing.T) {
	drinks := []string{"Beer", "Wine"}
	result := randomizeList(drinks)
	assert.Contains(t, drinks, result)
}
