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

## Voice Agent Conversion using Deepgram API

**Title:**  Take audio from an input source and play the resulting agent audio

**Code Sample:** voice-agent/voice-agent-play-audio/main.py

**Description:** This Python script uses the Deepgram API to take audio from an input source and play the resulting agent audio on the selected output device.

### voice-agent/voice-agent-play-audio/main.py

```python

import pyaudio
import asyncio
import sys
import os
import json
import inspect
import queue

import threading
from typing import Optional, Callable, Union

from websockets.sync.client import ClientConnection as SyncClientConnection

from websockets.sync.client import connect

TIMEOUT = 0.050
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 8000

def main():
    try:
        dg_api_key = os.environ.get("DEEPGRAM_API_KEY")
        if dg_api_key is None:
            print("DEEPGRAM_API_KEY env var not present")
            return

        print("\n\n\nPress Enter to stop...\n\n\n")

        _socket = connect(
            "wss://agent.deepgram.com/agent",
            additional_headers={"Authorization": f"Token {dg_api_key}"},
        )

        _config_message = {
            "type": "SettingsConfiguration",
            "audio": {
                "input": {
                    "encoding": "linear16",
                    "sample_rate": RATE,
                },
                "output": {
                    "encoding": "linear16",
                    "sample_rate": RATE,
                    "container": "none",
                },
            },
            "agent": {
                "listen": {"model": "nova-2"},
                "think": {
                    "provider": {
                        "type": "open_ai",  # examples are anthropic, open_ai, groq, ollama
                    },
                    "model": "gpt-4o-mini",  # examples are claude-3-haiku-20240307, gpt-3.5-turbo, mixtral-8x7b-32768, mistral
                    "instructions": "You are a helpful AI assistant.",
                },
                "speak": {"model": "aura-athena-en"},
            },
        }

        _socket.send(json.dumps(_config_message))

        speaker = Speaker()
        speaker.start(_socket)

        microphone = Microphone(push_callback=_socket.send)
        microphone.start()

        input()

        print("Stopping microphone...")
        microphone.stop()

        print("Stopping speaker...")
        speaker.stop()

        print("Closing socket...")
        _socket.close()
        _socket = None

    except Exception as e:
        print(f"main: {e}")

class Microphone:
    _audio: pyaudio.PyAudio
    _chunk: int
    _rate: int
    _format: int
    _channels: int
    _input_device_index: Optional[int]
    _is_muted: bool

    _stream: pyaudio.Stream
    _asyncio_loop: asyncio.AbstractEventLoop
    _asyncio_thread: threading.Thread
    _exit: threading.Event

    _push_callback_org: object
    _push_callback: object

    def __init__(
        self,
        push_callback: Optional[Callable] = None,
        rate: Optional[int] = RATE,
        chunk: Optional[int] = CHUNK,
        channels: Optional[int] = CHANNELS,
        input_device_index: Optional[int] = None,
    ):
        self._exit = threading.Event()

        self._audio = pyaudio.PyAudio()
        self._chunk = chunk
        self._rate = rate
        self._format = FORMAT
        self._channels = channels
        self._is_muted = False

        self._input_device_index = input_device_index
        self._push_callback_org = push_callback

    def _start_asyncio_loop(self) -> None:
        self._asyncio_loop = asyncio.new_event_loop()
        self._asyncio_loop.run_forever()

    def is_active(self) -> bool:
        if self._stream is None:
            return False

        val = self._stream.is_active()
        return val

    def set_callback(self, push_callback: Callable) -> None:
        self._push_callback_org = push_callback

    def start(self) -> bool:
        if self._push_callback_org is None:
            return False

        if inspect.iscoroutinefunction(self._push_callback_org):
            self._asyncio_thread = threading.Thread(target=self._start_asyncio_loop)
            self._asyncio_thread.start()

            self._push_callback = lambda data: asyncio.run_coroutine_threadsafe(
                self._push_callback_org(data), self._asyncio_loop
            ).result()
        else:
            self._push_callback = self._push_callback_org

        self._stream = self._audio.open(
            format=self._format,
            channels=self._channels,
            rate=self._rate,
            input=True,
            output=False,
            frames_per_buffer=self._chunk,
            input_device_index=self._input_device_index,
            stream_callback=self._callback,
        )

        self._exit.clear()
        self._stream.start_stream()

        return True

    def _callback(self, input_data, frame_count, time_info, status_flags):
        if self._exit.is_set():
            return None, pyaudio.paAbort

        if input_data is None:
            return None, pyaudio.paContinue

        try:
            if self._is_muted:
                size = len(input_data)
                input_data = b"\x00" * size

            self._push_callback(input_data)
        except Exception as e:
            raise

        return input_data, pyaudio.paContinue

    def mute(self) -> bool:
        if self._stream is None:
            return False

        self._is_muted = True

        return True

    def unmute(self) -> bool:
        if self._stream is None:
            return False

        self._is_muted = False

        return True

    def stop(self) -> bool:
        self._exit.set()

        if self._stream is not None:
            self._stream.stop_stream()
            self._stream.close()
            self._stream = None

        if (
            inspect.iscoroutinefunction(self._push_callback_org)
            and self._asyncio_thread is not None
        ):
            self._asyncio_loop.call_soon_threadsafe(self._asyncio_loop.stop)
            self._asyncio_thread.join()
            self._asyncio_thread = None

        return True

class Speaker:
    _audio: pyaudio.PyAudio
    _chunk: int
    _rate: int
    _format: int
    _channels: int
    _output_device_index: Optional[int]

    _queue: queue.Queue
    _exit: threading.Event

    _stream: pyaudio.Stream
    _thread: threading.Thread
    _asyncio_loop: asyncio.AbstractEventLoop
    _receiver_thread: threading.Thread = None

    _socket: SyncClientConnection
    _push_callback_org: Callable = None
    _push_callback: Callable = None
    _loop: asyncio.AbstractEventLoop

    def __init__(
        self,
        push_callback: Optional[Callable] = None,
        rate: int = RATE,
        chunk: int = CHUNK,
        channels: int = CHANNELS,
        output_device_index: Optional[int] = None,
    ):
        self._exit = threading.Event()
        self._queue = queue.Queue()

        self._audio = pyaudio.PyAudio()
        self._chunk = chunk
        self._rate = rate
        self._format = FORMAT
        self._channels = channels
        self._output_device_index = output_device_index

        self._socket = None
        self._push_callback_org = push_callback

    def set_callback(self, push_callback: Callable) -> None:
        self._push_callback_org = push_callback

    def start(self, socket: SyncClientConnection) -> bool:
        # Automatically get the current running event loop
        if inspect.iscoroutinefunction(socket.send):
            self._loop = asyncio.get_running_loop()

        self._exit.clear()
        self._socket = socket

        self._stream = self._audio.open(
            format=self._format,
            channels=self._channels,
            rate=self._rate,
            input=False,
            output=True,
            frames_per_buffer=self._chunk,
            output_device_index=self._output_device_index,
        )

        # determine if the push_callback is a coroutine
        if inspect.iscoroutinefunction(self._push_callback_org):
            self._push_callback = lambda data: asyncio.run_coroutine_threadsafe(
                self._push_callback_org(data), self._asyncio_loop
            ).result()
        else:
            self._push_callback = self._push_callback_org

        # start the play thread
        self._thread = threading.Thread(
            target=self._play, args=(self._queue, self._stream, self._exit), daemon=True
        )
        self._thread.start()

        # Start the stream
        self._stream.start_stream()

        # Start the receiver thread within the start function
        if self._socket is not None:
            print("Starting receiver thread...")
            self._receiver_thread = threading.Thread(
                target=self._start_receiver, args=(self._socket,)
            )
            self._receiver_thread.start()

        return True

    def _start_receiver(self, socket: SyncClientConnection):
        print("Starting threaded receiver...")
        self._start_threaded_receiver(socket)

    def _start_threaded_receiver(self, socket: SyncClientConnection):
        try:
            while True:
                if socket is None or self._exit.is_set():
                    break

                message = socket.recv()
                if message is None:
                    continue

                if isinstance(message, str):
                    print(message)
                elif isinstance(message, bytes):
                    self.add_audio_to_queue(message)
        except Exception as e:
            print(f"threaded receiver: {e}")

    def add_audio_to_queue(self, data):
        self._queue.put(data)

    def stop(self):
        self._exit.set()

        if self._stream is not None:
            self._stream.stop_stream()
            self._stream.close()
            self._stream = None

        self._thread.join()
        self._thread = None

        if self._receiver_thread is not None:
            self._receiver_thread.join()
            self._receiver_thread = None

        self._socket = None
        self._queue = None

    def _play(self, audio_out, stream, stop):
        while not stop.is_set():
            try:
                data = audio_out.get(True, TIMEOUT)
                stream.write(data)
            except queue.Empty:
                pass
            except Exception as e:
                print(f"_play: {e}")

if __name__ == "__main__":
    sys.exit(main() or 0)

```
