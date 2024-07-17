import http.client
import json

url = "api.deepgram.com"
request_body = json.dumps({"text": "Hello, how can I help you today?"})
headers = {
    "Authorization": "Token YOUR_DEEPGRAM_API_KEY",  # Replace with your Deepgram API key
    "Content-Type": "application/json"
}

conn = http.client.HTTPSConnection(url)

conn.request("POST", "/v1/speak?model=aura-asteria-en", request_body, headers)

response = conn.getresponse()

output_file_path = "your_output_file.mp3"
with open(output_file_path, "wb") as output_file:
    output_file.write(response.read())

conn.close()

print("File saved successfully at:", output_file_path)
