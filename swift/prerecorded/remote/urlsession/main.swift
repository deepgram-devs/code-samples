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
request.setValue("Token YOUR_DEEPGRAM_API_KEY", forHTTPHeaderField: "Authorization") // Replace YOUR_DEEPGRAM_API_KEY with your actual API key
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
