## Real-Time Speech-to-Text Conversion with Deepgram API using WebSockets

**Title:** Real-Time Speech-to-Text Conversion

**Code Sample:** speech-to-text/streaming/threading/main.py

**Description:** This Python script uses the Deepgram API to convert real-time audio stream from a URL into text transcripts. It uses WebSocketApp from the websocket library to establish a WebSocket connection with Deepgram's 'listen' endpoint. The audio stream is fetched using the requests library and sent to the WebSocket in chunks. The received messages from the WebSocket are then processed to extract the transcripts. Threading is used to handle the audio streaming concurrently with the WebSocket connection.

### speech-to-text/streaming/threading/main.py

```python
from websocket import WebSocketApp
import websocket
import json
import threading
import requests

auth_token = "YOUR_DEEPGRAM_API_KEY"  # Replace 'DEEPGRAM_API_KEY' with your actual authorization token
headers = {
    "Authorization": f"Token {auth_token}"
}

# WebSocket URL
ws_url = "wss://api.deepgram.com/v1/listen"

# Audio stream URL
audio_url = "http://stream.live.vc.bbcmedia.co.uk/bbc_world_service"

# Define the WebSocket functions on_open, on_message, on_close, and on_error
def on_open(ws):
    print("WebSocket connection established.")
    
    # Start audio streaming thread
    audio_thread = threading.Thread(target=stream_audio, args=(ws,))
    audio_thread.daemon = True
    audio_thread.start()

def on_message(ws, message):
    try:
      response = json.loads(message)
      if response.get("type") == "Results":
          transcript = response["channel"]["alternatives"][0].get("transcript", "")
          if transcript:
              print("Transcript:", transcript)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON message: {e}")
    except KeyError as e:
        print(f"Key error: {e}")

def on_close(ws, close_status_code, close_msg):
    print(f"WebSocket connection closed with code: {close_status_code}, message: {close_msg}")

def on_error(ws, error):
    print("WebSocket error:", error)

# Define the function to stream audio to the WebSocket
def stream_audio(ws):
    response = requests.get(audio_url, stream=True)
    if response.status_code == 200:
        print("Audio stream opened.")
        for chunk in response.iter_content(chunk_size=4096):
            ws.send(chunk, opcode=websocket.ABNF.OPCODE_BINARY)
    else:
        print("Failed to open audio stream:", response.status_code)

# Create WebSocket connection
ws = WebSocketApp(ws_url, on_open=on_open, on_message=on_message, on_close=on_close, on_error=on_error, header=headers)

# Run the WebSocket
ws.run_forever()

```

## Real-time Speech-to-Text Conversion using Deepgram WebSocket API

**Title:** Real-time Speech-to-Text Conversion

**Code Sample:** speech-to-text/streaming/asyncio/main.py

**Description:** This Python script uses the asyncio and aiohttp libraries to establish a WebSocket connection with the Deepgram API. It streams audio from a live BBC radio broadcast and sends it to the Deepgram API for real-time transcription. The transcriptions are then printed to the console.

### speech-to-text/streaming/asyncio/main.py

```python
import asyncio
import aiohttp
import json

api_key = "YOUR_DEEPGRAM_API_KEY"
headers = {
    "Authorization": f"Token {api_key}",
}

# URL for Deepgram WebSocket API
deepgram_ws_url = "wss://api.deepgram.com/v1/listen"
# URL for the remote audio stream
audio_stream_url = "http://stream.live.vc.bbcmedia.co.uk/bbc_world_service"

async def stream_audio_to_websocket():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(deepgram_ws_url, headers=headers) as ws:
            print("WebSocket connection established.")

            async def send_audio_stream():
                try:
                    async with session.get(audio_stream_url) as response:
                        async for chunk in response.content.iter_chunked(4096):
                            if chunk:
                                await ws.send_bytes(chunk)
                    print("Audio stream ended.")
                except aiohttp.ClientError as error:
                    print(f"Error fetching audio stream: {error}")

            async def receive_transcripts():
                try:
                    async for message in ws:
                        try:
                            response = json.loads(message.data)
                            if response.get("type") == "Results":
                                transcript = response["channel"]["alternatives"][0].get("transcript", "")
                                if transcript:
                                    print("Transcript:", transcript)
                        except json.JSONDecodeError as e:
                            print(f"Error decoding JSON message: {e}")
                        except KeyError as e:
                            print(f"Key error: {e}")
                except Exception as e:
                    print(f"WebSocket error: {e}")

            await asyncio.gather(send_audio_stream(), receive_transcripts())
            await close_websocket(ws)

async def close_websocket(ws):
    close_msg = '{"type": "CloseStream"}'
    await ws.send_str(close_msg)
    await ws.close()

def main():
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(stream_audio_to_websocket())
    except KeyboardInterrupt:
        print("Process interrupted. Closing WebSocket connection.")
        loop.run_until_complete(close_websocket())

if __name__ == "__main__":
    main()

```

## Speech-to-Text Conversion using Deepgram API

**Title:** Converting Pre-recorded Local Audio to Text with Deepgram API

**Code Sample:** speech-to-text/prerecorded/local/requests/main.py

**Description:** This script uses the Deepgram API to convert a pre-recorded local audio file to text. It sends a POST request with the audio file to the Deepgram API endpoint and prints the response in JSON format.

### speech-to-text/prerecorded/local/requests/main.py

```python
import requests

# Define the URL for the Deepgram API endpoint
url = "https://api.deepgram.com/v1/listen"

# Define the headers for the HTTP request
headers = {
    "Authorization": "Token YOUR_DEEPGRAM_API_KEY",
    "Content-Type": "audio/*"
}

# Get the audio file
with open("/path/to/youraudio.wav", "rb") as audio_file:
    # Make the HTTP request
    response = requests.post(url, headers=headers, data=audio_file)

print(response.json())
```

## Speech-to-Text Conversion using Deepgram API with Local Audio Files

**Title:** Converting Local Audio Files to Text with Deepgram API

**Code Sample:** speech-to-text/prerecorded/local/http-client/main.py

**Description:** This Python script uses the Deepgram API to convert a local audio file to text. It reads the audio file as binary data, sends it to the Deepgram API via a POST request, and prints the response. The Deepgram API key and audio file path are required inputs.

### speech-to-text/prerecorded/local/http-client/main.py

```python
import http.client
import json

# Define the URL for the Deepgram API endpoint
url = "api.deepgram.com"

# Define the path to the audio file
audio_file_path = "/path/to/youraudio.wav"  # Replace with the path to your audio file

# Read the audio file as binary data
with open(audio_file_path, "rb") as audio_file:
  audio_data = audio_file.read()

# Define request headers
headers = {
    "Authorization":
    "Token YOUR_DEEPGRAM_API_KEY",  # Replace with your Deepgram API key
    "Content-Type": "audio/*"
}

# Create a connection to the API endpoint
conn = http.client.HTTPSConnection(url)

# Define the request body
body = audio_data

# Send the POST request
conn.request("POST", "/v1/listen", body, headers)

# Get the response
response = conn.getresponse()

# Read and print the response data
response_data = response.read()
print(json.loads(response_data))

# Close the connection
conn.close()

```

## Speech-to-Text Conversion using Deepgram API

**Title:** Converting Pre-recorded Remote Audio to Text with Deepgram API

**Code Sample:** speech-to-text/prerecorded/remote/requests/main.py

**Description:** This code uses the Deepgram API to convert a pre-recorded remote audio file (spacewalk.wav) into text. It sends a HTTP request with necessary headers and data, and prints the response in JSON format.

### speech-to-text/prerecorded/remote/requests/main.py

```python
import requests

# Define the URL for the Deepgram API endpoint
url = "https://api.deepgram.com/v1/listen"

# Define the headers for the HTTP request
headers = {
    "Accept": "application/json",
    "Authorization": "Token YOUR_API_KEY",
    "Content-Type": "application/json"
}
# Define the data for the HTTP request
data = {"url": "https://dpgr.am/spacewalk.wav"}

# Make the HTTP request
response = requests.post(url, headers=headers, json=data)

print(response.json())
```

## Speech-to-Text Conversion using Deepgram API

**Title:** Converting Pre-recorded Remote Audio to Text using HTTP Client in Python

**Code Sample:** speech-to-text/prerecorded/remote/http-client/main.py

**Description:** This Python script uses the http.client library to send a POST request to the Deepgram API, converting a pre-recorded audio file (spacewalk.wav) hosted remotely into text. The output is then printed to the console.

### speech-to-text/prerecorded/remote/http-client/main.py

```python
import http.client
import json

# Create the connection
conn = http.client.HTTPSConnection("api.deepgram.com")

# Define the payload for the HTTP request
payload = json.dumps({"url": "https://dpgr.am/spacewalk.wav"})

# Define the headers for the HTTP request
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Token YOUR_API_KEY'
}

# Make the HTTP request
conn.request("POST", "/v1/listen", payload, headers)

# Get the response from the HTTP request
res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
```

## Text-to-Speech Conversion Using Deepgram API

**Title:** Converting Text to Speech using Deepgram API

**Code Sample:** text-to-speech/requests/main.py

**Description:** This Python script uses the Deepgram API to convert a text string ("Hello, how can I help you today?") into speech. The resulting audio is saved as an MP3 file. The script uses the requests library to send a POST request, including the necessary headers and payload, to the Deepgram API.

### text-to-speech/requests/main.py

```python
import requests

url = "https://api.deepgram.com/v1/speak?model=aura-asteria-en"
headers = {
    "Authorization": "Token DEEPGRAM_API_KEY", # Replace with your Deepgram API key
    "Content-Type": "application/json"
}
payload = {
    "text": "Hello, how can I help you today?"
}

response = requests.post(url, headers=headers, json=payload)

if response.status_code == 200:
    with open("your_output_file.mp3", "wb") as f:
        f.write(response.content)
    print("File saved successfully.")
else:
    print(f"Error: {response.status_code} - {response.text}")

```

## Text-to-Speech Conversion using Deepgram API

**Title:** Converting Text to Speech using Deepgram API and Python's http.client

**Code Sample:** text-to-speech/http-client/main.py

**Description:** This Python script uses the Deepgram API to convert a given text into speech. The output is saved as an mp3 file. The http.client library is used to make a POST request to the API.

### text-to-speech/http-client/main.py

```python
import http.client
import json

url = "api.deepgram.com"
request_body = json.dumps({"text": "Hello, how can I help you today?"})
headers = {
    "Authorization": "Token YOUR_DEEPGRAM_API_KEY",  # Replace with your Deepgram API key
    "Content-Type": "application/json"
}

conn = http.client.HTTPSConnection(url)

conn.request("POST", "/v1/speak?model=aura-asteria-en", request_body, headers)

response = conn.getresponse()

output_file_path = "your_output_file.mp3"
with open(output_file_path, "wb") as output_file:
    output_file.write(response.read())

conn.close()

print("File saved successfully at:", output_file_path)

```

