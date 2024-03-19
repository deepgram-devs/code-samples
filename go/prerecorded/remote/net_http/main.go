package main

import (
	"fmt"
	"io"
	"net/http"
	"strings"
)

func main() {

	url := "https://api.deepgram.com/v1/listen"
	method := "POST"

	payload := strings.NewReader(`{"url":"https://dpgr.am/spacewalk.wav"}`)

	client := &http.Client{}
	req, err := http.NewRequest(method, url, payload)

	if err != nil {
		fmt.Println(err)
		return
	}
	req.Header.Add("Content-Type", "application/json")
	req.Header.Add("Authorization", "Token DEEPGRAM_API_KEY") // Replace with actual API key

	res, err := client.Do(req)
	if err != nil {
		fmt.Println(err)
		return
	}
	defer res.Body.Close()

	body, err := io.ReadAll(res.Body)
	if err != nil {
		fmt.Println(err)
		return
	}
	fmt.Println(string(body))
}
