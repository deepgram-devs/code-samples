const fs = require("fs");

const url = "https://api.deepgram.com/v1/speak?model=aura-asteria-en";
const apiKey = "DEEPGRAM_API_KEY"; // Replace with your Deepgram API key
const outputFilePath = "output_file.mp3";

const body = JSON.stringify({
  text: "Hello, how can I help you today?",
});

const headers = {
  Authorization: `Token ${apiKey}`,
  "Content-Type": "application/json",
};

const options = {
  method: "POST",
  headers: headers,
  body: body,
};

fetch(url, options)
  .then((response) => {
    if (!response.ok) {
      throw new Error("Failed to make request:", response.statusText);
    }
    return response.blob();
  })
  .then((blob) => {
    const reader = blob.stream().getReader();

    const fileStream = fs.createWriteStream(outputFilePath);
    reader.read().then(function processText({ done, value }) {
      if (done) {
        console.log("File downloaded successfully.");
        return;
      }
      fileStream.write(Buffer.from(value));
      return reader.read().then(processText);
    });
  })
  .catch((error) => {
    console.error("Error:", error);
  });
