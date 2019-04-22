# Proxy-Api documentation

The proxy-api aims to provide a gateway to the different microservices of the Beverage Randomizer. It reroutes requests to the appropriate services and validates credentials for protected routes.

## Routes

Protected routes should be called with a x-api-token header, that should contain a valid JWT token, issued by the login route.

|                   | path                           | Protected | Methods             |
| ----------------- | ------------------------------ | --------- | ------------------- |
| Login             | `/authentication-api/login`    | false     | POST                |
| Register          | `/authentication-api/register` | false     | POST                |
| Highscore         | `/highscore-api/v1/highscores` | false     | GET                 |
| Frontpage         | `/playlist-api/v2/frontpage`   | false     | GET                 |
| Private playlists | `/playlist-api/v1/private`     | true      | GET,POST,PUT,DELETE |
| Randomize         | `/randomize-api/v2/randomize`  | false     | POST                |

## Getting Started

Installing dependencies:

    npm install

Starting the application:

    npm start

Since the application acts as a proxy/gateway to the other microservices, it needs these microservices in order to run succesfully.

## Configuration

The proxy-api will try to read configuration from environment variables. An .env file can be used to set these environment variables. The application will
| Variable name |Description  
|-----------------|---------------------------
|PLAYLIST_API |Endpoint of the playlist api  
|RANDOMIZER_API | Endpoint of the randomizer api  
|AUTHENTICATION_API | Endpoint of the authentication api  
|HIGHSCORE_API | Endpoint of the highscore api
|AUTHENTICATION_SECRET | Authentication secret, used to generate unique tokens  
|AUTHENTICATION_EXPIRATION_TIME| Expiration time for the authentication token  
|FRONTEND_JWT_SECRET |Secret that will be used to sign playlist objects
| PORT | Port at which the application will run, defaults to 5000
| NODE_ENV | Node environemtn to use
|DEFAULT_FRONTPAGE_LIST| Default frontpage list to pick when retrieving them
|JAEGER_AGENT_HOST| Address at which the Jaeger Host will run
| JAEGER_AGENT_PORT | Port which will be used by the Jaeger agent

## Folder structure

TODO
