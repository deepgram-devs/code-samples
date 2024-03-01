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
