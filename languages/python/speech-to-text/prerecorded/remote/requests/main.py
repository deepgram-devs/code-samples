import requests

# Define the URL for the Deepgram API endpoint
url = "https://api.deepgram.com/v1/listen"

# Define the headers for the HTTP request
headers = {
    "Accept": "application/json",
    "Authorization": "Token YOUR_API_KEY",
    "Content-Type": "application/json"
}
# Define the data for the HTTP request
data = {"url": "https://dpgr.am/spacewalk.wav"}

# Make the HTTP request
response = requests.post(url, headers=headers, json=data)

print(response.json())