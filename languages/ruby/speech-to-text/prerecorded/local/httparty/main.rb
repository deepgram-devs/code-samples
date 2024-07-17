require 'httparty'

# Define the URL for the Deepgram API endpoint
url = 'https://api.deepgram.com/v1/listen'

# Define the path to the audio file
audio_file_path = '/path/to/youraudio.wav' # Replace 'youraudio.wav' with the path to your audio file

# Read the audio file as binary data
audio_data = File.binread(audio_file_path)

# Define the headers
headers = {
  'Authorization' => 'Token DEEPGRAM_API_KEY', # Replace YOUR_DEEPGRAM_API_KEY with your actual API key
  'Content-Type' => 'audio/wav'
}

# Make the HTTP POST request using HTTParty
response = HTTParty.post(
  url,
  headers: headers,
  body: audio_data
)

# Print the response body
puts response.body
