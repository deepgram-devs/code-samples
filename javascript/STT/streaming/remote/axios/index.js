const WebSocket = require("ws");
const axios = require("axios");
const { PassThrough } = require("stream");

const apiKey = "YOUR_DEEPGRAM_API_KEY";
const headers = {
  Authorization: `Token ${apiKey}`,
};

// Initialize WebSocket connection
const ws = new WebSocket("wss://api.deepgram.com/v1/listen", { headers });

ws.on("open", async function open() {
  console.log("WebSocket connection established.");

  try {
    // Fetch the audio stream from the remote URL
    const response = await axios({
      method: "get",
      url: "http://stream.live.vc.bbcmedia.co.uk/bbc_world_service",
      responseType: "stream",
    });

    const passThrough = new PassThrough();
    response.data.pipe(passThrough);

    passThrough.on("data", (chunk) => {
      ws.send(chunk);
    });

    passThrough.on("end", () => {
      console.log("Audio stream ended.");
      closeWebSocket();
    });

    passThrough.on("error", (err) => {
      console.error("Stream error:", err.message);
    });
  } catch (error) {
    console.error("Error fetching audio stream:", error.message);
  }
});

// Handle WebSocket message event
ws.on("message", function incoming(data) {
  let response = JSON.parse(data);
  if (response.type === "Results") {
    console.log("Transcript: ", response.channel.alternatives[0].transcript);
  }
});

// Handle WebSocket close event
ws.on("close", function close() {
  console.log("WebSocket connection closed.");
});

// Handle WebSocket error event
ws.on("error", function error(err) {
  console.error("WebSocket error:", err.message);
});

// Gracefully close the WebSocket connection when done
function closeWebSocket() {
  const closeMsg = JSON.stringify({ type: "CloseStream" });
  ws.send(closeMsg);
  ws.close();
}

// Close WebSocket when process is terminated
process.on("SIGINT", () => {
  closeWebSocket();
  process.exit();
});
