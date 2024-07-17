## Speech-to-Text Conversion using Deepgram API and HTTParty

**Title:** Local Audio File Speech-to-Text Conversion

**Code Sample:** speech-to-text/prerecorded/local/httparty/main.rb

**Description:** This Ruby script uses the HTTParty library to send a local audio file to the Deepgram API for speech-to-text conversion. The script reads the audio file as binary data, and then sends it as a POST request to the Deepgram API. The resulting transcription is then printed to the console.

### speech-to-text/prerecorded/local/httparty/main.rb

```ruby
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

```

## Speech-to-Text Conversion using Deepgram API with Ruby

**Title:** Converting Pre-recorded Audio to Text using Net::HTTP in Ruby

**Code Sample:** speech-to-text/prerecorded/local/net-http/main.rb

**Description:** This Ruby script uses the 'net/http' library to send a POST request to Deepgram's API, converting a pre-recorded audio file to text. The script reads an audio file, sends it to the Deepgram API, and prints the response, which contains the transcribed text.

### speech-to-text/prerecorded/local/net-http/main.rb

```ruby
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
request["Authorization"] = "Token DEEPGRAM_API_KEY" # Replace YOUR_DEEPGRAM_API_KEY with your actual API key
request["Content-Type"] = "audio/wav"

# Set request body with audio data
request.body = audio_data

# Send the request and get the response
response = http.request(request)

# Print the response body
puts response.body

```

## Speech-to-Text Conversion using Deepgram API with HTTParty

**Title:** Converting Pre-recorded Remote Audio to Text using Deepgram API and HTTParty

**Code Sample:** speech-to-text/prerecorded/remote/httparty/main.rb

**Description:** This Ruby script uses the HTTParty library to send a POST request to the Deepgram API, converting a pre-recorded remote audio file (spacewalk.wav) into text. The script defines the API endpoint, headers, and request body, and then outputs the response.

### speech-to-text/prerecorded/remote/httparty/main.rb

```ruby
require 'httparty'

# Define the URL for the Deepgram API endpoint
url = 'https://api.deepgram.com/v1/listen'

# Define headers
headers = {
  'Accept' => 'application/json',
  'Authorization' => 'Token DEEPGRAM_API_KEY',
  'Content-Type' => 'application/json'
}

# Define the request body in JSON format
body = {
  url: 'https://dpgr.am/spacewalk.wav'
}.to_json

# Make a POST request to the Deepgram API endpoint using HTTParty
response = HTTParty.post(url, headers: headers, body: body)

# Output the response
puts response.body
```

## Speech-to-Text Conversion using Deepgram API with Ruby

**Title:** Converting Pre-recorded Remote Audio to Text using Deepgram API and Ruby

**Code Sample:** speech-to-text/prerecorded/remote/net-http/main.rb

**Description:** This Ruby script sends a POST request to the Deepgram API to transcribe a pre-recorded audio file (spacewalk.wav) located at a remote URL. It sets up the required headers, sends the request, and prints the response body.

### speech-to-text/prerecorded/remote/net-http/main.rb

```ruby
require 'uri'
require 'net/http'
require 'json'

# Parse the URI for the Deepgram API endpoint
uri = URI.parse('https://api.deepgram.com/v1/listen')

# Create a new HTTP POST request
request = Net::HTTP::Post.new(uri)

# Set the headers
request.content_type = 'application/json'
request['Accept'] = 'application/json'
request['Authorization'] = 'Token DEEPGRAM_API_KEY'

# Set the request body with a JSON payload containing the UR
request.body = JSON.dump({
                           'url' => 'https://dpgr.am/spacewalk.wav'
                         })
# Send the HTTP request and store the response
response = Net::HTTP.start(uri.hostname, uri.port, use_ssl: true) do |http|
  http.request(request)
end

# Output the response body
puts response.body

```

## Text-to-Speech Conversion Using Deepgram API and HTTParty Library

**Title:** Converting Text to Speech with Deepgram API and HTTParty

**Code Sample:** text-to-speech/httparty/main.rb

**Description:** This Ruby script uses the HTTParty library to send a POST request to the Deepgram API, converting a given text into speech. The output is saved as an MP3 file. If the request is successful, it will output 'File saved successfully', otherwise, it will display the error code and message.

### text-to-speech/httparty/main.rb

```ruby
require 'httparty'

url = "https://api.deepgram.com/v1/speak?model=aura-asteria-en"
headers = {
  "Authorization" => "Token DEEPGRAM_API_KEY", # Replace with your Deepgram API key
  "Content-Type" => "application/json"
}
body = {
  "text" => "Hello, how can I help you today?"
}

response = HTTParty.post(url, headers: headers, body: body.to_json)

if response.code == 200
  File.open('your_output_file.mp3', 'wb') do |file|
    file.write(response.body)
  end
  puts 'File saved successfully.'
else
  puts "Error: #{response.code} #{response.message}"
end

```

## Text-to-Speech Conversion using Deepgram API in Ruby

**Title:** Converting Text to Speech using Deepgram API in Ruby

**Code Sample:** text-to-speech/net-http/main.rb

**Description:** This code uses the Deepgram API to convert a given text into speech. The output is saved as an MP3 file. It uses the Net::HTTP library in Ruby to make HTTP requests. The API key for Deepgram is required for authentication.

### text-to-speech/net-http/main.rb

```ruby
require 'net/http'
require 'uri'

uri = URI.parse("https://api.deepgram.com/v1/speak?model=aura-asteria-en")
http = Net::HTTP.new(uri.host, uri.port)
http.use_ssl = true

request = Net::HTTP::Post.new(uri.request_uri)
request['Authorization'] = 'Token DEEPGRAM_API_KEY' # Replace with your Deepgram API key
request['Content-Type'] = 'application/json'
request.body = '{"text": "Hello, how can I help you today?"}'

response = http.request(request)

if response.code == '200'
  File.open('your_output_file.mp3', 'wb') do |file|
    file.write(response.body)
  end
  puts 'File saved successfully.'
else
  puts "Error: #{response.code} #{response.message}"
end

```

