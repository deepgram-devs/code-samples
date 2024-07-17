**Title:** Speech-to-Text Conversion with Local Audio File using Deepgram API
**Code Sample:** speech-to-text/prerecorded/local/net_http/main.go

**Description:** This Go program uses the Deepgram API to convert a locally stored audio file into text. It opens the audio file, sends it to the Deepgram API, and prints out the text response.

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

**Title:** Speech-to-Text Conversion with Remote Audio File using Deepgram API

**Code Sample:** speech-to-text/prerecorded/remote/net_http/main.go

**Description:** This Go program uses the Deepgram API to convert speech to text from a remotely stored audio file. It sends a POST request with the URL of the audio file as payload, and prints the response from the API, which is the transcribed text.

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

**Title:** Text-to-Speech Conversion using Deepgram API
**Code Sample:** text-to-speech/net_http/main.go

**Description:** This Go code snippet uses the Deepgram API to convert a text string to speech. It sends a POST request to the Deepgram API with the text to be converted. If the request is successful, it saves the response, which is an MP3 file of the spoken text, to the local system.

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

