FROM golang:1.11.5-alpine3.8 as build-env

#STEP 1 build the image
RUN apk --no-cache add git
ENV GO111MODULE=on
RUN mkdir /app
WORKDIR /app

# Create a group and user
RUN addgroup --system --gid 4580 appgroup \
&& adduser --system -u 4580 --ingroup d --shell /bin/sh appuser

COPY go.mod .
COPY go.sum .

# Get dependenciesgo
RUN go mod download
# COPY the source code as the last step
COPY . .

# Build the binary
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-w -s" -a -installsuffix cgo -o highscoreapi

# Make app directory content read-only, except for go executable
RUN chown -R 4580:4580 /app/ && chmod -R u-x+X,go-rwx /app/ && chmod u+x /app/highscoreapi

#Based on https://medium.com/@chemidy/create-the-smallest-and-secured-golang-docker-image-based-on-scratch-4752223b7324
# STEP 2 copy to a small image
FROM scratch

# Copy application and settings
COPY --from=build-env /app/highscoreapi /app/
COPY --from=build-env /app/.env.docker /

# Set sane defaults
ENV GO_ENV=docker
ENV GIN_MODE=release

# Drop user
USER 4580:4580

CMD ["/app/highscoreapi"]