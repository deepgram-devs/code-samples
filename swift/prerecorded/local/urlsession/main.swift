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
request.setValue("Token YOUR_DEEPGRAM_API_KEY", forHTTPHeaderField: "Authorization") // Replace YOUR_DEEPGRAM_API_KEY with your actual API key
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
