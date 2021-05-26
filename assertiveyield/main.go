package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"sync"
	"time"
)


type HTTPBody struct {
	Id string
	X int
	Y float32
}

func main() {

	var ids []string
	// could be split into read/write locks
	lock := sync.Mutex{}

	go func() {
		var newIds []string
		for {
			resp, err := http.Get("https://dubbelboer.com/ay/entities.json")
			if err != nil {
				panic(err)
			}
			dec := json.NewDecoder(resp.Body)
			err = dec.Decode(&newIds)
			if err != nil {
				panic(err)
			}
			lock.Lock()
			ids = newIds
			lock.Unlock()

			time.Sleep(time.Second)
		}
	}()

	//fmt.Printf("Ids : %+v", ids)


	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		dec := json.NewDecoder(r.Body)
		var parsed HTTPBody
		dec.Decode(&parsed)
		fmt.Print(parsed)

		lock.Lock()
		defer lock.Unlock()
		for _, i := range ids {
			if i == parsed.Id {
				w.WriteHeader(200)
				return
			}
		}
		w.WriteHeader(404)
	})
	log.Fatal(http.ListenAndServe(":8080", nil))

}
