<?php

// API endpoint URL
$url = "https://api.deepgram.com/v1/listen";

// API key
$apiKey = "YOUR_DEEPGRAM_API_KEY";

// Path to the audio file
$audioFilePath = "/path/to/youraudio.wav"; // Replace with the path to your audio file

// Initialize cURL session
$ch = curl_init();

// Set cURL options
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, file_get_contents($audioFilePath));
curl_setopt($ch, CURLOPT_HTTPHEADER, array(
    'Authorization: Token ' . $apiKey,
    'Content-Type: audio/wav'
));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

// Execute cURL request
$response = curl_exec($ch);

// Check for errors
if ($response === false) {
    echo 'cURL error: ' . curl_error($ch);
} else {
    // Print the response
    echo $response;
}

// Close cURL session
curl_close($ch);

?>
