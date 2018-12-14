package models

import "gopkg.in/oauth2.v3/utils/uuid"

type ErrorModel struct {
	Message	string `json:"errorMessage"`
	UniqueCode uuid.UUID `json:"uniqueCode"`
}