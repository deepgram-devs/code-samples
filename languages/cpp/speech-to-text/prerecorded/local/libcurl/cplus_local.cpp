#include <iostream>
#include <curl/curl.h>
#include <fstream>
#include <string>

int main() {
    // Initialize libcurl
    curl_global_init(CURL_GLOBAL_ALL);

    // Create a CURL handle
    CURL *curl = curl_easy_init();
    if (curl) {
        // Set the request URL
        curl_easy_setopt(curl, CURLOPT_URL, "https://api.deepgram.com/v1/listen");

        // Set the request headers
        struct curl_slist *headers = NULL;
        headers = curl_slist_append(headers, "Authorization: Token DEEPGRAM_API_KEY"); // Replace YOUR_DEEPGRAM_API_KEY with your actual API key
        headers = curl_slist_append(headers, "Content-Type: audio/wav");
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

        // Read the audio file as binary data
        std::ifstream file("youraudio.wav", std::ios::binary | std::ios::ate);
        if (!file.is_open()) {
            std::cerr << "Failed to open audio file" << std::endl;
            return 1;
        }
        std::streamsize file_size = file.tellg();
        file.seekg(0, std::ios::beg);
        std::string audio_data(file_size, '\0');
        if (!file.read(&audio_data[0], file_size)) {
            std::cerr << "Failed to read audio file" << std::endl;
            return 1;
        }
        file.close();

        // Set the request data as binary
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, audio_data.c_str());
        curl_easy_setopt(curl, CURLOPT_POSTFIELDSIZE, audio_data.size());

        // Perform the request
        CURLcode res = curl_easy_perform(curl);

        // Check for errors
        if (res != CURLE_OK) {
            std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << std::endl;
        }

        // Cleanup
        curl_easy_cleanup(curl);
        curl_slist_free_all(headers);
    } else {
        std::cerr << "Failed to initialize libcurl" << std::endl;
    }

    // Cleanup libcurl
    curl_global_cleanup();

    return 0;
}
