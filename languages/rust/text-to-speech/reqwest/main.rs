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