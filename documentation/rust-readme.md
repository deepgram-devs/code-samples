## Speech-to-Text Conversion using Deepgram API

**Title:** Remote Speech-to-Text Conversion with Deepgram API

**Code Sample:** speech-to-text/remote/main.rs

**Description:** This Rust code sample uses the Deepgram API to convert speech to text. It sends a POST request to the API with an audio file URL and then retrieves and prints the transcription. The reqwest and serde libraries are used for HTTP requests and serialization, respectively.

### speech-to-text/remote/main.rs

```rust
use reqwest::blocking::Client;
use serde::Serialize;

#[derive(Serialize)]
struct RequestBody {
    url: String,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let api_key = "DEEPGRAM_API_KEY";
    let url = "https://api.deepgram.com/v1/listen";

    let client = Client::new();

    let request_body = RequestBody {
        url: "https://dpgr.am/spacewalk.wav".to_string(),
    };

    let response = client.post(url)
        .header("Content-Type", "application/json")
        .header("Authorization", format!("Token {}", api_key))
        .json(&request_body)
        .send()?;

    let response_text = response.text()?;

    println!("{}", response_text);

    Ok(())
}
```

## Text-to-Speech Conversion Using Deepgram API with Reqwest Library

**Title:** Converting Text to Speech Using Deepgram API and Reqwest in Rust

**Code Sample:** text-to-speech/reqwest/main.rs

**Description:** This Rust code uses the Deepgram API and the Reqwest library to convert a given text string to speech. The output is saved as an mp3 file. The program sends a POST request with the text to be converted in the request body, receives the audio data in the response, and writes it to a file.

### text-to-speech/reqwest/main.rs

```rust
use reqwest::blocking::Client;
use std::fs::File;
use std::io::copy;
use serde::Serialize;

#[derive(Serialize)]
struct RequestBody {
    text: String,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let api_key = "DEEPGRAM_API_KEY";
    let url = "https://api.deepgram.com/v1/speak?model=aura-asteria-en";
    let output_file = "your_output_file.mp3";

    let client = Client::new();

    let request_body = RequestBody {
        text: "Hello, how can I help you today?".to_string(),
    };

    let response = client.post(url)
        .header("Content-Type", "application/json")
        .header("Authorization", format!("Token {}", api_key))
        .json(&request_body)
        .send()?;

    let mut dest = File::create(output_file)?;
    let content = response.bytes()?;
    copy(&mut content.as_ref(), &mut dest)?;

    Ok(())
}
```

