
using System;
using System.Net.Http;
using System.Threading.Tasks;
class Program
{
    static async Task Main(string[] args)
    {
        string audioFilePath = "/path/to/youraudio.wav"; // Replace with the path to your audio file
        string url = "https://api.deepgram.com/v1/listen";
        string apiKey = "DEEPGRAM_API_KEY"; // Replace with your actual API key

        using (HttpClient httpClient = new HttpClient())
        {
            try
            {
                // Read the audio file as binary data
                byte[] audioData = await File.ReadAllBytesAsync(audioFilePath);

                HttpContent content = new ByteArrayContent(audioData);

                content.Headers.Add("Content-Type", "audio/wav");
                httpClient.DefaultRequestHeaders.Add("Authorization", "Token " + apiKey);

                HttpResponseMessage response = await httpClient.PostAsync(url, content);

                if (response.IsSuccessStatusCode)
                {
                    string transcription = await response.Content.ReadAsStringAsync();
                    Console.WriteLine("Transcription:");
                    Console.WriteLine(transcription);
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
