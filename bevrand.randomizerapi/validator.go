package main

import (
	"errors"
	"strconv"
)

const beverageField = "beverages"
const usernameField = "username"
const playlistField = "playlist"

func ValidateRequest(request RandomizeRequest) (ValidationError, error) {
	var validationError ValidationError
	validationError.UniqueCode = CreateGUID()

	err := validateUsername(request.Username)
	if err != nil {
		tempErr := ValidationMessages{err.Field, err.Message}
		validationError.Messages = append(validationError.Messages, tempErr)
	}
	err = validatePlaylist(request.Playlist)
	if err != nil {
		tempErr := ValidationMessages{err.Field, err.Message}
		validationError.Messages = append(validationError.Messages, tempErr)
	}
	err = validateBeverages(request.Beverages)
	if err != nil {
		tempErr := ValidationMessages{err.Field, err.Message}
		validationError.Messages = append(validationError.Messages, tempErr)
	}

	if len(validationError.Messages) > 0 {
		return validationError, errors.New("error in validation")
	}
	return validationError, nil
}

func validateUsername(username string) *ValidationMessages {
	valid := username != "" && len(username) >= 2
	if !valid {
		return &ValidationMessages{usernameField, "username " + username + " is too short or empty"}
	}
	return nil
}

func validatePlaylist(playlist string) *ValidationMessages {
	valid := playlist != "" && len(playlist) >= 2
	if !valid {
		return &ValidationMessages{playlistField, "playlist " + playlist + " is too short or empty"}
	}
	return nil
}

func validateBeverages(beverages []string) *ValidationMessages {
	valid := len(beverages) >= 2
	if !valid {
		return &ValidationMessages{beverageField, "beveragelist length " + strconv.Itoa(len(beverages)) + " is too short"}
	}
	return nil
}
