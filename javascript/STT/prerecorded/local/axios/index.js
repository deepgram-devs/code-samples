const axios = require("axios");
const fs = require("fs");

const url = "https://api.deepgram.com/v1/listen";
const apiKey = "YOUR_DEEPGRAM_API_KEY"; // Replace with your actual API key
const audioFilePath = "/path/to/youraudio.wav"; // Replace with the path to your audio file

// Read the audio file as binary data
const audioData = fs.readFileSync(audioFilePath);

// Define request headers
const headers = {
  Authorization: `Token ${apiKey}`,
  "Content-Type": "audio/wav",
};

// Make the POST request using axios
axios
  .post(url, audioData, { headers: headers })
  .then((response) => {
    console.log(response.data); // Handle response data
  })
  .catch((error) => {
    console.error("Error:", error); // Handle errors
  });
