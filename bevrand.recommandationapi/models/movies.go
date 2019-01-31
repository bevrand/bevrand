package models

// MovieResult is the result of moves when searching
type MovieResult struct {
	Movie `json:"movie"`
}

// Movie is a movie
type Movie struct {
	Released int      `json:"released"`
	Title    string   `json:"title,omitempty"`
	Tagline  string   `json:"tagline,omitempty"`
	Cast     []Person `json:"cast,omitempty"`
}

// Person is a person in a movie
type Person struct {
	Job  string   `json:"job"`
	Role []string `json:"role"`
	Name string   `json:"name"`
}

// D3Response is the graph response
type D3Response struct {
	Nodes []Node `json:"nodes"`
	Links []Link `json:"links"`
}

// Node is the graph response node
type Node struct {
	Title string `json:"title"`
	Label string `json:"label"`
}

// Link is the graph response link
type Link struct {
	Source int `json:"source"`
	Target int `json:"target"`
}
