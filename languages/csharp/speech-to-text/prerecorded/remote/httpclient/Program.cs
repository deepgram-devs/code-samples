using System;
using System.Net.Http;
using System.Threading.Tasks;
using Newtonsoft.Json;


class Program
{
    static async Task Main(string[] args)
    {
        string apiKey = "DEEPGRAM_API_KEY"; // Replace with the path to your audio file
        string url = "https://api.deepgram.com/v1/listen";
        string audioUrl = "https://dpgr.am/spacewalk.wav";

        using (HttpClient client = new HttpClient())
        {
            client.DefaultRequestHeaders.Add("Accept", "application/json");
            client.DefaultRequestHeaders.Add("Authorization", "Token " + apiKey);
            
            var requestBody = new { url = audioUrl };
            var json = JsonConvert.SerializeObject(requestBody);
            var content = new StringContent(json, System.Text.Encoding.UTF8, "application/json");

            HttpResponseMessage response = await client.PostAsync(url, content);

            if (response.IsSuccessStatusCode)
            {
                string responseContent = await response.Content.ReadAsStringAsync();
                Console.WriteLine(responseContent);
            }
            else
            {
                Console.WriteLine($"Error: {response.StatusCode}");
            }
        }
    }
}
