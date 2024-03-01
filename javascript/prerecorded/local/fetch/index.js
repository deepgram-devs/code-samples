const fs = require("fs");

const url = "https://api.deepgram.com/v1/listen";
const apiKey = "YOUR_DEEPGRAM_API_KEY"; // Replace with your actual API key
const audioFilePath = "/path/to/youraudio.wav"; // Replace with the path to your audio file

// Read the audio file as binary data
fs.readFile(audioFilePath, (err, audioData) => {
  if (err) {
    console.error("Error reading audio file:", err);
    return;
  }

  // Define request headers
  const headers = {
    Accept: "application/json",
    Authorization: `Token ${apiKey}`,
    "Content-Type": "audio/wav",
  };

  // Define fetch options
  const options = {
    method: "POST",
    headers: headers,
    body: audioData,
  };

  // Make the POST request using fetch
  fetch(url, options)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to make request:", response.statusText);
      }
      return response.json();
    })
    .then((data) => {
      console.dir(data, { depth: null }); // Handle response data
    })
    .catch((error) => {
      console.error("Error:", error); // Handle errors
    });
});
