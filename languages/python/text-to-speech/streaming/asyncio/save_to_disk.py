import os
import json
import struct
import asyncio
import aiohttp

import pyaudio

api_key = os.environ["DEEPGRAM_API_KEY"]
headers = {
    "Authorization": f"Token {api_key}",
}

# URL for Deepgram WebSocket API
DEEPGRAM_WS_URL = "wss://api.deepgram.com/v1/speak"

# Text to speak
TEXT: str = """
The sun had just begun to rise over the sleepy town of Millfield.
Emily a young woman in her mid-twenties was already awake and bustling about.
"""
TEXT = TEXT.strip()

# Audio settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
SAMPLE_RATE = 48000
CHUNK_SIZE = 8000


def generate_wav_header(sample_rate: int, channels: int):
    BITS_PER_SAMPLE = 8
    byte_rate = sample_rate * channels * (BITS_PER_SAMPLE // 8)
    header = b""
    header += b"RIFF"
    header += struct.pack("<I", 0)
    header += b"WAVE"
    header += b"fmt "
    header += struct.pack("<IHHIIHH", 16, 1, 1, sample_rate, byte_rate, 2, 16)
    header += b"data"
    header += struct.pack("<I", 0)
    return header


def chunk_text(text: str, words_per_chunk: int):
    words = text.split()
    for i in range(0, len(words), words_per_chunk):
        yield " ".join(words[i : i + words_per_chunk])


async def stream_text_to_websocket():
    async with aiohttp.ClientSession() as session:
        url = f"{DEEPGRAM_WS_URL}?sample_rate={SAMPLE_RATE}"
        async with session.ws_connect(url, headers=headers) as ws:
            print("WebSocket connection established.")
            CLOSE_MESSAGE_RECEIVED = False

            async def send_text_stream():
                for a_few_words in chunk_text(TEXT, 3):
                    await asyncio.sleep(0.5)  # pause between sending text
                    print(f"Sending: {a_few_words}")
                    await ws.send_str(
                        json.dumps({"type": "Speak", "text": a_few_words})
                    )
                await ws.send_str(json.dumps({"type": "Flush"}))
                await ws.send_str(json.dumps({"type": "Close"}))
                # Wait until Deepgram closes the websocket, then close it on this end
                while not CLOSE_MESSAGE_RECEIVED:
                    await asyncio.sleep(0.1)
                await ws.close()
                print("WebSocket connection closed.")

            async def receive_audio_stream():
                try:
                    nonlocal CLOSE_MESSAGE_RECEIVED
                    with open("output.wav", "wb") as f:
                        header = generate_wav_header(SAMPLE_RATE, CHANNELS)
                        f.write(header)
                        while True:
                            try:
                                message = await ws.receive(timeout=2)
                            except asyncio.TimeoutError:
                                continue
                            if message.type == aiohttp.WSMsgType.BINARY:
                                f.write(message.data)
                                f.flush()
                            elif message.type == aiohttp.WSMsgType.CLOSE:
                                CLOSE_MESSAGE_RECEIVED = True
                                break
                    print("Audio saved to `output.wav`")

                except Exception as e:
                    print(f"receiver error: {vars(e)}")

            await asyncio.gather(send_text_stream(), receive_audio_stream())


async def main():
    await stream_text_to_websocket()


if __name__ == "__main__":
    asyncio.run(main())
