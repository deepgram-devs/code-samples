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
