<h1>Highscore Api</h1>

<h2>Introduction</h2>

The highscore api keeps track of user and global highscores.

It uses Redis for storing keys and these are incremented by the randomizerapi.

In the long run this might be connected using a queue but for now we use a 
simple http request. Traces are logged to jaeger for further inspection.

<h2>Routes</h2>

<h3>Local:</h3>

**localhost:4580/**

<h3>Docker:</h3>

**highscoreapi:5000/**
    
    Health check:
    GET /ping
    
    Redis related:
    GET /api/v1/highscores/ -> global highscore
    GET /api/v1/highscores/<username>/<playList>/ -> user related highscore
    
    Examples:
    
    /api/v1/highscores/marvin/paranoid/
    /api/v1/highscores/frontpage/tgif/
    
    POST /api/v1/highscores/<username>/<playList>/ -> increase highscore 
    (also increases globalcount)
    
    /api/v1/highscores/frontpage/tgif/
    Body:
    { 
        "drink" : "beer"
    }


<h2>Testing</h2>

go test -v -cover

<h3>Coverage:</h3>

go test -covermode=count -coverprofile=count.out

go tool cover -html=count.out