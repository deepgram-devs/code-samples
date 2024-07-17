## Speech-to-Text Conversion using Deepgram API with HttpURLConnection

**Title:** Converting Prerecorded Speech to Text with HttpURLConnection in Java

**Code Sample:** speech-to-text/prerecorded/local/httpURLConnection/Main.java

**Description:** This Java code uses HttpURLConnection to send an audio file to the Deepgram API, which then converts the speech in the audio file to text. The code handles connection setup, request configuration, audio file reading, and response processing.

### speech-to-text/prerecorded/local/httpURLConnection/Main.java

```java
package prerecorded.local.httpURLConnection;

import java.io.*;
import java.net.*;

public class Main {

  public static void main(String[] args) {
    try {
      // Specify the URL for the Deepgram API endpoint
      URI uri = new URI("https://api.deepgram.com/v1/listen");

      // Open a connection to the URL
      HttpURLConnection connection = (HttpURLConnection) uri.toURL().openConnection();

      // Set the request method to POST
      connection.setRequestMethod("POST");

      // Set request headers
      connection.setRequestProperty("Authorization", "Token YOUR_DEEPGRAM_API_KEY"); // Replace YOUR_DEEPGRAM_API_KEY
                                                                                     // with your actual API key
      connection.setRequestProperty("Content-Type", "audio/wav");

      // Enable output (sending data to the server)
      connection.setDoOutput(true);

      // Get the output stream of the connection
      OutputStream outputStream = connection.getOutputStream();

      // Read the audio file as binary data and write it to the output stream
      FileInputStream fileInputStream = new FileInputStream("/path/to/youraudio.wav"); // Replace "youraudio.wav" with the path
                                                                              // to your audio file
      byte[] buffer = new byte[1024];
      int bytesRead;
      while ((bytesRead = fileInputStream.read(buffer)) != -1) {
        outputStream.write(buffer, 0, bytesRead);
      }
      fileInputStream.close();

      // Close the output stream
      outputStream.close();

      // Get the response code from the server
      int responseCode = connection.getResponseCode();

      // Check if the request was successful (status code 200)
      if (responseCode == HttpURLConnection.HTTP_OK) {
        // Read and print the response from the server
        BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
        String inputLine;
        StringBuffer response = new StringBuffer();
        while ((inputLine = in.readLine()) != null) {
          response.append(inputLine);
        }
        in.close();
        System.out.println("Response: " + response.toString());
      } else {
        System.out.println("HTTP request failed with status code " + responseCode);
      }

      // Disconnect the connection
      connection.disconnect();
    } catch (IOException | URISyntaxException e) {
      e.printStackTrace();
    }
  }
}


```

## Speech-to-Text Conversion using Deepgram API with OkHttpClient

**Title:** Converting Pre-recorded Remote Audio to Text using Deepgram API and OkHttpClient

**Code Sample:** speech-to-text/prerecorded/remote/okhttp3/Main.java

**Description:** This Java code uses the Deepgram API and OkHttpClient to convert pre-recorded audio from a remote URL into text. It sends a POST request to the Deepgram API with the audio URL and API key, then prints the response or an error message.

### speech-to-text/prerecorded/remote/okhttp3/Main.java

```java
package prerecorded.remote.okhttp3;

import okhttp3.*;

import java.io.IOException;

public class Main {
  public static void main(String[] args) throws IOException {
    // Replace "YOUR_API_KEY" with your actual API key
    String apiKey = "YOUR_DEEPGRAM_API_KEY";
    String url = "https://api.deepgram.com/v1/listen";
    String audioUrl = "https://dpgr.am/spacewalk.wav";

    // Create OkHttpClient instance
    OkHttpClient client = new OkHttpClient();

    // Create JSON request body
    MediaType mediaType = MediaType.parse("application/json");
    String json = "{\"url\": \"" + audioUrl + "\"}";
    RequestBody body = RequestBody.create(json, mediaType);

    // Create HTTP request
    Request request = new Request.Builder()
        .url(url)
        .post(body)
        .addHeader("Accept", "application/json")
        .addHeader("Authorization", "Token " + apiKey)
        .addHeader("Content-Type", "application/json")
        .build();

    // Execute the request and get the response
    Response response = client.newCall(request).execute();

    // Print the response body
    if (response.isSuccessful()) {
      System.out.println(response.body().string());
    } else {
      System.out.println("Request failed: " + response.code() + " - " + response.message());
    }

    // Close the response
    response.close();
  }
}

```

## Text-to-Speech Conversion Using Deepgram API in Java

**Title:** Text-to-Speech Conversion with Deepgram API

**Code Sample:** text-to-speech/HttpClient/Main.java

**Description:** This Java code uses the Deepgram API to convert a given text to speech. It sends a POST request with the text to be converted as a JSON payload. The response, which is an audio file, is saved in the specified output file. If the request fails, it prints the error message.

### text-to-speech/HttpClient/Main.java

```java
package TTS.HttpClient;

import java.io.FileOutputStream;
import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class Main {
    public static void main(String[] args) throws IOException, InterruptedException {
        String apiKey = "DEEPGRAM_API_KEY"; // Replace DEEPGRAM_API_KEY with your actual API key
        String url = "https://api.deepgram.com/v1/speak?model=aura-asteria-en";
        String text = "{\"text\": \"Hello, how can I help you today?\"}";
        String outputFile = "your_output_file.mp3";

        HttpClient httpClient = HttpClient.newHttpClient();
        
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .header("Authorization", "Token " + apiKey)
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(text))
                .build();

        HttpResponse<byte[]> response = httpClient.send(request, HttpResponse.BodyHandlers.ofByteArray());

        if (response.statusCode() == 200) {
            byte[] audioData = response.body();
            Path outputPath = Paths.get(outputFile);
            Files.write(outputPath, audioData);
            System.out.println("Audio file saved: " + outputPath);
        } else {
            System.err.println("Error: " + response.statusCode() + " - " + response.body());
        }
    }
}

```

## Text-to-Speech Conversion using Deepgram API and OkHttp3 Library

**Title:** Converting Text to Speech with Deepgram API and OkHttp3

**Code Sample:** text-to-speech/okhttp3/Main.java

**Description:** This Java code uses the Deepgram API and OkHttp3 library to convert a text string into speech. It sends a POST request to the Deepgram API with the text to be converted, and then saves the resulting audio file in mp3 format.

### text-to-speech/okhttp3/Main.java

```java
package TTS.okhttp3;

import okhttp3.*;

import java.io.FileOutputStream;
import java.io.IOException;

public class Main {
    public static void main(String[] args) throws IOException {
        String apiKey = "DEEPGRAM_API_KEY"; // Replace DEEPGRAM_API_KEY with your actual API key
        String url = "https://api.deepgram.com/v1/speak?model=aura-asteria-en";
        String text = "{\"text\": \"Hello, how can I help you today?\"}";
        String outputFile = "your_output_file.mp3";

        OkHttpClient client = new OkHttpClient();

        RequestBody requestBody = RequestBody.create(MediaType.parse("application/json"), text);
        Request request = new Request.Builder()
                .url(url)
                .header("Authorization", "Token " + apiKey)
                .post(requestBody)
                .build();

        try (Response response = client.newCall(request).execute()) {
            if (!response.isSuccessful()) {
                throw new IOException("Unexpected response code: " + response);
            }

            try (FileOutputStream fos = new FileOutputStream(outputFile)) {
                fos.write(response.body().bytes());
                System.out.println("Audio file saved: " + outputFile);
            }
        }
    }
}


```

