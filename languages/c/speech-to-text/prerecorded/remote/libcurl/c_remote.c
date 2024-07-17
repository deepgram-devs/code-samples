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
        headers = curl_slist_append(headers, "Accept: application/json");
        headers = curl_slist_append(headers, "Authorization: Token DEEPGRAM_API_KEY"); // Replace DEEPGRAM_API_KEY with your actual API key
        headers = curl_slist_append(headers, "Content-Type: application/json");

        // Set the request URL
        curl_easy_setopt(curl, CURLOPT_URL, "https://api.deepgram.com/v1/listen");
        // Set the request headers
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

        // Set the request data
        const char *json_data = "{\"url\": \"https://dpgr.am/spacewalk.wav\"}"; // Replace with remote file URL
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, json_data);

        // Perform the request
        res = curl_easy_perform(curl);
        // Check for errors
        if(res != CURLE_OK)
            fprintf(stderr, "curl_easy_perform() failed: %s\n",
                    curl_easy_strerror(res));

        // Cleanup
        curl_slist_free_all(headers);
        curl_easy_cleanup(curl);
    }
    return 0;
}
