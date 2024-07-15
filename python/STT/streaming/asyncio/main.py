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
