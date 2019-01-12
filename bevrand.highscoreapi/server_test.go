package main

import (
	"fmt"
	"testing"
	"context"
	)

func TestInitJaeger(t *testing.T){
	expectedName := "testjaeger"
	tracer, _ := InitJaeger(expectedName, "localhost:4570")
	if tracer == nil {
		t.Errorf("tracer not returned")
	}
}

func TestInitRoutes(t *testing.T) {
	routes := InitRoutes()
	if routes == nil {
		t.Errorf("routes not returned")
	}
}

func TestPrintServerInfo(t *testing.T) {
	logValue := fmt.Sprintf("Starting server for HighScores!")
	ctx := context.Background()
	PrintServerInfo(ctx, logValue)
}