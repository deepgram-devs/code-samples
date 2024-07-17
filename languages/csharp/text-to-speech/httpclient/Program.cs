using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        // Define your JSON object (text input for TTS)
        string json = "{\"text\": \"Hello, how can I help you today?\"}";
        string url = "https://api.deepgram.com/v1/speak";
        string apiKey = "DEEPGRAM_API_KEY"; // Replace with your actual API key

        using (HttpClient httpClient = new HttpClient())
        {
            try
            {
                HttpContent content = new StringContent(json, Encoding.UTF8, "application/json");

                httpClient.DefaultRequestHeaders.Add("Authorization", "token " + apiKey);

                HttpResponseMessage response = await httpClient.PostAsync(url, content);

                if (response.IsSuccessStatusCode)
                {
                    // Read and save the response as binary data
                    using (Stream audioStream = await response.Content.ReadAsStreamAsync())
                    {
                        string filePath = "your_output_file.mp3"; // Change the file extension based on the audio format
                        using (FileStream fileStream = File.Create(filePath))
                        {
                            using (BinaryWriter writer = new BinaryWriter(fileStream))
                            {
                                // Copy the binary data from the response stream to the file stream
                                byte[] buffer = new byte[8192];
                                int bytesRead;
                                while ((bytesRead = await audioStream.ReadAsync(buffer, 0, buffer.Length)) > 0)
                                {
                                    writer.Write(buffer, 0, bytesRead);
                                }
                            }
                        }
                        Console.WriteLine("Audio file saved successfully.");
                    }
                }
                else
                {
                    Console.WriteLine("Request failed with status code: " + response.StatusCode);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error: " + ex.Message);
            }
        }
    }
}