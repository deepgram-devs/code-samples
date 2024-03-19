import requests

url = "https://api.deepgram.com/v1/speak?model=aura-asteria-en"
headers = {
    "Authorization": "Token DEEPGRAM_API_KEY", # Replace with your Deepgram API key
    "Content-Type": "application/json"
}
payload = {
    "text": "Hello, how can I help you today?"
}

response = requests.post(url, headers=headers, json=payload)

if response.status_code == 200:
    with open("your_output_file.mp3", "wb") as f:
        f.write(response.content)
    print("File saved successfully.")
else:
    print(f"Error: {response.status_code} - {response.text}")
