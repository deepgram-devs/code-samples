require 'net/http'

# Define the URL for the Deepgram API endpoint
url = URI.parse("https://api.deepgram.com/v1/listen")

# Define the path to the audio file
audio_file_path = "/path/to/youraudio.wav" # Replace "youraudio.wav" with the path to your audio file

# Read the audio file as binary data
audio_data = File.binread(audio_file_path)

# Create a new Net::HTTP object
http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

# Create a new HTTP request
request = Net::HTTP::Post.new(url)

# Set request headers
request["Authorization"] = "Token YOUR_DEEPGRAM_API_KEY" # Replace YOUR_DEEPGRAM_API_KEY with your actual API key
request["Content-Type"] = "audio/wav"

# Set request body with audio data
request.body = audio_data

# Send the request and get the response
response = http.request(request)

# Print the response body
puts response.body
