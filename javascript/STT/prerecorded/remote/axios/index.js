const axios = require("axios");

const url = "https://api.deepgram.com/v1/listen";
const apiKey = "YOUR_DEEPGRAM_API_KEY"; // Replace with your actual API key
const audioUrl = "https://dpgr.am/spacewalk.wav";

// Define request data
const requestData = {
  url: audioUrl,
};

// Define request headers
const headers = {
  Accept: "application/json",
  Authorization: `Token ${apiKey}`,
  "Content-Type": "application/json",
};

// Make the POST request using axios
axios
  .post(url, requestData, { headers: headers })
  .then((response) => {
    console.dir(response.data.results, { depth: null }); // Handle response data
  })
  .catch((error) => {
    console.error("Error:", error); // Handle errors
  });
