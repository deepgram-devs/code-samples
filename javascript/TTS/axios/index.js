const axios = require("axios");
const fs = require("fs");

const url = "https://api.deepgram.com/v1/speak?model=aura-asteria-en";
const apiKey = "DEEPGRAM_API_KEY"; // Replace with your Deepgram API key
const data = {
  text: "Hello, how can I help you today?",
};

const config = {
  headers: {
    Authorization: `Token ${apiKey}`,
    "Content-Type": "application/json",
  },
  responseType: "stream", // Ensure the response is treated as a stream
};

axios
  .post(url, data, config)
  .then((response) => {
    if (response.status !== 200) {
      console.error(`HTTP error! Status: ${response.status}`);
      return;
    }

    const dest = fs.createWriteStream("output.mp3");
    response.data.pipe(dest);
    dest.on("finish", () => {
      console.log("File saved successfully.");
    });
  })
  .catch((error) => {
    console.error("Error:", error.message);
  });
