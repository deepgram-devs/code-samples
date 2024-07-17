### speech-to-text/prerecorded/local/urlsession/main.swift

```swift
import Foundation

// Specify the URL for the Deepgram API endpoint
let url = URL(string: "https://api.deepgram.com/v1/listen")!

// Specify the path to the audio file
let audioFilePath = "/path/to/youraudio.wav"

// Read the audio file as binary data
guard let audioData = FileManager.default.contents(atPath: audioFilePath) else {
    print("Error: Unable to read audio file")
    exit(1)
}

// Create the URLRequest object
var request = URLRequest(url: url)
request.httpMethod = "POST"

// Set request headers
request.setValue("Token DEEPGRAM_API_KEY", forHTTPHeaderField: "Authorization") // Replace YOUR_DEEPGRAM_API_KEY with your actual API key
request.setValue("audio/wav", forHTTPHeaderField: "Content-Type")

// Set request body with audio data
request.httpBody = audioData

// Create URLSession task to perform the request
let task = URLSession.shared.dataTask(with: request) { data, response, error in
    if let error = error {
        print("Error: \(error)")
        return
    }
    
    guard let httpResponse = response as? HTTPURLResponse, (200...299).contains(httpResponse.statusCode) else {
        print("Error: Invalid response")
        return
    }
    
    if let data = data {
        if let responseBody = String(data: data, encoding: .utf8) {
            print("Response: \(responseBody)")
        } else {
            print("Error: Unable to parse response body")
        }
    } else {
        print("Error: No response data")
    }
}

// Start the URLSession task
task.resume()

// Keep the program running until the URLSession task completes
RunLoop.main.run()

```

### speech-to-text/prerecorded/remote/urlsession/main.swift

```swift
import Foundation

// Define the URL for the Deepgram API endpoint
let url = URL(string: "https://api.deepgram.com/v1/listen")!

// Define the request body
let requestBody = ["url": "https://dpgr.am/spacewalk.wav"]
guard let httpBody = try? JSONSerialization.data(withJSONObject: requestBody) else {
    print("Error: Unable to serialize request body")
    exit(1)
}

// Define the request headers
var request = URLRequest(url: url)
request.httpMethod = "POST"
request.setValue("application/json", forHTTPHeaderField: "Content-Type")
request.setValue("application/json", forHTTPHeaderField: "Accept")
request.setValue("Token DEEPGRAM_API_KEY", forHTTPHeaderField: "Authorization") // Replace YOUR_DEEPGRAM_API_KEY with your actual API key
request.httpBody = httpBody

// Perform the HTTP request
let task = URLSession.shared.dataTask(with: request) { data, response, error in
    guard let data = data, let httpResponse = response as? HTTPURLResponse, error == nil else {
        print("Error: \(error?.localizedDescription ?? "Unknown error")")
        return
    }

    // Check if the HTTP request was successful (status code 200)
    guard httpResponse.statusCode == 200 else {
        print("HTTP request failed with status code \(httpResponse.statusCode)")
        return
    }

    // Parse and print the response body
    if let responseBody = String(data: data, encoding: .utf8) {
        print("Response: \(responseBody)")
    } else {
        print("Error: Unable to parse response body")
    }
}

task.resume()

// Keep the program running until the HTTP request completes
RunLoop.main.run()

```

### text-to-speech/urlsession/main.swift

```swift
import Foundation

// Specify the URL for the Deepgram API endpoint
let url = URL(string: "https://api.deepgram.com/v1/speak?model=aura-asteria-en")!

// Replace DEEPGRAM_API_KEY with your actual API key
let apiKey = "DEEPGRAM_API_KEY"

// Text to be converted to speech
let textToSpeak = "Hello, how can I help you today?"

// Create the URLRequest object
var request = URLRequest(url: url)
request.httpMethod = "POST"

// Set request headers
request.setValue("Token \(apiKey)", forHTTPHeaderField: "Authorization")
request.setValue("application/json", forHTTPHeaderField: "Content-Type")

// Create request body with text data
let textData = ["text": textToSpeak]
let jsonData = try! JSONSerialization.data(withJSONObject: textData)
request.httpBody = jsonData

// Create URLSession task to perform the request
let task = URLSession.shared.dataTask(with: request) { data, response, error in
    if let error = error {
        print("Error: \(error)")
        return
    }
    
    guard let httpResponse = response as? HTTPURLResponse, (200...299).contains(httpResponse.statusCode) else {
        print("Error: Invalid response")
        return
    }
    
    if let audioData = data {
        do {
            // Specify the path to save the output MP3 file
            let outputPath = "your_output_file.mp3"
            try audioData.write(to: URL(fileURLWithPath: outputPath))
            print("MP3 file saved at: \(outputPath)")
        } catch {
            print("Error saving MP3 file: \(error)")
        }
    } else {
        print("Error: No response data")
    }
}

// Start the URLSession task
task.resume()

// Keep the program running until the URLSession task completes
RunLoop.main.run()

```

