**Title:** Speech-to-Text Conversion using Deepgram API with PHP and cURL

**Code Sample:** speech-to-text/prerecorded/local/curl/index.php

**Description:** This PHP script uses the cURL library to send a POST request to the Deepgram API, converting a pre-recorded .wav audio file to text. The response from the API is then printed. If there's an error, it is displayed instead.

### speech-to-text/prerecorded/local/curl/index.php

```php
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

```

## Speech-to-Text Conversion using Deepgram API with PHP

**Title:** Converting Pre-recorded Remote Audio to Text with Deepgram API in PHP

**Code Sample:** speech-to-text/prerecorded/remote/curl/index.php

**Description:** This PHP script uses the Deepgram API to convert pre-recorded audio from a remote URL to text. It sends a POST request to the API with the audio file URL, receives the response in JSON format, and prints it. If an error occurs during the process, it prints the cURL error.

### speech-to-text/prerecorded/remote/curl/index.php

```php
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

```

## Text-to-Speech Conversion Using Deepgram API

**Title:** Converting Text to Speech using Deepgram API in PHP

**Code Sample:** text-to-speech/curl/index.php

**Description:** This PHP script sends a request to Deepgram's API to convert text to speech. It uses the cURL library to make the request, passing the text "Hello, how can I help you today?" as JSON data. The API responds with an audio file which is saved as 'your_output_file.mp3'.

### text-to-speech/curl/index.php

```php
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

```

