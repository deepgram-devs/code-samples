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
