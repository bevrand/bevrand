<h1>Recommendation Api</h1>

<h2>Introduction</h2>

The recommendation api uses a graph database (neo4j) to keep track of
drinks and categories that can be used to recommend drinks to users.

<h2>Routes</h2>

<h3>Local:</h3>

**localhost:4590/**

<h3>Docker:</h3>

**recommendationapi:5000/**
    
    Health check:
    GET /ping
    
    Groups:
    GET /api/v1/beveragroups/ -> all groups
    
    Categories:
    GET /api/v1/categories -> all categories
    GET /api/v1/categories?kind=beer -> specific categories
    
    Beverages:
    GET /api/v1/beverages -> all beverages with metadata
    Example:
    [
        {
            "beverage": {
            "name": "Rye Whiskey",
            "perc": 40,
            "type": "Alcoholic",
            "country": "American"
            }
        },
        {
            "beverage": {
            "name": "Bourbon",
            "perc": 40,
            "type": "Alcoholic",
            "country": "American"
            }
        }
    ]
    
    GET /api/v1/beverages?limit=5 -> all beverages with metadata
    
    Cocktails:
    You can include 2 and exclude 1 drink from your query. Exclude is optional
    GET /api/v1/cocktails?include=vodka
    GET /api/v1/cocktails?include=vodka&exclude=gin 
    GET /api/v1/cocktails?include=gin&include=vodka&exclude=rum



<h2>Testing</h2>

go test -v -cover

<h3>Coverage:</h3>

go test -covermode=count -coverprofile=count.out

go tool cover -html=count.out