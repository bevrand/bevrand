package main

import (
	"bytes"
	"encoding/json"
	"github.com/streadway/amqp"
	"math/rand"
	"net/http"
	"time"
)

var queueDrinks = true

// RandomizeHandler randomizes a drink and puts it on the queue
func RandomizeHandler(w http.ResponseWriter, r *http.Request) {
	var randomizeRequest RandomizeRequest
	randomizeRequest = r.Context().Value(ContextKey).(RandomizeRequest)

	randomizedDrink := randomizeList(randomizeRequest.Beverages)
	randomDrink := ResultModel{Result: randomizedDrink}
	queue := queueModel{
		randomizeRequest.Playlist, randomizeRequest.Username, randomizedDrink,
	}
	if queueDrinks{
		go queueDrink(queue)
	}
	ResponseWithJson(r.Context(), w, randomDrink)
}

// takes a slice and return a random value from that slice
func randomizeList(beverages []string) string {
	rand.Seed(time.Now().UnixNano())
	randomDrink := beverages[rand.Intn(len(beverages))]

	return randomDrink
}

func queueDrink(queueMessage queueModel) {
	ch, _ := rabbitConn.Channel()

	body := new(bytes.Buffer)
	err := json.NewEncoder(body).Encode(queueMessage)
	if err != nil {
		println("error")
	}

	defer ch.Close()

	q, _ := ch.QueueDeclare(
		"highscores", // name
		false,   // durable
		false,   // delete when unused
		false,   // exclusive
		false,   // no-wait
		nil,     // arguments
	)

	err = ch.Publish(
		"",     // exchange
		q.Name, // routing key
		false,  // mandatory
		false,  // immediate
		amqp.Publishing{
			ContentType: "application/json",
			Body:        []byte(body.Bytes()),
		})
	if err != nil {
		println(err)
	}
}
