import os
import json
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


class AsyncSpeaker:
    def __init__(
        self,
        rate: int = SAMPLE_RATE,
        chunk_size: int = CHUNK_SIZE,
        channels: int = CHANNELS,
        output_device_index: int = None,
    ):
        self._audio = pyaudio.PyAudio()
        self._chunk = chunk_size
        self._rate = rate
        self._format = FORMAT
        self._channels = channels
        self._output_device_index = output_device_index
        self._stream = None
        self._audio_queue = asyncio.Queue()
        self._is_playing = False

    def start(self) -> bool:
        self._stream = self._audio.open(
            format=self._format,
            channels=self._channels,
            rate=self._rate,
            input=False,
            output=True,
            frames_per_buffer=self._chunk,
            output_device_index=self._output_device_index,
        )
        self._stream.start_stream()
        self._is_playing = True
        return True

    def stop(self):
        self._is_playing = False
        if self._stream is not None:
            self._stream.stop_stream()
            self._stream.close()
            self._stream = None

    async def play(self, data):
        await self._audio_queue.put(data)

    async def _play_audio(self):
        while self._is_playing:
            try:
                data = await asyncio.wait_for(self._audio_queue.get(), timeout=0.050)
                self._stream.write(data)
                self._audio_queue.task_done()
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                print(f"_play_audio error: {e}")
                break


def chunk_text(text: str, words_per_chunk: int):
    words = text.split()
    for i in range(0, len(words), words_per_chunk):
        yield " ".join(words[i : i + words_per_chunk])


async def stream_text_to_websocket():
    speaker = AsyncSpeaker()
    async with aiohttp.ClientSession() as session:
        url = f"{DEEPGRAM_WS_URL}?encoding=linear16&sample_rate={SAMPLE_RATE}"
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
                speaker.start()
                try:
                    audio_player = asyncio.create_task(speaker._play_audio())
                    last_audio_duration = 0
                    nonlocal CLOSE_MESSAGE_RECEIVED
                    while True:
                        try:
                            message = await ws.receive(timeout=2)
                        except asyncio.TimeoutError:
                            continue
                        if message.type == aiohttp.WSMsgType.BINARY:
                            last_audio_duration = len(message.data) / (
                                SAMPLE_RATE * CHANNELS * 2
                            )
                            await speaker.play(message.data)
                        elif message.type == aiohttp.WSMsgType.CLOSE:
                            CLOSE_MESSAGE_RECEIVED = True
                            break

                        # Wait for remaining audio to be sent to the player
                        await speaker._audio_queue.join()
                        # Wait for the last bit of audio to be played
                        await asyncio.sleep(last_audio_duration + 0.5)
                        speaker.stop()
                        audio_player.cancel()

                except Exception as e:
                    print(f"receiver error: {vars(e)}")
                    speaker.stop()

            await asyncio.gather(send_text_stream(), receive_audio_stream())


async def main():
    await stream_text_to_websocket()


if __name__ == "__main__":
    asyncio.run(main())
