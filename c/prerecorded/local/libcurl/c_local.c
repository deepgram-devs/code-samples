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
        headers = curl_slist_append(headers, "Content-Type: audio/wav");

        // Set the request URL
        curl_easy_setopt(curl, CURLOPT_URL, "https://api.deepgram.com/v1/listen");
        // Set the request headers
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

        // Set the request data
        FILE *file = fopen("youraudio.wav", "rb"); // Replace "youraudio.wav" with the path to your audio file
        if (!file) {
            fprintf(stderr, "Error: Unable to open audio file\n");
            return 1;
        }
        fseek(file, 0, SEEK_END);
        long file_size = ftell(file);
        rewind(file);
        char *buffer = malloc(file_size);
        if (!buffer) {
            fprintf(stderr, "Error: Memory allocation failed\n");
            fclose(file);
            return 1;
        }
        if (fread(buffer, 1, file_size, file) != file_size) {
            fprintf(stderr, "Error: Failed to read audio file\n");
            fclose(file);
            free(buffer);
            return 1;
        }
        fclose(file);

        // Set the request data as binary
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, buffer);
        curl_easy_setopt(curl, CURLOPT_POSTFIELDSIZE, file_size);

        // Perform the request
        res = curl_easy_perform(curl);
        // Check for errors
        if(res != CURLE_OK)
            fprintf(stderr, "curl_easy_perform() failed: %s\n",
                    curl_easy_strerror(res));

        // Cleanup
        curl_slist_free_all(headers);
        curl_easy_cleanup(curl);
        free(buffer);
    }
    return 0;
}
