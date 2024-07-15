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