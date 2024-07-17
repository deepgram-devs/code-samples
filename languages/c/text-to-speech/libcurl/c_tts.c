#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>

int main(void) {
    CURL *curl;
    CURLcode res;

    // Initialize libcurl
    curl = curl_easy_init();
    if(curl) {
      // Set the request headers
        struct curl_slist *headers = NULL;
        headers = curl_slist_append(headers, "Authorization: Token DEEPGRAM_API_KEY"); // Replace DEEPGRAM_API_KEY with your actual API key
        headers = curl_slist_append(headers, "Content-Type: application/json");

        // Set the request URL and add model choice
        curl_easy_setopt(curl, CURLOPT_URL, "https://api.deepgram.com/v1/speak?model=aura-asteria-en");
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

        // Set the request data
        const char *data = "{\"text\": \"Hello, how can I help you today?\"}"; // JSON data
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data);

        FILE *file = fopen("your_output_file.mp3", "wb"); // Replace "your_output_file.mp3" with the path to your output file
        if (!file) {
            fprintf(stderr, "Error: Unable to open output file\n");
            return 1;
        }
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, file);

        res = curl_easy_perform(curl);
        if(res != CURLE_OK)
            fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));

        curl_slist_free_all(headers);
        curl_easy_cleanup(curl);
        fclose(file);
    }
    return 0;
}
