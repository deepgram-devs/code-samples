## Speech-to-Text Conversion using Deepgram API with Go

**Title:** Converting Pre-recorded Remote Audio to Text using Go and Deepgram API

**Code Sample:** speech-to-text/prerecorded/remote/net_http/main.go

**Description:** This Go code sends a POST request to the Deepgram API to convert a pre-recorded audio file (spacewalk.wav) located at a remote URL into text. The response, which is the transcribed text, is then printed to the console.

### speech-to-text/prerecorded/remote/net_http/main.go

```go
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

```

## Speech-to-Text Conversion using Deepgram API and Go

**Title:** Converting Pre-recorded Audio to Text using Go and Deepgram API

**Code Sample:** speech-to-text/prerecorded/local/net_http/main.go

**Description:** This is a Go program that uses Deepgram's API to convert a pre-recorded audio file to text. It reads the audio file, sends it to the Deepgram API via an HTTP POST request, and prints the response.

### speech-to-text/prerecorded/local/net_http/main.go

```go
package main

import (
	"bytes"
	"fmt"
	"io"
	"net/http"
	"os"
)

func main() {
	url := "https://api.deepgram.com/v1/listen"

	file, err := os.Open("youraudio.wav") // Replace path with actual audio file path
	if err != nil {
		fmt.Println("Error opening file:", err)
		return
	}
	defer file.Close()

	body := &bytes.Buffer{}
	_, err = io.Copy(body, file)
	if err != nil {
		fmt.Println("Error reading file:", err)
		return
	}

	req, err := http.NewRequest("POST", url, body)
	if err != nil {
		fmt.Println("Error creating request:", err)
		return
	}

	req.Header.Set("Authorization", "Token DEEPGRAM_API_KEY") // Replace with actual API key
	req.Header.Set("Content-Type", "audio/wav")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("Error sending request:", err)
		return
	}
	defer resp.Body.Close()

	fmt.Println("Response status code:", resp.Status)

	var responseBody bytes.Buffer
	_, err = io.Copy(&responseBody, resp.Body)
	if err != nil {
		fmt.Println("Error reading response body:", err)
		return
	}
	fmt.Println("Response body:", responseBody.String())
}

```

## Streaming Speech-to-Text Conversion using Gorilla WebSocket and Deepgram API

**Title:** Real-time Speech-to-Text Conversion with WebSockets

**Code Sample:** speech-to-text/streaming/remote/gorilla-websocket/main.go

**Description:** This code establishes a WebSocket connection to the Deepgram API for real-time speech-to-text conversion. It streams audio data from a URL, decodes the JSON response, and prints the transcript. Gorilla WebSocket package is used for managing WebSocket connections.

### speech-to-text/streaming/remote/gorilla-websocket/main.go

```go
package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/gorilla/websocket"
)

const (
	authToken = "YOUR_DEEPGRAM_API_KEY" // Replace 'YOUR_DEEPGRAM_API_KEY' with your actual authorization token
	wsURL     = "wss://api.deepgram.com/v1/listen"
	audioURL  = "http://stream.live.vc.bbcmedia.co.uk/bbc_world_service"
)

type Response struct {
	Type    string `json:"type"`
	Channel struct {
		Alternatives []struct {
			Transcript string `json:"transcript"`
		} `json:"alternatives"`
	} `json:"channel"`
}

func main() {
	// Create HTTP headers with the authorization token
	headers := http.Header{}
	headers.Set("Authorization", "Token "+authToken)

	// Set up a channel to capture interrupt signals for graceful shutdown
	interrupt := make(chan os.Signal, 1)
	signal.Notify(interrupt, os.Interrupt, syscall.SIGTERM)

	// Establish a WebSocket connection to the Deepgram API
	conn, _, err := websocket.DefaultDialer.Dial(wsURL, headers)
	if err != nil {
		log.Fatal("Dial:", err)
	}
	defer conn.Close()

	// Create a channel to signal when the WebSocket connection is done
	done := make(chan struct{})

	// Start a goroutine to read messages from the WebSocket
	go func() {
		defer close(done)
		for {
			_, message, err := conn.ReadMessage()
			if err != nil {
				log.Println("Read:", err)
				return
			}
			var response Response
			if err := json.Unmarshal(message, &response); err != nil {
				log.Printf("Error decoding JSON message: %v", err)
				continue
			}
			if response.Type == "Results" && len(response.Channel.Alternatives) > 0 {
				transcript := response.Channel.Alternatives[0].Transcript
				if transcript != "" {
					fmt.Println("Transcript:", transcript)
				}
			}
		}
	}()

	// Start a goroutine to stream audio to the WebSocket
	go func() {
		if err := streamAudio(conn); err != nil {
			log.Printf("Error streaming audio: %v", err)
			conn.Close()
		}
	}()

	// Wait for interrupt signal to gracefully close the WebSocket connection
	for {
		select {
		case <-done:
			return
		case <-interrupt:
			log.Println("Interrupt received, closing connection")
			err := conn.WriteMessage(websocket.CloseMessage, websocket.FormatCloseMessage(websocket.CloseNormalClosure, ""))
			if err != nil {
				log.Println("Write close:", err)
				return
			}
			select {
			case <-done:
			case <-time.After(time.Second):
			}
			return
		}

	}
}

// streamAudio streams audio from a URL to the Deepgram API using a WebSocket connection
func streamAudio(conn *websocket.Conn) error {
	resp, err := http.Get(audioURL)
	if err != nil {
		return fmt.Errorf("failed to open audio stream: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("failed to open audio stream: status code %d", resp.StatusCode)
	}

	buf := make([]byte, 4096)
	for {
		n, err := resp.Body.Read(buf)
		if err != nil {
			if err == io.EOF {
				break
			}
			return fmt.Errorf("failed to read audio stream: %w", err)
		}
		if err := conn.WriteMessage(websocket.BinaryMessage, buf[:n]); err != nil {
			return fmt.Errorf("failed to send audio data: %w", err)
		}
	}
	return nil
}

```

## Text-to-Speech Conversion using Deepgram API

**Title:** Text-to-Speech Conversion in Go

**Code Sample:** text-to-speech/net_http/main.go

**Description:** This Go program uses the Deepgram API to convert a given text into speech. The output is saved as an MP3 file. The program makes an HTTP POST request with the text to be converted and writes the response to a file.

### text-to-speech/net_http/main.go

```go
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

```

