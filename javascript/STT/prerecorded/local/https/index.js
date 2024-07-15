const https = require("https");
const fs = require("fs");

const url = "https://api.deepgram.com/v1/listen";
const apiKey = "YOUR_DEEPGRAM_API_KEY"; // Replace with your actual API key
const audioFilePath = "/path/to/youraudio.wav"; // Replace with the path to your audio file

// Read the audio file as binary data
const audioData = fs.readFileSync(audioFilePath);

// Define request headers
const headers = {
  Accept: "application/json",
  Authorization: `Token ${apiKey}`,
  "Content-Type": "audio/wav",
};

// Define request options
const options = {
  method: "POST",
  headers: headers,
};

// Create a HTTPS request
const req = https.request(url, options, (res) => {
  let responseBody = "";

  // Concatenate chunks of response data
  res.on("data", (chunk) => {
    responseBody += chunk;
  });

  // When the response ends, parse and log the response body
  res.on("end", () => {
    console.dir(JSON.parse(responseBody), { depth: null }); // Handle response data
  });
});

// Handle request errors
req.on("error", (error) => {
  console.error("Error:", error); // Handle errors
});

// Write the audio data to the request body
req.write(audioData);

// End the request
req.end();
