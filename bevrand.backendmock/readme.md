To start the mock you first need to install a few dependencies (first time only).
You can do so by using: go get -u all
If that fails just install the three packages included:

go get -u github.com/gorilla/mux
go get -u github.com/urfave/negroni
go get -u github.com/rs/cors

To start the server itself (from the folder bevrand.backendmock):
go run server.go

The following routes are included:
GET:
http://0.0.0.0/4540/api/redis*
http://0.0.0.0/4540/api/frontpage

POST:
http://0.0.0.0/4540/api/randomize

To start the react app (from the folder bevrand.reactapp)

npm install
npm start

This starts the development server on port 3000