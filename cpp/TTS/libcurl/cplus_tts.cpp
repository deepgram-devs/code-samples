#include <iostream>
#include <curl/curl.h>

int main() {
    CURL *curl;
    CURLcode res;

    curl = curl_easy_init();
    if(curl) {
        curl_easy_setopt(curl, CURLOPT_URL, "https://api.deepgram.com/v1/speak?model=aura-asteria-en");

        struct curl_slist *headers = NULL;
        headers = curl_slist_append(headers, "Authorization: Token DEEPGRAM_API_KEY"); // Replace YOUR_DEEPGRAM_API_KEY with your actual API key
        headers = curl_slist_append(headers, "Content-Type: application/json");
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, "{\"text\": \"Hello, how can I help you today?\"}");
        
        FILE *fp = fopen("your_output_file.mp3", "wb");
        if (fp == NULL) {
            std::cerr << "Failed to create output file." << std::endl;
            return 1;
        }

        curl_easy_setopt(curl, CURLOPT_WRITEDATA, fp);
        
        res = curl_easy_perform(curl);

        curl_slist_free_all(headers);
        curl_easy_cleanup(curl);
        fclose(fp);

        if(res != CURLE_OK)
            std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << std::endl;
    }
    return 0;
}
