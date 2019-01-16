package main

type ErrorModel struct {
	Message	string `json:"errorMessage"`
	UniqueCode string `json:"uniqueCode"`
}

type PostObject struct {
	Drink	string `json:"drink"`
}

type Score struct {
	Drink	string `json:"drink"`
	Rolled int `json:"rolled"`
}