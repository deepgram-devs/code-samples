<?php

// API endpoint URL
$url = "https://api.deepgram.com/v1/listen";

// API key
$apiKey = "YOUR_API_KEY";

// Audio file URL
$audioUrl = "https://dpgr.am/spacewalk.wav";

// Request body data
$data = array(
    "url" => $audioUrl
);

// Convert data to JSON format
$jsonData = json_encode($data);

// cURL initialization
$ch = curl_init();

// Set cURL options
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $jsonData);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, array(
    'Accept: application/json',
    'Authorization: Token ' . $apiKey,
    'Content-Type: application/json'
));

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
