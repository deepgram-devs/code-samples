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
request['Authorization'] = 'Token YOUR_API_KEY'

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
