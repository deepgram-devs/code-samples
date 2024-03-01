import http.client
import json

# Create the connection
conn = http.client.HTTPSConnection("api.deepgram.com")

# Define the payload for the HTTP request
payload = json.dumps({"url": "https://dpgr.am/spacewalk.wav"})

# Define the headers for the HTTP request
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Token YOUR_API_KEY'
}

# Make the HTTP request
conn.request("POST", "/v1/listen", payload, headers)

# Get the response from the HTTP request
res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))