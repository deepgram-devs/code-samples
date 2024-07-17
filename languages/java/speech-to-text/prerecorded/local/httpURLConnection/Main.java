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

