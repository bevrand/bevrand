package models

type ErrorModel struct {
	Message	string `json:"errorMessage"`
	UniqueCode string `json:"uniqueCode"`
}