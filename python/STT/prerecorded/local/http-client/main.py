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
