package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"
)

func main() {
	url := "https://api.deepgram.com/v1/speak?model=aura-asteria-en"
	apiKey := "DEEPGRAM_API_KEY" // Replace with actual API key
	payload := strings.NewReader(`{"text": "Hello, how can I help you today?"}`)

	client := &http.Client{}
	req, err := http.NewRequest("POST", url, payload)
	if err != nil {
		fmt.Println("Error creating request:", err)
		return
	}

	req.Header.Set("Authorization", "Token "+apiKey)
	req.Header.Set("Content-Type", "application/json")

	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("Error making request:", err)
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		fmt.Printf("HTTP error! Status: %d\n", resp.StatusCode)
		return
	}

	outputFile, err := os.Create("your_output_file.mp3")
	if err != nil {
		fmt.Println("Error creating output file:", err)
		return
	}
	defer outputFile.Close()

	_, err = io.Copy(outputFile, resp.Body)
	if err != nil {
		fmt.Println("Error copying response body:", err)
		return
	}

	fmt.Println("File saved successfully.")
}
