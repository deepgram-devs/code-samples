## Speech-to-Text Conversion using Deepgram API with Axios

**Title:** Converting Pre-recorded Speech to Text Using Deepgram API and Axios

**Code Sample:** speech-to-text/prerecorded/remote/axios/index.js

**Description:** This JavaScript code uses Axios to make a POST request to the Deepgram API, converting a pre-recorded audio file (spacewalk.wav) from a remote URL into text. It handles both the response data and any potential errors.

### speech-to-text/prerecorded/remote/axios/index.js

```javascript
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

```

## Speech-to-Text Conversion using Deepgram API with Fetch

**Title:** Converting Pre-recorded Remote Audio to Text using Fetch and Deepgram API

**Code Sample:** speech-to-text/prerecorded/remote/fetch/index.js

**Description:** This JavaScript snippet uses the Fetch API to send a POST request to the Deepgram API. It submits a pre-recorded audio file URL and receives a transcription of the audio in response. The Deepgram API key is required for authentication.

### speech-to-text/prerecorded/remote/fetch/index.js

```javascript
const url = "https://api.deepgram.com/v1/listen";
const apiKey = "YOUR_DEEPGRAM_API_KEY"; // Replace with your actual API key
const audioUrl = "https://dpgr.am/spacewalk.wav";

// Define the request data object
const data = {
  url: audioUrl,
};

// Define the request headers object
const headers = {
  Accept: "application/json",
  Authorization: `Token ${apiKey}`,
  "Content-Type": "application/json",
};

// Make the POST request using fetch API
fetch(url, {
  method: "POST",
  headers: headers, // Pass the headers object
  body: JSON.stringify(data), // Convert data object to JSON string
})
  .then((response) => response.json()) // Parse the JSON response
  .then((data) => {
    console.dir(data.results, { depth: null }); // Log response data
  })
  .catch((error) => {
    console.error("Error:", error); // Handle errors
  });

```

## Speech-to-Text Conversion using Local Audio File and Deepgram API

**Title:** Converting Local Audio File to Text using Deepgram API

**Code Sample:** speech-to-text/prerecorded/local/https/index.js

**Description:** This JavaScript code utilizes the Deepgram API to convert a local audio file into text. It reads the audio file as binary data, sends a POST request to the Deepgram API, and handles the response. The resulting transcription is then logged to the console.

### speech-to-text/prerecorded/local/https/index.js

```javascript
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

```

## Speech-to-Text Conversion using Deepgram API with Local Audio File

**Title:** Converting Local Audio File to Text using Deepgram API and Axios

**Code Sample:** speech-to-text/prerecorded/local/axios/index.js

**Description:** This code uses the Deepgram API to convert a local audio file to text. It reads the audio file as binary data and sends it to the Deepgram API using an HTTP POST request via Axios. The API key and file path are configurable.

### speech-to-text/prerecorded/local/axios/index.js

```javascript
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

```

## Speech-to-Text Conversion using Deepgram API with Local Audio File

**Title:** Converting Local Audio File to Text using Deepgram API

**Code Sample:** speech-to-text/prerecorded/local/fetch/index.js

**Description:** This JavaScript code reads a local audio file, sends it to the Deepgram API, and converts the speech in the audio file to text. The code handles potential errors in reading the file and in the API request. It prints the response data or error message to the console.

### speech-to-text/prerecorded/local/fetch/index.js

```javascript
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

```

## Real-Time Speech-to-Text Conversion with Deepgram API using WebSocket

**Title:** Streaming Speech-to-Text Conversion from Remote Audio Source

**Code Sample:** speech-to-text/streaming/remote/axios/index.js

**Description:** This JavaScript code uses the WebSocket and axios libraries to establish a real-time connection with the Deepgram API. It fetches a live audio stream from a remote URL (BBC World Service in this case), sends the audio data to the Deepgram API through the WebSocket connection, and receives transcriptions of the audio data in real-time. The code also handles various events such as opening, closing, and errors on the WebSocket, and the ending or errors in the audio stream.

### speech-to-text/streaming/remote/axios/index.js

```javascript
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

```

## Text-to-Speech Conversion Using Deepgram API

**Title:** Converting Text to Speech with Deepgram API

**Code Sample:** text-to-speech/https/index.js

**Description:** This JavaScript code uses the Deepgram API to convert a given text into speech. It sends a POST request to the API with the text to be converted. The resulting audio is saved as an MP3 file. If there's an error, it's logged in the console.

### text-to-speech/https/index.js

```javascript
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

```

## Text-to-Speech Conversion Using Deepgram API and Axios

**Title:** Converting Text to Speech with Deepgram API and Axios

**Code Sample:** text-to-speech/axios/index.js

**Description:** This JavaScript code uses the Deepgram API and Axios to convert text to speech. It sends a POST request with the text to be converted. The response is treated as a stream and saved as an MP3 file. If there's an error, it logs the error message.

### text-to-speech/axios/index.js

```javascript
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

```

## Text-to-Speech Conversion Using Deepgram API

**Title:** Converting Text to Speech and Saving as MP3 File

**Code Sample:** text-to-speech/fetch/index.js

**Description:** This Node.js script uses the Deepgram API to convert text into speech. The script sends a POST request with the text "Hello, how can I help you today?" to the API and saves the resulting speech audio as an MP3 file. The script uses fetch for HTTP requests and the fs module to write the audio data to a file.

### text-to-speech/fetch/index.js

```javascript
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

```

