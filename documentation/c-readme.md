## Speech-to-Text Conversion using Deepgram API with C and libcurl

**Title:** Converting Local Audio File to Text using Deepgram API

**Code Sample:** speech-to-text/prerecorded/local/libcurl/c_local.c

**Description:** This C program uses the libcurl library to send a local audio file to the Deepgram API for speech-to-text conversion. The code initializes libcurl, sets request headers, reads the audio file into a buffer, and sends the audio data to the Deepgram API. It then checks for errors and cleans up.

### speech-to-text/prerecorded/local/libcurl/c_local.c

```c
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

```

## Speech-to-Text Conversion using Deepgram API with libcurl in C

**Title:** Converting Remote Pre-recorded Speech to Text

**Code Sample:** speech-to-text/prerecorded/remote/libcurl/c_remote.c

**Description:** This C code uses the libcurl library to send a HTTP request to the Deepgram API. It sets the necessary headers and sends a JSON payload containing the URL of a pre-recorded audio file. The Deepgram API then processes this audio file and returns a transcription.

### speech-to-text/prerecorded/remote/libcurl/c_remote.c

```c
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

```

## Text-to-Speech Conversion using Deepgram API and libcurl in C

**Title:** Converting Text to Speech Using Deepgram API and libcurl in C

**Code Sample:** text-to-speech/libcurl/c_tts.c

**Description:** This C code uses the Deepgram API and the libcurl library to convert a hardcoded text string into speech. The output is saved as an MP3 file. The program initializes libcurl, sets the request headers, URL, and data, performs the request, and then cleans up.

### text-to-speech/libcurl/c_tts.c

```c
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

```

