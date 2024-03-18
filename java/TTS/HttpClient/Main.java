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
