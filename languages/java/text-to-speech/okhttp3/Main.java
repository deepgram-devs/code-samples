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

