package models

// BeverageResult is the result of beverages when searching
type BeverageResult struct {
	Beverage `json:"beverage"`
}

// Beverage is the main type of beverage stored in Neo
type Beverage struct {
	Name    string `json:"name"`
	Perc    int    `json:"perc,omitempty"`
	Type    string `json:"type,omitempty"`
	Country string `json:"country,omitempty"`
}

// CocktailResult is the parent of Cocktail
type CocktailResult struct {
	Cocktail `json:"cocktail"`
}

// Cocktail is the main type of cocktail stored in Neo
type Cocktail struct {
	Name    string `json:"name"`
	Alcohol string `json:"alcohol,omitempty"`
}

// D3BevGroupResponse is the graph response
type D3BevGroupResponse struct {
	Nodes []Node `json:"nodes"`
}

// D3BeverageResponse is the graph response
type D3BeverageResponse struct {
	Nodes []BeverageNode `json:"nodes"`
}

// BeverageNode is the graph response node
type BeverageNode struct {
	Name    string `json:"name"`
	Perc    int    `json:"perc"`
	Type    string `json:"type"`
	Country string `json:"country,omitempty"`
}

// Node is the graph response node
type Node struct {
	Title string `json:"title"`
	Label string `json:"label"`
}
