package main

// ErrorModel is the model used for handling errors
type ErrorModel struct {
	Message    string `json:"errorMessage"`
	UniqueCode string `json:"uniqueCode"`
}

// PostObject struct for the increase of drinks
type PostObject struct {
	Drink string `json:"drink"`
}

type HighScoreObject struct {
	Playlist string `json:"playlist"`
	Username string `json:"username"`
	Result string `json:"result"`
}

// Score is the return struct for highscores
type Score struct {
	Drink  string `json:"drink"`
	Rolled int    `json:"rolled"`
}
