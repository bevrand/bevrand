package models

// BeverageResult is the result of beverages when searching
type BeverageResult struct {
	Beverage `json:"beverage"`
}

type Beverage struct {
	Name    string `json:"name"`
	Perc    int    `json:"perc,omitempty"`
	Type    string `json:"type,omitempty"`
	Country string `json:"country,omitempty"`
}

type CocktailResult struct {
	Cocktail `json:"cocktail"`
}

type Cocktail struct {
	Name    string `json:"name"`
	Alcohol string `json:"alcohol,omitempty"`
}

// D3Response is the graph response
type D3BevGroupResponse struct {
	Nodes []Node `json:"nodes"`
}

type D3BeverageResponse struct {
	Nodes []BeverageNode `json:"nodes"`
}

// Node is the graph response node
type BeverageNode struct {
	Name    string `json:"name"`
	Perc    int    `json:"perc"`
	Type    string `json:"type"`
	Country string `json:"country,omitempty"`
}

type Node struct {
	Title string `json:"title"`
	Label string `json:"label"`
}
