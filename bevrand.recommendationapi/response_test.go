package recommendation

import (
	"github.com/stretchr/testify/assert"
	"testing"
)

func TestCreateGuid(t *testing.T) {
	guid := createGUID()
	assert.Len(t, guid, 36)
}
