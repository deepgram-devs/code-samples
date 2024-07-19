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
