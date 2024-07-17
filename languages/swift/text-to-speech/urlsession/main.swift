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
