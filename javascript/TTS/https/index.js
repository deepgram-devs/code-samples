const https = require("https");
const fs = require("fs");

const url = "https://api.deepgram.com/v1/speak?model=aura-asteria-en";
const apiKey = "DEEPGRAM_API_KEY"; // Replace with your Deepgram API key
const data = JSON.stringify({
  text: "Hello, how can I help you today?",
});

const options = {
  method: "POST",
  headers: {
    Authorization: `Token ${apiKey}`,
    "Content-Type": "application/json",
  },
};

const req = https.request(url, options, (res) => {
  if (res.statusCode !== 200) {
    console.error(`HTTP error! Status: ${res.statusCode}`);
    return;
  }

  const dest = fs.createWriteStream("output.mp3");
  res.pipe(dest);
  dest.on("finish", () => {
    console.log("File saved successfully.");
  });
});

req.on("error", (error) => {
  console.error("Error:", error);
});

req.write(data);
req.end();
