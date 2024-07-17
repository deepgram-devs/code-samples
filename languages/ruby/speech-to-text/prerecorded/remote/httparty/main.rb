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