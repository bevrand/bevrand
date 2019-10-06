package main

// Model for queueing to the highscore api
type queueModel struct {
	Playlist string `json:"playlist"`
	Username string `json:"username"`
	Result string `json:"result"`
}

// Model to put on the queue
type ResultModel struct {
	Result string `json:"result"`
}

// Request model
type RandomizeRequest struct {
	Beverages []string `json:"beverages"`
	Playlist string `json:"list"`
	Username string `json:"user"`
}

// ErrorModel is the base model used for handling errors
type ErrorModel struct {
	UniqueCode string `json:"uniqueCode"`
}

// messages used in validation error
type ValidationMessages struct {
	Field    string `json:"validationField"`
	Message    string `json:"validationMessage"`
}

// validation errors occur when data is malformed
type ValidationError struct {
	ErrorModel
	Messages   []ValidationMessages `json:"errorModel"`
}

//  messages used in method error
type MethodMessages struct {
	Methods    string `json:"allowedMethods"`
	Message    string `json:"methodError"`
}

// method errors occur when calling endpoints with an unallowed method
type MethodError struct {
	ErrorModel
	Messages   []MethodMessages `json:"errorModel"`
}
