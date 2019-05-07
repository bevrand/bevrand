FROM golang:1.11.9-alpine3.8 as build-env

#STEP 1 build the image
RUN apk --no-cache add git
ENV GO111MODULE=on
RUN mkdir /app
WORKDIR /app
COPY go.mod .
COPY go.sum .

# Get dependenciesgo
RUN go mod download
# COPY the source code as the last step
COPY . .

# Build the binary
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -a -installsuffix cgo -o recommendationapi

# STEP 2 copy to a small image
FROM alpine:3.9
RUN apk --no-cache add ca-certificates
COPY --from=build-env /app/recommendationapi /
CMD ["/recommendationapi"]