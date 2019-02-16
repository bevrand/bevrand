FROM golang:1.11.5-alpine3.8 as build-env

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
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -a -installsuffix cgo -o highscoreapi

# STEP 2 copy to a small image
FROM alpine:3.9

# Create a group and user
RUN addgroup --system --gid 4580 appgroup \
&& adduser --system -u 4580 --ingroup appgroup --shell /bin/sh appuser

RUN apk --no-cache add ca-certificates
COPY --from=build-env /app/highscoreapi /
COPY --from=build-env /app/.env.docker /

# Make app directory content read-only (dotnet is executed, not program)
RUN chown 4580:4580 /highscoreapi &&  chown -R 4580:4580 /.env.docker && chmod 0500 /highscoreapi && chmod 0400 /.env.docker
# Drop user
USER appuser

CMD ["/highscoreapi"]