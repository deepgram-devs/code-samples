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
