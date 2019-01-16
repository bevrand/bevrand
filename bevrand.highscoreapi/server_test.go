package main

import (
	"testing"
)

func TestInitJaeger(t *testing.T){
	expectedName := "testjaeger"
	tracer, _ := InitJaeger(expectedName, "localhost:4570")

	if tracer == nil {
		t.Errorf("tracer not returned")
	}
}

