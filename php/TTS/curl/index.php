<?php

// Set the API endpoint URL
$url = "https://api.deepgram.com/v1/speak?model=aura-asteria-en";

// Set your Deepgram API key
$api_key = "DEEPGRAM_API_KEY";

// Set the data to be sent in JSON format
$data = array(
    'text' => "Hello, how can I help you today?"
);

// Initialize cURL session
$ch = curl_init();

// Set cURL options
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, array(
    'Authorization: Token ' . $api_key,
    'Content-Type: application/json'
));

// Execute the cURL request
$response = curl_exec($ch);

// Check for errors
if(curl_errno($ch)) {
    echo 'Error: ' . curl_error($ch);
}

// Close cURL session
curl_close($ch);

// Save the response as an MP3 file
file_put_contents('your_output_file.mp3', $response);

?>
