package main

// ErrorModel is the model used for handling errors
type ErrorModel struct {
	Message    string `json:"errorMessage"`
	UniqueCode string `json:"uniqueCode"`
}
