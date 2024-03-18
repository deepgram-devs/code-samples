#include <iostream>
#include <curl/curl.h>

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
        headers = curl_slist_append(headers, "Accept: application/json");
        headers = curl_slist_append(headers, "Authorization: Token DEEPGRAM_API_KEY"); // Replace YOUR_DEEPGRAM_API_KEY with your actual API key
        headers = curl_slist_append(headers, "Content-Type: application/json");
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
        
        // Set the request data
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, "{\"url\": \"https://dpgr.am/spacewalk.wav\"}"); // Replace https://dpgr.am/spacewalk.wav with the actual URL of the audio file
        
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
