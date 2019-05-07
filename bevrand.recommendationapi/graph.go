package main

import (
	"fmt"
	"io/ioutil"
	"os"
	bolt "github.com/johnnadratowski/golang-neo4j-bolt-driver"
)

// Creates the connection to neo4j
func CreateConnection() {
	var err error
	neo4jUrl := os.Getenv("NEO4J_URL")
	driver, err := bolt.NewDriverPool(neo4jUrl, 10)
	db, err = driver.OpenPool()
	handleError(err)
}

// Can be used to seed the database
func SeedDataBaseOnStartUp() {
	b, err := ioutil.ReadFile("cypher/beverages.cypher")
	if err != nil {
		fmt.Print(err)
	}

	createNode := string(b) // convert content to a 'string'
	st := prepareStatement(createNode)
	executeStatement(st)
}

//we prepare a query to be executed
func prepareStatement(query string) bolt.Stmt {
	st, err := db.PrepareNeo(query)
	handleError(err)
	return st
}

// Executing a statement just returns summary information
func executeStatement(st bolt.Stmt) {
	result, err := st.ExecNeo(map[string]interface{}{"name": "Whiskey"})
	handleError(err)
	numResult, err := result.RowsAffected()
	handleError(err)
	fmt.Printf("CREATED ROWS: %d\n", numResult) // print the number of created rows

	// Closing the statement will also close the rows
	st.Close()
}
