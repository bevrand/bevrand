package recommendation

import (
	"github.com/stretchr/testify/assert"
	"os"
	"testing"
)

const neo4jURL = "bolt://neo4j:anewpassthatishard@localhost:7687"

func TestEnvSetting(t *testing.T) {
	err := os.Setenv("GO_ENV", "")
	if err != nil {
		assert.Fail(t, err.Error(), "Failed setting env")
	}

	getEnvFile()
	expectedURL := os.Getenv("NEO4J_URL")

	assert.Equal(t, neo4jURL, expectedURL)
}
