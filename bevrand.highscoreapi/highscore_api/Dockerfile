FROM golang:1.10
ADD . /go/src/app
WORKDIR /go/src/app
RUN go get app
RUN go install
RUN go build -o main
CMD ["go/src/app/main"]


