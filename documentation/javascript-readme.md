### speech-to-text/streaming/remote/axios/index.js

```javascript
const WebSocket = require("ws");
const axios = require("axios");
const { PassThrough } = require("stream");

const apiKey = "YOUR_DEEPGRAM_API_KEY";
const headers = {
  Authorization: `Token ${apiKey}`,
};

// Initialize WebSocket connection
const ws = new WebSocket("wss://api.deepgram.com/v1/listen", { headers });

ws.on("open", async function open() {
  console.log("WebSocket connection established.");

  try {
    // Fetch the audio stream from the remote URL
    const response = await axios({
      method: "get",
      url: "http://stream.live.vc.bbcmedia.co.uk/bbc_world_service",
      responseType: "stream",
    });

    const passThrough = new PassThrough();
    response.data.pipe(passThrough);

    passThrough.on("data", (chunk) => {
      ws.send(chunk);
    });

    passThrough.on("end", () => {
      console.log("Audio stream ended.");
      closeWebSocket();
    });

    passThrough.on("error", (err) => {
      console.error("Stream error:", err.message);
    });
  } catch (error) {
    console.error("Error fetching audio stream:", error.message);
  }
});

// Handle WebSocket message event
ws.on("message", function incoming(data) {
  let response = JSON.parse(data);
  if (response.type === "Results") {
    console.log("Transcript: ", response.channel.alternatives[0].transcript);
  }
});

// Handle WebSocket close event
ws.on("close", function close() {
  console.log("WebSocket connection closed.");
});

// Handle WebSocket error event
ws.on("error", function error(err) {
  console.error("WebSocket error:", err.message);
});

// Gracefully close the WebSocket connection when done
function closeWebSocket() {
  const closeMsg = JSON.stringify({ type: "CloseStream" });
  ws.send(closeMsg);
  ws.close();
}

// Close WebSocket when process is terminated
process.on("SIGINT", () => {
  closeWebSocket();
  process.exit();
});

```

### speech-to-text/prerecorded/local/https/index.js

```javascript
const https = require("https");
const fs = require("fs");

const url = "https://api.deepgram.com/v1/listen";
const apiKey = "YOUR_DEEPGRAM_API_KEY"; // Replace with your actual API key
const audioFilePath = "/path/to/youraudio.wav"; // Replace with the path to your audio file

// Read the audio file as binary data
const audioData = fs.readFileSync(audioFilePath);

// Define request headers
const headers = {
  Accept: "application/json",
  Authorization: `Token ${apiKey}`,
  "Content-Type": "audio/wav",
};

// Define request options
const options = {
  method: "POST",
  headers: headers,
};

// Create a HTTPS request
const req = https.request(url, options, (res) => {
  let responseBody = "";

  // Concatenate chunks of response data
  res.on("data", (chunk) => {
    responseBody += chunk;
  });

  // When the response ends, parse and log the response body
  res.on("end", () => {
    console.dir(JSON.parse(responseBody), { depth: null }); // Handle response data
  });
});

// Handle request errors
req.on("error", (error) => {
  console.error("Error:", error); // Handle errors
});

// Write the audio data to the request body
req.write(audioData);

// End the request
req.end();

```

### speech-to-text/prerecorded/local/fetch/index.js

```javascript
const fs = require("fs");

const url = "https://api.deepgram.com/v1/listen";
const apiKey = "YOUR_DEEPGRAM_API_KEY"; // Replace with your actual API key
const audioFilePath = "/path/to/youraudio.wav"; // Replace with the path to your audio file

// Read the audio file as binary data
fs.readFile(audioFilePath, (err, audioData) => {
  if (err) {
    console.error("Error reading audio file:", err);
    return;
  }

  // Define request headers
  const headers = {
    Accept: "application/json",
    Authorization: `Token ${apiKey}`,
    "Content-Type": "audio/wav",
  };

  // Define fetch options
  const options = {
    method: "POST",
    headers: headers,
    body: audioData,
  };

  // Make the POST request using fetch
  fetch(url, options)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to make request:", response.statusText);
      }
      return response.json();
    })
    .then((data) => {
      console.dir(data, { depth: null }); // Handle response data
    })
    .catch((error) => {
      console.error("Error:", error); // Handle errors
    });
});

```

### speech-to-text/prerecorded/local/axios/index.js

```javascript
const axios = require("axios");
const fs = require("fs");

const url = "https://api.deepgram.com/v1/listen";
const apiKey = "YOUR_DEEPGRAM_API_KEY"; // Replace with your actual API key
const audioFilePath = "/path/to/youraudio.wav"; // Replace with the path to your audio file

// Read the audio file as binary data
const audioData = fs.readFileSync(audioFilePath);

// Define request headers
const headers = {
  Authorization: `Token ${apiKey}`,
  "Content-Type": "audio/wav",
};

// Make the POST request using axios
axios
  .post(url, audioData, { headers: headers })
  .then((response) => {
    console.log(response.data); // Handle response data
  })
  .catch((error) => {
    console.error("Error:", error); // Handle errors
  });

```

### speech-to-text/prerecorded/remote/fetch/index.js

```javascript
const url = "https://api.deepgram.com/v1/listen";
const apiKey = "YOUR_DEEPGRAM_API_KEY"; // Replace with your actual API key
const audioUrl = "https://dpgr.am/spacewalk.wav";

// Define the request data object
const data = {
  url: audioUrl,
};

// Define the request headers object
const headers = {
  Accept: "application/json",
  Authorization: `Token ${apiKey}`,
  "Content-Type": "application/json",
};

// Make the POST request using fetch API
fetch(url, {
  method: "POST",
  headers: headers, // Pass the headers object
  body: JSON.stringify(data), // Convert data object to JSON string
})
  .then((response) => response.json()) // Parse the JSON response
  .then((data) => {
    console.dir(data.results, { depth: null }); // Log response data
  })
  .catch((error) => {
    console.error("Error:", error); // Handle errors
  });

```

### speech-to-text/prerecorded/remote/axios/index.js

```javascript
const axios = require("axios");

const url = "https://api.deepgram.com/v1/listen";
const apiKey = "YOUR_DEEPGRAM_API_KEY"; // Replace with your actual API key
const audioUrl = "https://dpgr.am/spacewalk.wav";

// Define request data
const requestData = {
  url: audioUrl,
};

// Define request headers
const headers = {
  Accept: "application/json",
  Authorization: `Token ${apiKey}`,
  "Content-Type": "application/json",
};

// Make the POST request using axios
axios
  .post(url, requestData, { headers: headers })
  .then((response) => {
    console.dir(response.data.results, { depth: null }); // Handle response data
  })
  .catch((error) => {
    console.error("Error:", error); // Handle errors
  });

```

### node_modules/buffer-alloc-unsafe/index.js

```javascript
function allocUnsafe (size) {
  if (typeof size !== 'number') {
    throw new TypeError('"size" argument must be a number')
  }

  if (size < 0) {
    throw new RangeError('"size" argument must not be negative')
  }

  if (Buffer.allocUnsafe) {
    return Buffer.allocUnsafe(size)
  } else {
    return new Buffer(size)
  }
}

module.exports = allocUnsafe

```

### node_modules/node-domexception/index.js

```javascript
/*! node-domexception. MIT License. Jimmy Wärting <https://jimmy.warting.se/opensource> */

if (!globalThis.DOMException) {
  try {
    const { MessageChannel } = require('worker_threads'),
    port = new MessageChannel().port1,
    ab = new ArrayBuffer()
    port.postMessage(ab, [ab, ab])
  } catch (err) {
    err.constructor.name === 'DOMException' && (
      globalThis.DOMException = err.constructor
    )
  }
}

module.exports = globalThis.DOMException

```

### node_modules/ms/index.js

```javascript
/**
 * Helpers.
 */

var s = 1000;
var m = s * 60;
var h = m * 60;
var d = h * 24;
var y = d * 365.25;

/**
 * Parse or format the given `val`.
 *
 * Options:
 *
 *  - `long` verbose formatting [false]
 *
 * @param {String|Number} val
 * @param {Object} [options]
 * @throws {Error} throw an error if val is not a non-empty string or a number
 * @return {String|Number}
 * @api public
 */

module.exports = function(val, options) {
  options = options || {};
  var type = typeof val;
  if (type === 'string' && val.length > 0) {
    return parse(val);
  } else if (type === 'number' && isNaN(val) === false) {
    return options.long ? fmtLong(val) : fmtShort(val);
  }
  throw new Error(
    'val is not a non-empty string or a valid number. val=' +
      JSON.stringify(val)
  );
};

/**
 * Parse the given `str` and return milliseconds.
 *
 * @param {String} str
 * @return {Number}
 * @api private
 */

function parse(str) {
  str = String(str);
  if (str.length > 100) {
    return;
  }
  var match = /^((?:\d+)?\.?\d+) *(milliseconds?|msecs?|ms|seconds?|secs?|s|minutes?|mins?|m|hours?|hrs?|h|days?|d|years?|yrs?|y)?$/i.exec(
    str
  );
  if (!match) {
    return;
  }
  var n = parseFloat(match[1]);
  var type = (match[2] || 'ms').toLowerCase();
  switch (type) {
    case 'years':
    case 'year':
    case 'yrs':
    case 'yr':
    case 'y':
      return n * y;
    case 'days':
    case 'day':
    case 'd':
      return n * d;
    case 'hours':
    case 'hour':
    case 'hrs':
    case 'hr':
    case 'h':
      return n * h;
    case 'minutes':
    case 'minute':
    case 'mins':
    case 'min':
    case 'm':
      return n * m;
    case 'seconds':
    case 'second':
    case 'secs':
    case 'sec':
    case 's':
      return n * s;
    case 'milliseconds':
    case 'millisecond':
    case 'msecs':
    case 'msec':
    case 'ms':
      return n;
    default:
      return undefined;
  }
}

/**
 * Short format for `ms`.
 *
 * @param {Number} ms
 * @return {String}
 * @api private
 */

function fmtShort(ms) {
  if (ms >= d) {
    return Math.round(ms / d) + 'd';
  }
  if (ms >= h) {
    return Math.round(ms / h) + 'h';
  }
  if (ms >= m) {
    return Math.round(ms / m) + 'm';
  }
  if (ms >= s) {
    return Math.round(ms / s) + 's';
  }
  return ms + 'ms';
}

/**
 * Long format for `ms`.
 *
 * @param {Number} ms
 * @return {String}
 * @api private
 */

function fmtLong(ms) {
  return plural(ms, d, 'day') ||
    plural(ms, h, 'hour') ||
    plural(ms, m, 'minute') ||
    plural(ms, s, 'second') ||
    ms + ' ms';
}

/**
 * Pluralization helper.
 */

function plural(ms, n, name) {
  if (ms < n) {
    return;
  }
  if (ms < n * 1.5) {
    return Math.floor(ms / n) + ' ' + name;
  }
  return Math.ceil(ms / n) + ' ' + name + 's';
}

```

### node_modules/wav/index.js

```javascript

/**
 * References:
 *  - http://tools.ietf.org/html/rfc2361
 *  - http://www.sonicspot.com/guide/wavefiles.html
 *  - https://ccrma.stanford.edu/courses/422/projects/WaveFormat/
 *  - http://www-mmsp.ece.mcgill.ca/Documents/AudioFormats/WAVE/WAVE.html
 *  - http://www.blitter.com/~russtopia/MIDI/~jglatt/tech/wave.htm
 */

/**
 * The `Reader` class accepts a WAVE audio file, emits a "format" event, and
 * outputs the raw "data" from the WAVE file (usually raw PCM data, but if the
 * WAVE file uses compression then the compressed data will be output, you are
 * responsible for uncompressing in that case if necessary).
 */

exports.Reader = require('./lib/reader');

/**
 * The `Writer` class outputs a valid WAVE file from the audio data written to
 * it. You may set any of the "channels", "sampleRate" or "bitsPerSample"
 * properties before writing the first chunk. You may also set the "dataLength" to
 * the number of bytes expected in the "data" portion of the WAVE file. If
 * "dataLength" is not set, then the maximum valid length for a WAVE file is
 * written.
 */

exports.Writer = require('./lib/writer');

/**
 * The `FileWriter` is a subclass of `Writer` that automatically takes care of
 * writing the "header" event at the end of the stream to the beginning of the
 * output file.
 */

exports.FileWriter = require('./lib/file-writer');

```

### node_modules/node-fetch/src/index.js

```javascript
/**
 * Index.js
 *
 * a request API compatible with window.fetch
 *
 * All spec algorithm step numbers are based on https://fetch.spec.whatwg.org/commit-snapshots/ae716822cb3a61843226cd090eefc6589446c1d2/.
 */

import http from 'node:http';
import https from 'node:https';
import zlib from 'node:zlib';
import Stream, {PassThrough, pipeline as pump} from 'node:stream';
import {Buffer} from 'node:buffer';

import dataUriToBuffer from 'data-uri-to-buffer';

import {writeToStream, clone} from './body.js';
import Response from './response.js';
import Headers, {fromRawHeaders} from './headers.js';
import Request, {getNodeRequestOptions} from './request.js';
import {FetchError} from './errors/fetch-error.js';
import {AbortError} from './errors/abort-error.js';
import {isRedirect} from './utils/is-redirect.js';
import {FormData} from 'formdata-polyfill/esm.min.js';
import {isDomainOrSubdomain, isSameProtocol} from './utils/is.js';
import {parseReferrerPolicyFromHeader} from './utils/referrer.js';
import {
	Blob,
	File,
	fileFromSync,
	fileFrom,
	blobFromSync,
	blobFrom
} from 'fetch-blob/from.js';

export {FormData, Headers, Request, Response, FetchError, AbortError, isRedirect};
export {Blob, File, fileFromSync, fileFrom, blobFromSync, blobFrom};

const supportedSchemas = new Set(['data:', 'http:', 'https:']);

/**
 * Fetch function
 *
 * @param   {string | URL | import('./request').default} url - Absolute url or Request instance
 * @param   {*} [options_] - Fetch options
 * @return  {Promise<import('./response').default>}
 */
export default async function fetch(url, options_) {
	return new Promise((resolve, reject) => {
		// Build request object
		const request = new Request(url, options_);
		const {parsedURL, options} = getNodeRequestOptions(request);
		if (!supportedSchemas.has(parsedURL.protocol)) {
			throw new TypeError(`node-fetch cannot load ${url}. URL scheme "${parsedURL.protocol.replace(/:$/, '')}" is not supported.`);
		}

		if (parsedURL.protocol === 'data:') {
			const data = dataUriToBuffer(request.url);
			const response = new Response(data, {headers: {'Content-Type': data.typeFull}});
			resolve(response);
			return;
		}

		// Wrap http.request into fetch
		const send = (parsedURL.protocol === 'https:' ? https : http).request;
		const {signal} = request;
		let response = null;

		const abort = () => {
			const error = new AbortError('The operation was aborted.');
			reject(error);
			if (request.body && request.body instanceof Stream.Readable) {
				request.body.destroy(error);
			}

			if (!response || !response.body) {
				return;
			}

			response.body.emit('error', error);
		};

		if (signal && signal.aborted) {
			abort();
			return;
		}

		const abortAndFinalize = () => {
			abort();
			finalize();
		};

		// Send request
		const request_ = send(parsedURL.toString(), options);

		if (signal) {
			signal.addEventListener('abort', abortAndFinalize);
		}

		const finalize = () => {
			request_.abort();
			if (signal) {
				signal.removeEventListener('abort', abortAndFinalize);
			}
		};

		request_.on('error', error => {
			reject(new FetchError(`request to ${request.url} failed, reason: ${error.message}`, 'system', error));
			finalize();
		});

		fixResponseChunkedTransferBadEnding(request_, error => {
			if (response && response.body) {
				response.body.destroy(error);
			}
		});

		/* c8 ignore next 18 */
		if (process.version < 'v14') {
			// Before Node.js 14, pipeline() does not fully support async iterators and does not always
			// properly handle when the socket close/end events are out of order.
			request_.on('socket', s => {
				let endedWithEventsCount;
				s.prependListener('end', () => {
					endedWithEventsCount = s._eventsCount;
				});
				s.prependListener('close', hadError => {
					// if end happened before close but the socket didn't emit an error, do it now
					if (response && endedWithEventsCount < s._eventsCount && !hadError) {
						const error = new Error('Premature close');
						error.code = 'ERR_STREAM_PREMATURE_CLOSE';
						response.body.emit('error', error);
					}
				});
			});
		}

		request_.on('response', response_ => {
			request_.setTimeout(0);
			const headers = fromRawHeaders(response_.rawHeaders);

			// HTTP fetch step 5
			if (isRedirect(response_.statusCode)) {
				// HTTP fetch step 5.2
				const location = headers.get('Location');

				// HTTP fetch step 5.3
				let locationURL = null;
				try {
					locationURL = location === null ? null : new URL(location, request.url);
				} catch {
					// error here can only be invalid URL in Location: header
					// do not throw when options.redirect == manual
					// let the user extract the errorneous redirect URL
					if (request.redirect !== 'manual') {
						reject(new FetchError(`uri requested responds with an invalid redirect URL: ${location}`, 'invalid-redirect'));
						finalize();
						return;
					}
				}

				// HTTP fetch step 5.5
				switch (request.redirect) {
					case 'error':
						reject(new FetchError(`uri requested responds with a redirect, redirect mode is set to error: ${request.url}`, 'no-redirect'));
						finalize();
						return;
					case 'manual':
						// Nothing to do
						break;
					case 'follow': {
						// HTTP-redirect fetch step 2
						if (locationURL === null) {
							break;
						}

						// HTTP-redirect fetch step 5
						if (request.counter >= request.follow) {
							reject(new FetchError(`maximum redirect reached at: ${request.url}`, 'max-redirect'));
							finalize();
							return;
						}

						// HTTP-redirect fetch step 6 (counter increment)
						// Create a new Request object.
						const requestOptions = {
							headers: new Headers(request.headers),
							follow: request.follow,
							counter: request.counter + 1,
							agent: request.agent,
							compress: request.compress,
							method: request.method,
							body: clone(request),
							signal: request.signal,
							size: request.size,
							referrer: request.referrer,
							referrerPolicy: request.referrerPolicy
						};

						// when forwarding sensitive headers like "Authorization",
						// "WWW-Authenticate", and "Cookie" to untrusted targets,
						// headers will be ignored when following a redirect to a domain
						// that is not a subdomain match or exact match of the initial domain.
						// For example, a redirect from "foo.com" to either "foo.com" or "sub.foo.com"
						// will forward the sensitive headers, but a redirect to "bar.com" will not.
						// headers will also be ignored when following a redirect to a domain using
						// a different protocol. For example, a redirect from "https://foo.com" to "http://foo.com"
						// will not forward the sensitive headers
						if (!isDomainOrSubdomain(request.url, locationURL) || !isSameProtocol(request.url, locationURL)) {
							for (const name of ['authorization', 'www-authenticate', 'cookie', 'cookie2']) {
								requestOptions.headers.delete(name);
							}
						}

						// HTTP-redirect fetch step 9
						if (response_.statusCode !== 303 && request.body && options_.body instanceof Stream.Readable) {
							reject(new FetchError('Cannot follow redirect with body being a readable stream', 'unsupported-redirect'));
							finalize();
							return;
						}

						// HTTP-redirect fetch step 11
						if (response_.statusCode === 303 || ((response_.statusCode === 301 || response_.statusCode === 302) && request.method === 'POST')) {
							requestOptions.method = 'GET';
							requestOptions.body = undefined;
							requestOptions.headers.delete('content-length');
						}

						// HTTP-redirect fetch step 14
						const responseReferrerPolicy = parseReferrerPolicyFromHeader(headers);
						if (responseReferrerPolicy) {
							requestOptions.referrerPolicy = responseReferrerPolicy;
						}

						// HTTP-redirect fetch step 15
						resolve(fetch(new Request(locationURL, requestOptions)));
						finalize();
						return;
					}

					default:
						return reject(new TypeError(`Redirect option '${request.redirect}' is not a valid value of RequestRedirect`));
				}
			}

			// Prepare response
			if (signal) {
				response_.once('end', () => {
					signal.removeEventListener('abort', abortAndFinalize);
				});
			}

			let body = pump(response_, new PassThrough(), error => {
				if (error) {
					reject(error);
				}
			});
			// see https://github.com/nodejs/node/pull/29376
			/* c8 ignore next 3 */
			if (process.version < 'v12.10') {
				response_.on('aborted', abortAndFinalize);
			}

			const responseOptions = {
				url: request.url,
				status: response_.statusCode,
				statusText: response_.statusMessage,
				headers,
				size: request.size,
				counter: request.counter,
				highWaterMark: request.highWaterMark
			};

			// HTTP-network fetch step 12.1.1.3
			const codings = headers.get('Content-Encoding');

			// HTTP-network fetch step 12.1.1.4: handle content codings

			// in following scenarios we ignore compression support
			// 1. compression support is disabled
			// 2. HEAD request
			// 3. no Content-Encoding header
			// 4. no content response (204)
			// 5. content not modified response (304)
			if (!request.compress || request.method === 'HEAD' || codings === null || response_.statusCode === 204 || response_.statusCode === 304) {
				response = new Response(body, responseOptions);
				resolve(response);
				return;
			}

			// For Node v6+
			// Be less strict when decoding compressed responses, since sometimes
			// servers send slightly invalid responses that are still accepted
			// by common browsers.
			// Always using Z_SYNC_FLUSH is what cURL does.
			const zlibOptions = {
				flush: zlib.Z_SYNC_FLUSH,
				finishFlush: zlib.Z_SYNC_FLUSH
			};

			// For gzip
			if (codings === 'gzip' || codings === 'x-gzip') {
				body = pump(body, zlib.createGunzip(zlibOptions), error => {
					if (error) {
						reject(error);
					}
				});
				response = new Response(body, responseOptions);
				resolve(response);
				return;
			}

			// For deflate
			if (codings === 'deflate' || codings === 'x-deflate') {
				// Handle the infamous raw deflate response from old servers
				// a hack for old IIS and Apache servers
				const raw = pump(response_, new PassThrough(), error => {
					if (error) {
						reject(error);
					}
				});
				raw.once('data', chunk => {
					// See http://stackoverflow.com/questions/37519828
					if ((chunk[0] & 0x0F) === 0x08) {
						body = pump(body, zlib.createInflate(), error => {
							if (error) {
								reject(error);
							}
						});
					} else {
						body = pump(body, zlib.createInflateRaw(), error => {
							if (error) {
								reject(error);
							}
						});
					}

					response = new Response(body, responseOptions);
					resolve(response);
				});
				raw.once('end', () => {
					// Some old IIS servers return zero-length OK deflate responses, so
					// 'data' is never emitted. See https://github.com/node-fetch/node-fetch/pull/903
					if (!response) {
						response = new Response(body, responseOptions);
						resolve(response);
					}
				});
				return;
			}

			// For br
			if (codings === 'br') {
				body = pump(body, zlib.createBrotliDecompress(), error => {
					if (error) {
						reject(error);
					}
				});
				response = new Response(body, responseOptions);
				resolve(response);
				return;
			}

			// Otherwise, use response as-is
			response = new Response(body, responseOptions);
			resolve(response);
		});

		// eslint-disable-next-line promise/prefer-await-to-then
		writeToStream(request_, request).catch(reject);
	});
}

function fixResponseChunkedTransferBadEnding(request, errorCallback) {
	const LAST_CHUNK = Buffer.from('0\r\n\r\n');

	let isChunkedTransfer = false;
	let properLastChunkReceived = false;
	let previousChunk;

	request.on('response', response => {
		const {headers} = response;
		isChunkedTransfer = headers['transfer-encoding'] === 'chunked' && !headers['content-length'];
	});

	request.on('socket', socket => {
		const onSocketClose = () => {
			if (isChunkedTransfer && !properLastChunkReceived) {
				const error = new Error('Premature close');
				error.code = 'ERR_STREAM_PREMATURE_CLOSE';
				errorCallback(error);
			}
		};

		const onData = buf => {
			properLastChunkReceived = Buffer.compare(buf.slice(-5), LAST_CHUNK) === 0;

			// Sometimes final 0-length chunk and end of message code are in separate packets
			if (!properLastChunkReceived && previousChunk) {
				properLastChunkReceived = (
					Buffer.compare(previousChunk.slice(-3), LAST_CHUNK.slice(0, 3)) === 0 &&
					Buffer.compare(buf.slice(-2), LAST_CHUNK.slice(3)) === 0
				);
			}

			previousChunk = buf;
		};

		socket.prependListener('close', onSocketClose);
		socket.on('data', onData);

		request.on('close', () => {
			socket.removeListener('close', onSocketClose);
			socket.removeListener('data', onData);
		});
	});
}

```

### node_modules/proxy-from-env/index.js

```javascript
'use strict';

var parseUrl = require('url').parse;

var DEFAULT_PORTS = {
  ftp: 21,
  gopher: 70,
  http: 80,
  https: 443,
  ws: 80,
  wss: 443,
};

var stringEndsWith = String.prototype.endsWith || function(s) {
  return s.length <= this.length &&
    this.indexOf(s, this.length - s.length) !== -1;
};

/**
 * @param {string|object} url - The URL, or the result from url.parse.
 * @return {string} The URL of the proxy that should handle the request to the
 *  given URL. If no proxy is set, this will be an empty string.
 */
function getProxyForUrl(url) {
  var parsedUrl = typeof url === 'string' ? parseUrl(url) : url || {};
  var proto = parsedUrl.protocol;
  var hostname = parsedUrl.host;
  var port = parsedUrl.port;
  if (typeof hostname !== 'string' || !hostname || typeof proto !== 'string') {
    return '';  // Don't proxy URLs without a valid scheme or host.
  }

  proto = proto.split(':', 1)[0];
  // Stripping ports in this way instead of using parsedUrl.hostname to make
  // sure that the brackets around IPv6 addresses are kept.
  hostname = hostname.replace(/:\d*$/, '');
  port = parseInt(port) || DEFAULT_PORTS[proto] || 0;
  if (!shouldProxy(hostname, port)) {
    return '';  // Don't proxy URLs that match NO_PROXY.
  }

  var proxy =
    getEnv('npm_config_' + proto + '_proxy') ||
    getEnv(proto + '_proxy') ||
    getEnv('npm_config_proxy') ||
    getEnv('all_proxy');
  if (proxy && proxy.indexOf('://') === -1) {
    // Missing scheme in proxy, default to the requested URL's scheme.
    proxy = proto + '://' + proxy;
  }
  return proxy;
}

/**
 * Determines whether a given URL should be proxied.
 *
 * @param {string} hostname - The host name of the URL.
 * @param {number} port - The effective port of the URL.
 * @returns {boolean} Whether the given URL should be proxied.
 * @private
 */
function shouldProxy(hostname, port) {
  var NO_PROXY =
    (getEnv('npm_config_no_proxy') || getEnv('no_proxy')).toLowerCase();
  if (!NO_PROXY) {
    return true;  // Always proxy if NO_PROXY is not set.
  }
  if (NO_PROXY === '*') {
    return false;  // Never proxy if wildcard is set.
  }

  return NO_PROXY.split(/[,\s]/).every(function(proxy) {
    if (!proxy) {
      return true;  // Skip zero-length hosts.
    }
    var parsedProxy = proxy.match(/^(.+):(\d+)$/);
    var parsedProxyHostname = parsedProxy ? parsedProxy[1] : proxy;
    var parsedProxyPort = parsedProxy ? parseInt(parsedProxy[2]) : 0;
    if (parsedProxyPort && parsedProxyPort !== port) {
      return true;  // Skip if ports don't match.
    }

    if (!/^[.*]/.test(parsedProxyHostname)) {
      // No wildcards, so stop proxying if there is an exact match.
      return hostname !== parsedProxyHostname;
    }

    if (parsedProxyHostname.charAt(0) === '*') {
      // Remove leading wildcard.
      parsedProxyHostname = parsedProxyHostname.slice(1);
    }
    // Stop proxying if the hostname ends with the no_proxy host.
    return !stringEndsWith.call(hostname, parsedProxyHostname);
  });
}

/**
 * Get the value for an environment variable.
 *
 * @param {string} key - The name of the environment variable.
 * @return {string} The value of the environment variable.
 * @private
 */
function getEnv(key) {
  return process.env[key.toLowerCase()] || process.env[key.toUpperCase()] || '';
}

exports.getProxyForUrl = getProxyForUrl;

```

### node_modules/string_decoder/index.js

```javascript
// Copyright Joyent, Inc. and other Node contributors.
//
// Permission is hereby granted, free of charge, to any person obtaining a
// copy of this software and associated documentation files (the
// "Software"), to deal in the Software without restriction, including
// without limitation the rights to use, copy, modify, merge, publish,
// distribute, sublicense, and/or sell copies of the Software, and to permit
// persons to whom the Software is furnished to do so, subject to the
// following conditions:
//
// The above copyright notice and this permission notice shall be included
// in all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
// OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
// MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
// NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
// DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
// OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE
// USE OR OTHER DEALINGS IN THE SOFTWARE.

var Buffer = require('buffer').Buffer;

var isBufferEncoding = Buffer.isEncoding
  || function(encoding) {
       switch (encoding && encoding.toLowerCase()) {
         case 'hex': case 'utf8': case 'utf-8': case 'ascii': case 'binary': case 'base64': case 'ucs2': case 'ucs-2': case 'utf16le': case 'utf-16le': case 'raw': return true;
         default: return false;
       }
     }


function assertEncoding(encoding) {
  if (encoding && !isBufferEncoding(encoding)) {
    throw new Error('Unknown encoding: ' + encoding);
  }
}

// StringDecoder provides an interface for efficiently splitting a series of
// buffers into a series of JS strings without breaking apart multi-byte
// characters. CESU-8 is handled as part of the UTF-8 encoding.
//
// @TODO Handling all encodings inside a single object makes it very difficult
// to reason about this code, so it should be split up in the future.
// @TODO There should be a utf8-strict encoding that rejects invalid UTF-8 code
// points as used by CESU-8.
var StringDecoder = exports.StringDecoder = function(encoding) {
  this.encoding = (encoding || 'utf8').toLowerCase().replace(/[-_]/, '');
  assertEncoding(encoding);
  switch (this.encoding) {
    case 'utf8':
      // CESU-8 represents each of Surrogate Pair by 3-bytes
      this.surrogateSize = 3;
      break;
    case 'ucs2':
    case 'utf16le':
      // UTF-16 represents each of Surrogate Pair by 2-bytes
      this.surrogateSize = 2;
      this.detectIncompleteChar = utf16DetectIncompleteChar;
      break;
    case 'base64':
      // Base-64 stores 3 bytes in 4 chars, and pads the remainder.
      this.surrogateSize = 3;
      this.detectIncompleteChar = base64DetectIncompleteChar;
      break;
    default:
      this.write = passThroughWrite;
      return;
  }

  // Enough space to store all bytes of a single character. UTF-8 needs 4
  // bytes, but CESU-8 may require up to 6 (3 bytes per surrogate).
  this.charBuffer = new Buffer(6);
  // Number of bytes received for the current incomplete multi-byte character.
  this.charReceived = 0;
  // Number of bytes expected for the current incomplete multi-byte character.
  this.charLength = 0;
};


// write decodes the given buffer and returns it as JS string that is
// guaranteed to not contain any partial multi-byte characters. Any partial
// character found at the end of the buffer is buffered up, and will be
// returned when calling write again with the remaining bytes.
//
// Note: Converting a Buffer containing an orphan surrogate to a String
// currently works, but converting a String to a Buffer (via `new Buffer`, or
// Buffer#write) will replace incomplete surrogates with the unicode
// replacement character. See https://codereview.chromium.org/121173009/ .
StringDecoder.prototype.write = function(buffer) {
  var charStr = '';
  // if our last write ended with an incomplete multibyte character
  while (this.charLength) {
    // determine how many remaining bytes this buffer has to offer for this char
    var available = (buffer.length >= this.charLength - this.charReceived) ?
        this.charLength - this.charReceived :
        buffer.length;

    // add the new bytes to the char buffer
    buffer.copy(this.charBuffer, this.charReceived, 0, available);
    this.charReceived += available;

    if (this.charReceived < this.charLength) {
      // still not enough chars in this buffer? wait for more ...
      return '';
    }

    // remove bytes belonging to the current character from the buffer
    buffer = buffer.slice(available, buffer.length);

    // get the character that was split
    charStr = this.charBuffer.slice(0, this.charLength).toString(this.encoding);

    // CESU-8: lead surrogate (D800-DBFF) is also the incomplete character
    var charCode = charStr.charCodeAt(charStr.length - 1);
    if (charCode >= 0xD800 && charCode <= 0xDBFF) {
      this.charLength += this.surrogateSize;
      charStr = '';
      continue;
    }
    this.charReceived = this.charLength = 0;

    // if there are no more bytes in this buffer, just emit our char
    if (buffer.length === 0) {
      return charStr;
    }
    break;
  }

  // determine and set charLength / charReceived
  this.detectIncompleteChar(buffer);

  var end = buffer.length;
  if (this.charLength) {
    // buffer the incomplete character bytes we got
    buffer.copy(this.charBuffer, 0, buffer.length - this.charReceived, end);
    end -= this.charReceived;
  }

  charStr += buffer.toString(this.encoding, 0, end);

  var end = charStr.length - 1;
  var charCode = charStr.charCodeAt(end);
  // CESU-8: lead surrogate (D800-DBFF) is also the incomplete character
  if (charCode >= 0xD800 && charCode <= 0xDBFF) {
    var size = this.surrogateSize;
    this.charLength += size;
    this.charReceived += size;
    this.charBuffer.copy(this.charBuffer, size, 0, size);
    buffer.copy(this.charBuffer, 0, 0, size);
    return charStr.substring(0, end);
  }

  // or just emit the charStr
  return charStr;
};

// detectIncompleteChar determines if there is an incomplete UTF-8 character at
// the end of the given buffer. If so, it sets this.charLength to the byte
// length that character, and sets this.charReceived to the number of bytes
// that are available for this character.
StringDecoder.prototype.detectIncompleteChar = function(buffer) {
  // determine how many bytes we have to check at the end of this buffer
  var i = (buffer.length >= 3) ? 3 : buffer.length;

  // Figure out if one of the last i bytes of our buffer announces an
  // incomplete char.
  for (; i > 0; i--) {
    var c = buffer[buffer.length - i];

    // See http://en.wikipedia.org/wiki/UTF-8#Description

    // 110XXXXX
    if (i == 1 && c >> 5 == 0x06) {
      this.charLength = 2;
      break;
    }

    // 1110XXXX
    if (i <= 2 && c >> 4 == 0x0E) {
      this.charLength = 3;
      break;
    }

    // 11110XXX
    if (i <= 3 && c >> 3 == 0x1E) {
      this.charLength = 4;
      break;
    }
  }
  this.charReceived = i;
};

StringDecoder.prototype.end = function(buffer) {
  var res = '';
  if (buffer && buffer.length)
    res = this.write(buffer);

  if (this.charReceived) {
    var cr = this.charReceived;
    var buf = this.charBuffer;
    var enc = this.encoding;
    res += buf.slice(0, cr).toString(enc);
  }

  return res;
};

function passThroughWrite(buffer) {
  return buffer.toString(this.encoding);
}

function utf16DetectIncompleteChar(buffer) {
  this.charReceived = buffer.length % 2;
  this.charLength = this.charReceived ? 2 : 0;
}

function base64DetectIncompleteChar(buffer) {
  this.charReceived = buffer.length % 3;
  this.charLength = this.charReceived ? 3 : 0;
}

```

### node_modules/fluent-ffmpeg/index.js

```javascript
module.exports = require('./lib/fluent-ffmpeg');

```

### node_modules/buffer-alloc/index.js

```javascript
var bufferFill = require('buffer-fill')
var allocUnsafe = require('buffer-alloc-unsafe')

module.exports = function alloc (size, fill, encoding) {
  if (typeof size !== 'number') {
    throw new TypeError('"size" argument must be a number')
  }

  if (size < 0) {
    throw new RangeError('"size" argument must not be negative')
  }

  if (Buffer.alloc) {
    return Buffer.alloc(size, fill, encoding)
  }

  var buffer = allocUnsafe(size)

  if (size === 0) {
    return buffer
  }

  if (fill === undefined) {
    return bufferFill(buffer, 0)
  }

  if (typeof encoding !== 'string') {
    encoding = undefined
  }

  return bufferFill(buffer, fill, encoding)
}

```

### node_modules/mime-types/index.js

```javascript
/*!
 * mime-types
 * Copyright(c) 2014 Jonathan Ong
 * Copyright(c) 2015 Douglas Christopher Wilson
 * MIT Licensed
 */

'use strict'

/**
 * Module dependencies.
 * @private
 */

var db = require('mime-db')
var extname = require('path').extname

/**
 * Module variables.
 * @private
 */

var EXTRACT_TYPE_REGEXP = /^\s*([^;\s]*)(?:;|\s|$)/
var TEXT_TYPE_REGEXP = /^text\//i

/**
 * Module exports.
 * @public
 */

exports.charset = charset
exports.charsets = { lookup: charset }
exports.contentType = contentType
exports.extension = extension
exports.extensions = Object.create(null)
exports.lookup = lookup
exports.types = Object.create(null)

// Populate the extensions/types maps
populateMaps(exports.extensions, exports.types)

/**
 * Get the default charset for a MIME type.
 *
 * @param {string} type
 * @return {boolean|string}
 */

function charset (type) {
  if (!type || typeof type !== 'string') {
    return false
  }

  // TODO: use media-typer
  var match = EXTRACT_TYPE_REGEXP.exec(type)
  var mime = match && db[match[1].toLowerCase()]

  if (mime && mime.charset) {
    return mime.charset
  }

  // default text/* to utf-8
  if (match && TEXT_TYPE_REGEXP.test(match[1])) {
    return 'UTF-8'
  }

  return false
}

/**
 * Create a full Content-Type header given a MIME type or extension.
 *
 * @param {string} str
 * @return {boolean|string}
 */

function contentType (str) {
  // TODO: should this even be in this module?
  if (!str || typeof str !== 'string') {
    return false
  }

  var mime = str.indexOf('/') === -1
    ? exports.lookup(str)
    : str

  if (!mime) {
    return false
  }

  // TODO: use content-type or other module
  if (mime.indexOf('charset') === -1) {
    var charset = exports.charset(mime)
    if (charset) mime += '; charset=' + charset.toLowerCase()
  }

  return mime
}

/**
 * Get the default extension for a MIME type.
 *
 * @param {string} type
 * @return {boolean|string}
 */

function extension (type) {
  if (!type || typeof type !== 'string') {
    return false
  }

  // TODO: use media-typer
  var match = EXTRACT_TYPE_REGEXP.exec(type)

  // get extensions
  var exts = match && exports.extensions[match[1].toLowerCase()]

  if (!exts || !exts.length) {
    return false
  }

  return exts[0]
}

/**
 * Lookup the MIME type for a file path/extension.
 *
 * @param {string} path
 * @return {boolean|string}
 */

function lookup (path) {
  if (!path || typeof path !== 'string') {
    return false
  }

  // get the extension ("ext" or ".ext" or full path)
  var extension = extname('x.' + path)
    .toLowerCase()
    .substr(1)

  if (!extension) {
    return false
  }

  return exports.types[extension] || false
}

/**
 * Populate the extensions and types maps.
 * @private
 */

function populateMaps (extensions, types) {
  // source preference (least -> most)
  var preference = ['nginx', 'apache', undefined, 'iana']

  Object.keys(db).forEach(function forEachMimeType (type) {
    var mime = db[type]
    var exts = mime.extensions

    if (!exts || !exts.length) {
      return
    }

    // mime -> extensions
    extensions[type] = exts

    // extension -> mime
    for (var i = 0; i < exts.length; i++) {
      var extension = exts[i]

      if (types[extension]) {
        var from = preference.indexOf(db[types[extension]].source)
        var to = preference.indexOf(mime.source)

        if (types[extension] !== 'application/octet-stream' &&
          (from > to || (from === to && types[extension].substr(0, 12) === 'application/'))) {
          // skip the remapping
          continue
        }
      }

      // set the extension -> mime
      types[extension] = type
    }
  })
}

```

### node_modules/buffer-fill/index.js

```javascript
/* Node.js 6.4.0 and up has full support */
var hasFullSupport = (function () {
  try {
    if (!Buffer.isEncoding('latin1')) {
      return false
    }

    var buf = Buffer.alloc ? Buffer.alloc(4) : new Buffer(4)

    buf.fill('ab', 'ucs2')

    return (buf.toString('hex') === '61006200')
  } catch (_) {
    return false
  }
}())

function isSingleByte (val) {
  return (val.length === 1 && val.charCodeAt(0) < 256)
}

function fillWithNumber (buffer, val, start, end) {
  if (start < 0 || end > buffer.length) {
    throw new RangeError('Out of range index')
  }

  start = start >>> 0
  end = end === undefined ? buffer.length : end >>> 0

  if (end > start) {
    buffer.fill(val, start, end)
  }

  return buffer
}

function fillWithBuffer (buffer, val, start, end) {
  if (start < 0 || end > buffer.length) {
    throw new RangeError('Out of range index')
  }

  if (end <= start) {
    return buffer
  }

  start = start >>> 0
  end = end === undefined ? buffer.length : end >>> 0

  var pos = start
  var len = val.length
  while (pos <= (end - len)) {
    val.copy(buffer, pos)
    pos += len
  }

  if (pos !== end) {
    val.copy(buffer, pos, 0, end - pos)
  }

  return buffer
}

function fill (buffer, val, start, end, encoding) {
  if (hasFullSupport) {
    return buffer.fill(val, start, end, encoding)
  }

  if (typeof val === 'number') {
    return fillWithNumber(buffer, val, start, end)
  }

  if (typeof val === 'string') {
    if (typeof start === 'string') {
      encoding = start
      start = 0
      end = buffer.length
    } else if (typeof end === 'string') {
      encoding = end
      end = buffer.length
    }

    if (encoding !== undefined && typeof encoding !== 'string') {
      throw new TypeError('encoding must be a string')
    }

    if (encoding === 'latin1') {
      encoding = 'binary'
    }

    if (typeof encoding === 'string' && !Buffer.isEncoding(encoding)) {
      throw new TypeError('Unknown encoding: ' + encoding)
    }

    if (val === '') {
      return fillWithNumber(buffer, 0, start, end)
    }

    if (isSingleByte(val)) {
      return fillWithNumber(buffer, val.charCodeAt(0), start, end)
    }

    val = new Buffer(val, encoding)
  }

  if (Buffer.isBuffer(val)) {
    return fillWithBuffer(buffer, val, start, end)
  }

  // Other values (e.g. undefined, boolean, object) results in zero-fill
  return fillWithNumber(buffer, 0, start, end)
}

module.exports = fill

```

### node_modules/asynckit/index.js

```javascript
module.exports =
{
  parallel      : require('./parallel.js'),
  serial        : require('./serial.js'),
  serialOrdered : require('./serialOrdered.js')
};

```

### node_modules/stream-parser/index.js

```javascript

/**
 * Module dependencies.
 */

var assert = require('assert');
var debug = require('debug')('stream-parser');

/**
 * Module exports.
 */

module.exports = Parser;

/**
 * Parser states.
 */

var INIT        = -1;
var BUFFERING   = 0;
var SKIPPING    = 1;
var PASSTHROUGH = 2;

/**
 * The `Parser` stream mixin works with either `Writable` or `Transform` stream
 * instances/subclasses. Provides a convenient generic "parsing" API:
 *
 *   _bytes(n, cb) - buffers "n" bytes and then calls "cb" with the "chunk"
 *   _skipBytes(n, cb) - skips "n" bytes and then calls "cb" when done
 *
 * If you extend a `Transform` stream, then the `_passthrough()` function is also
 * added:
 *
 *   _passthrough(n, cb) - passes through "n" bytes untouched and then calls "cb"
 *
 * @param {Stream} stream Transform or Writable stream instance to extend
 * @api public
 */

function Parser (stream) {
  var isTransform = stream && 'function' == typeof stream._transform;
  var isWritable = stream && 'function' == typeof stream._write;

  if (!isTransform && !isWritable) throw new Error('must pass a Writable or Transform stream in');
  debug('extending Parser into stream');

  // Transform streams and Writable streams get `_bytes()` and `_skipBytes()`
  stream._bytes = _bytes;
  stream._skipBytes = _skipBytes;

  // only Transform streams get the `_passthrough()` function
  if (isTransform) stream._passthrough = _passthrough;

  // take control of the streams2 callback functions for this stream
  if (isTransform) {
    stream._transform = transform;
  } else {
    stream._write = write;
  }
}

function init (stream) {
  debug('initializing parser stream');

  // number of bytes left to parser for the next "chunk"
  stream._parserBytesLeft = 0;

  // array of Buffer instances that make up the next "chunk"
  stream._parserBuffers = [];

  // number of bytes parsed so far for the next "chunk"
  stream._parserBuffered = 0;

  // flag that keeps track of if what the parser should do with bytes received
  stream._parserState = INIT;

  // the callback for the next "chunk"
  stream._parserCallback = null;

  // XXX: backwards compat with the old Transform API... remove at some point..
  if ('function' == typeof stream.push) {
    stream._parserOutput = stream.push.bind(stream);
  }

  stream._parserInit = true;
}

/**
 * Buffers `n` bytes and then invokes `fn` once that amount has been collected.
 *
 * @param {Number} n the number of bytes to buffer
 * @param {Function} fn callback function to invoke when `n` bytes are buffered
 * @api public
 */

function _bytes (n, fn) {
  assert(!this._parserCallback, 'there is already a "callback" set!');
  assert(isFinite(n) && n > 0, 'can only buffer a finite number of bytes > 0, got "' + n + '"');
  if (!this._parserInit) init(this);
  debug('buffering %o bytes', n);
  this._parserBytesLeft = n;
  this._parserCallback = fn;
  this._parserState = BUFFERING;
}

/**
 * Skips over the next `n` bytes, then invokes `fn` once that amount has
 * been discarded.
 *
 * @param {Number} n the number of bytes to discard
 * @param {Function} fn callback function to invoke when `n` bytes have been skipped
 * @api public
 */

function _skipBytes (n, fn) {
  assert(!this._parserCallback, 'there is already a "callback" set!');
  assert(n > 0, 'can only skip > 0 bytes, got "' + n + '"');
  if (!this._parserInit) init(this);
  debug('skipping %o bytes', n);
  this._parserBytesLeft = n;
  this._parserCallback = fn;
  this._parserState = SKIPPING;
}

/**
 * Passes through `n` bytes to the readable side of this stream untouched,
 * then invokes `fn` once that amount has been passed through.
 *
 * @param {Number} n the number of bytes to pass through
 * @param {Function} fn callback function to invoke when `n` bytes have passed through
 * @api public
 */

function _passthrough (n, fn) {
  assert(!this._parserCallback, 'There is already a "callback" set!');
  assert(n > 0, 'can only pass through > 0 bytes, got "' + n + '"');
  if (!this._parserInit) init(this);
  debug('passing through %o bytes', n);
  this._parserBytesLeft = n;
  this._parserCallback = fn;
  this._parserState = PASSTHROUGH;
}

/**
 * The `_write()` callback function implementation.
 *
 * @api private
 */

function write (chunk, encoding, fn) {
  if (!this._parserInit) init(this);
  debug('write(%o bytes)', chunk.length);

  // XXX: old Writable stream API compat... remove at some point...
  if ('function' == typeof encoding) fn = encoding;

  data(this, chunk, null, fn);
}

/**
 * The `_transform()` callback function implementation.
 *
 * @api private
 */


function transform (chunk, output, fn) {
  if (!this._parserInit) init(this);
  debug('transform(%o bytes)', chunk.length);

  // XXX: old Transform stream API compat... remove at some point...
  if ('function' != typeof output) {
    output = this._parserOutput;
  }

  data(this, chunk, output, fn);
}

/**
 * The internal buffering/passthrough logic...
 *
 * This `_data` function get's "trampolined" to prevent stack overflows for tight
 * loops. This technique requires us to return a "thunk" function for any
 * synchronous action. Async stuff breaks the trampoline, but that's ok since it's
 * working with a new stack at that point anyway.
 *
 * @api private
 */

function _data (stream, chunk, output, fn) {
  if (stream._parserBytesLeft <= 0) {
    return fn(new Error('got data but not currently parsing anything'));
  }

  if (chunk.length <= stream._parserBytesLeft) {
    // small buffer fits within the "_parserBytesLeft" window
    return function () {
      return process(stream, chunk, output, fn);
    };
  } else {
    // large buffer needs to be sliced on "_parserBytesLeft" and processed
    return function () {
      var b = chunk.slice(0, stream._parserBytesLeft);
      return process(stream, b, output, function (err) {
        if (err) return fn(err);
        if (chunk.length > b.length) {
          return function () {
            return _data(stream, chunk.slice(b.length), output, fn);
          };
        }
      });
    };
  }
}

/**
 * The internal `process` function gets called by the `data` function when
 * something "interesting" happens. This function takes care of buffering the
 * bytes when buffering, passing through the bytes when doing that, and invoking
 * the user callback when the number of bytes has been reached.
 *
 * @api private
 */

function process (stream, chunk, output, fn) {
  stream._parserBytesLeft -= chunk.length;
  debug('%o bytes left for stream piece', stream._parserBytesLeft);

  if (stream._parserState === BUFFERING) {
    // buffer
    stream._parserBuffers.push(chunk);
    stream._parserBuffered += chunk.length;
  } else if (stream._parserState === PASSTHROUGH) {
    // passthrough
    output(chunk);
  }
  // don't need to do anything for the SKIPPING case

  if (0 === stream._parserBytesLeft) {
    // done with stream "piece", invoke the callback
    var cb = stream._parserCallback;
    if (cb && stream._parserState === BUFFERING && stream._parserBuffers.length > 1) {
      chunk = Buffer.concat(stream._parserBuffers, stream._parserBuffered);
    }
    if (stream._parserState !== BUFFERING) {
      chunk = null;
    }
    stream._parserCallback = null;
    stream._parserBuffered = 0;
    stream._parserState = INIT;
    stream._parserBuffers.splice(0); // empty

    if (cb) {
      var args = [];
      if (chunk) {
        // buffered
        args.push(chunk);
      } else {
        // passthrough
      }
      if (output) {
        // on a Transform stream, has "output" function
        args.push(output);
      }
      var async = cb.length > args.length;
      if (async) {
        args.push(trampoline(fn));
      }
      // invoke cb
      var rtn = cb.apply(stream, args);
      if (!async || fn === rtn) return fn;
    }
  } else {
    // need more bytes
    return fn;
  }
}

var data = trampoline(_data);

/**
 * Generic thunk-based "trampoline" helper function.
 *
 * @param {Function} input function
 * @return {Function} "trampolined" function
 * @api private
 */

function trampoline (fn) {
  return function () {
    var result = fn.apply(this, arguments);

    while ('function' == typeof result) {
      result = result();
    }

    return result;
  };
}

```

### node_modules/follow-redirects/index.js

```javascript
var url = require("url");
var URL = url.URL;
var http = require("http");
var https = require("https");
var Writable = require("stream").Writable;
var assert = require("assert");
var debug = require("./debug");

// Whether to use the native URL object or the legacy url module
var useNativeURL = false;
try {
  assert(new URL());
}
catch (error) {
  useNativeURL = error.code === "ERR_INVALID_URL";
}

// URL fields to preserve in copy operations
var preservedUrlFields = [
  "auth",
  "host",
  "hostname",
  "href",
  "path",
  "pathname",
  "port",
  "protocol",
  "query",
  "search",
  "hash",
];

// Create handlers that pass events from native requests
var events = ["abort", "aborted", "connect", "error", "socket", "timeout"];
var eventHandlers = Object.create(null);
events.forEach(function (event) {
  eventHandlers[event] = function (arg1, arg2, arg3) {
    this._redirectable.emit(event, arg1, arg2, arg3);
  };
});

// Error types with codes
var InvalidUrlError = createErrorType(
  "ERR_INVALID_URL",
  "Invalid URL",
  TypeError
);
var RedirectionError = createErrorType(
  "ERR_FR_REDIRECTION_FAILURE",
  "Redirected request failed"
);
var TooManyRedirectsError = createErrorType(
  "ERR_FR_TOO_MANY_REDIRECTS",
  "Maximum number of redirects exceeded",
  RedirectionError
);
var MaxBodyLengthExceededError = createErrorType(
  "ERR_FR_MAX_BODY_LENGTH_EXCEEDED",
  "Request body larger than maxBodyLength limit"
);
var WriteAfterEndError = createErrorType(
  "ERR_STREAM_WRITE_AFTER_END",
  "write after end"
);

// istanbul ignore next
var destroy = Writable.prototype.destroy || noop;

// An HTTP(S) request that can be redirected
function RedirectableRequest(options, responseCallback) {
  // Initialize the request
  Writable.call(this);
  this._sanitizeOptions(options);
  this._options = options;
  this._ended = false;
  this._ending = false;
  this._redirectCount = 0;
  this._redirects = [];
  this._requestBodyLength = 0;
  this._requestBodyBuffers = [];

  // Attach a callback if passed
  if (responseCallback) {
    this.on("response", responseCallback);
  }

  // React to responses of native requests
  var self = this;
  this._onNativeResponse = function (response) {
    try {
      self._processResponse(response);
    }
    catch (cause) {
      self.emit("error", cause instanceof RedirectionError ?
        cause : new RedirectionError({ cause: cause }));
    }
  };

  // Perform the first request
  this._performRequest();
}
RedirectableRequest.prototype = Object.create(Writable.prototype);

RedirectableRequest.prototype.abort = function () {
  destroyRequest(this._currentRequest);
  this._currentRequest.abort();
  this.emit("abort");
};

RedirectableRequest.prototype.destroy = function (error) {
  destroyRequest(this._currentRequest, error);
  destroy.call(this, error);
  return this;
};

// Writes buffered data to the current native request
RedirectableRequest.prototype.write = function (data, encoding, callback) {
  // Writing is not allowed if end has been called
  if (this._ending) {
    throw new WriteAfterEndError();
  }

  // Validate input and shift parameters if necessary
  if (!isString(data) && !isBuffer(data)) {
    throw new TypeError("data should be a string, Buffer or Uint8Array");
  }
  if (isFunction(encoding)) {
    callback = encoding;
    encoding = null;
  }

  // Ignore empty buffers, since writing them doesn't invoke the callback
  // https://github.com/nodejs/node/issues/22066
  if (data.length === 0) {
    if (callback) {
      callback();
    }
    return;
  }
  // Only write when we don't exceed the maximum body length
  if (this._requestBodyLength + data.length <= this._options.maxBodyLength) {
    this._requestBodyLength += data.length;
    this._requestBodyBuffers.push({ data: data, encoding: encoding });
    this._currentRequest.write(data, encoding, callback);
  }
  // Error when we exceed the maximum body length
  else {
    this.emit("error", new MaxBodyLengthExceededError());
    this.abort();
  }
};

// Ends the current native request
RedirectableRequest.prototype.end = function (data, encoding, callback) {
  // Shift parameters if necessary
  if (isFunction(data)) {
    callback = data;
    data = encoding = null;
  }
  else if (isFunction(encoding)) {
    callback = encoding;
    encoding = null;
  }

  // Write data if needed and end
  if (!data) {
    this._ended = this._ending = true;
    this._currentRequest.end(null, null, callback);
  }
  else {
    var self = this;
    var currentRequest = this._currentRequest;
    this.write(data, encoding, function () {
      self._ended = true;
      currentRequest.end(null, null, callback);
    });
    this._ending = true;
  }
};

// Sets a header value on the current native request
RedirectableRequest.prototype.setHeader = function (name, value) {
  this._options.headers[name] = value;
  this._currentRequest.setHeader(name, value);
};

// Clears a header value on the current native request
RedirectableRequest.prototype.removeHeader = function (name) {
  delete this._options.headers[name];
  this._currentRequest.removeHeader(name);
};

// Global timeout for all underlying requests
RedirectableRequest.prototype.setTimeout = function (msecs, callback) {
  var self = this;

  // Destroys the socket on timeout
  function destroyOnTimeout(socket) {
    socket.setTimeout(msecs);
    socket.removeListener("timeout", socket.destroy);
    socket.addListener("timeout", socket.destroy);
  }

  // Sets up a timer to trigger a timeout event
  function startTimer(socket) {
    if (self._timeout) {
      clearTimeout(self._timeout);
    }
    self._timeout = setTimeout(function () {
      self.emit("timeout");
      clearTimer();
    }, msecs);
    destroyOnTimeout(socket);
  }

  // Stops a timeout from triggering
  function clearTimer() {
    // Clear the timeout
    if (self._timeout) {
      clearTimeout(self._timeout);
      self._timeout = null;
    }

    // Clean up all attached listeners
    self.removeListener("abort", clearTimer);
    self.removeListener("error", clearTimer);
    self.removeListener("response", clearTimer);
    self.removeListener("close", clearTimer);
    if (callback) {
      self.removeListener("timeout", callback);
    }
    if (!self.socket) {
      self._currentRequest.removeListener("socket", startTimer);
    }
  }

  // Attach callback if passed
  if (callback) {
    this.on("timeout", callback);
  }

  // Start the timer if or when the socket is opened
  if (this.socket) {
    startTimer(this.socket);
  }
  else {
    this._currentRequest.once("socket", startTimer);
  }

  // Clean up on events
  this.on("socket", destroyOnTimeout);
  this.on("abort", clearTimer);
  this.on("error", clearTimer);
  this.on("response", clearTimer);
  this.on("close", clearTimer);

  return this;
};

// Proxy all other public ClientRequest methods
[
  "flushHeaders", "getHeader",
  "setNoDelay", "setSocketKeepAlive",
].forEach(function (method) {
  RedirectableRequest.prototype[method] = function (a, b) {
    return this._currentRequest[method](a, b);
  };
});

// Proxy all public ClientRequest properties
["aborted", "connection", "socket"].forEach(function (property) {
  Object.defineProperty(RedirectableRequest.prototype, property, {
    get: function () { return this._currentRequest[property]; },
  });
});

RedirectableRequest.prototype._sanitizeOptions = function (options) {
  // Ensure headers are always present
  if (!options.headers) {
    options.headers = {};
  }

  // Since http.request treats host as an alias of hostname,
  // but the url module interprets host as hostname plus port,
  // eliminate the host property to avoid confusion.
  if (options.host) {
    // Use hostname if set, because it has precedence
    if (!options.hostname) {
      options.hostname = options.host;
    }
    delete options.host;
  }

  // Complete the URL object when necessary
  if (!options.pathname && options.path) {
    var searchPos = options.path.indexOf("?");
    if (searchPos < 0) {
      options.pathname = options.path;
    }
    else {
      options.pathname = options.path.substring(0, searchPos);
      options.search = options.path.substring(searchPos);
    }
  }
};


// Executes the next native request (initial or redirect)
RedirectableRequest.prototype._performRequest = function () {
  // Load the native protocol
  var protocol = this._options.protocol;
  var nativeProtocol = this._options.nativeProtocols[protocol];
  if (!nativeProtocol) {
    throw new TypeError("Unsupported protocol " + protocol);
  }

  // If specified, use the agent corresponding to the protocol
  // (HTTP and HTTPS use different types of agents)
  if (this._options.agents) {
    var scheme = protocol.slice(0, -1);
    this._options.agent = this._options.agents[scheme];
  }

  // Create the native request and set up its event handlers
  var request = this._currentRequest =
        nativeProtocol.request(this._options, this._onNativeResponse);
  request._redirectable = this;
  for (var event of events) {
    request.on(event, eventHandlers[event]);
  }

  // RFC7230§5.3.1: When making a request directly to an origin server, […]
  // a client MUST send only the absolute path […] as the request-target.
  this._currentUrl = /^\//.test(this._options.path) ?
    url.format(this._options) :
    // When making a request to a proxy, […]
    // a client MUST send the target URI in absolute-form […].
    this._options.path;

  // End a redirected request
  // (The first request must be ended explicitly with RedirectableRequest#end)
  if (this._isRedirect) {
    // Write the request entity and end
    var i = 0;
    var self = this;
    var buffers = this._requestBodyBuffers;
    (function writeNext(error) {
      // Only write if this request has not been redirected yet
      /* istanbul ignore else */
      if (request === self._currentRequest) {
        // Report any write errors
        /* istanbul ignore if */
        if (error) {
          self.emit("error", error);
        }
        // Write the next buffer if there are still left
        else if (i < buffers.length) {
          var buffer = buffers[i++];
          /* istanbul ignore else */
          if (!request.finished) {
            request.write(buffer.data, buffer.encoding, writeNext);
          }
        }
        // End the request if `end` has been called on us
        else if (self._ended) {
          request.end();
        }
      }
    }());
  }
};

// Processes a response from the current native request
RedirectableRequest.prototype._processResponse = function (response) {
  // Store the redirected response
  var statusCode = response.statusCode;
  if (this._options.trackRedirects) {
    this._redirects.push({
      url: this._currentUrl,
      headers: response.headers,
      statusCode: statusCode,
    });
  }

  // RFC7231§6.4: The 3xx (Redirection) class of status code indicates
  // that further action needs to be taken by the user agent in order to
  // fulfill the request. If a Location header field is provided,
  // the user agent MAY automatically redirect its request to the URI
  // referenced by the Location field value,
  // even if the specific status code is not understood.

  // If the response is not a redirect; return it as-is
  var location = response.headers.location;
  if (!location || this._options.followRedirects === false ||
      statusCode < 300 || statusCode >= 400) {
    response.responseUrl = this._currentUrl;
    response.redirects = this._redirects;
    this.emit("response", response);

    // Clean up
    this._requestBodyBuffers = [];
    return;
  }

  // The response is a redirect, so abort the current request
  destroyRequest(this._currentRequest);
  // Discard the remainder of the response to avoid waiting for data
  response.destroy();

  // RFC7231§6.4: A client SHOULD detect and intervene
  // in cyclical redirections (i.e., "infinite" redirection loops).
  if (++this._redirectCount > this._options.maxRedirects) {
    throw new TooManyRedirectsError();
  }

  // Store the request headers if applicable
  var requestHeaders;
  var beforeRedirect = this._options.beforeRedirect;
  if (beforeRedirect) {
    requestHeaders = Object.assign({
      // The Host header was set by nativeProtocol.request
      Host: response.req.getHeader("host"),
    }, this._options.headers);
  }

  // RFC7231§6.4: Automatic redirection needs to done with
  // care for methods not known to be safe, […]
  // RFC7231§6.4.2–3: For historical reasons, a user agent MAY change
  // the request method from POST to GET for the subsequent request.
  var method = this._options.method;
  if ((statusCode === 301 || statusCode === 302) && this._options.method === "POST" ||
      // RFC7231§6.4.4: The 303 (See Other) status code indicates that
      // the server is redirecting the user agent to a different resource […]
      // A user agent can perform a retrieval request targeting that URI
      // (a GET or HEAD request if using HTTP) […]
      (statusCode === 303) && !/^(?:GET|HEAD)$/.test(this._options.method)) {
    this._options.method = "GET";
    // Drop a possible entity and headers related to it
    this._requestBodyBuffers = [];
    removeMatchingHeaders(/^content-/i, this._options.headers);
  }

  // Drop the Host header, as the redirect might lead to a different host
  var currentHostHeader = removeMatchingHeaders(/^host$/i, this._options.headers);

  // If the redirect is relative, carry over the host of the last request
  var currentUrlParts = parseUrl(this._currentUrl);
  var currentHost = currentHostHeader || currentUrlParts.host;
  var currentUrl = /^\w+:/.test(location) ? this._currentUrl :
    url.format(Object.assign(currentUrlParts, { host: currentHost }));

  // Create the redirected request
  var redirectUrl = resolveUrl(location, currentUrl);
  debug("redirecting to", redirectUrl.href);
  this._isRedirect = true;
  spreadUrlObject(redirectUrl, this._options);

  // Drop confidential headers when redirecting to a less secure protocol
  // or to a different domain that is not a superdomain
  if (redirectUrl.protocol !== currentUrlParts.protocol &&
     redirectUrl.protocol !== "https:" ||
     redirectUrl.host !== currentHost &&
     !isSubdomain(redirectUrl.host, currentHost)) {
    removeMatchingHeaders(/^(?:(?:proxy-)?authorization|cookie)$/i, this._options.headers);
  }

  // Evaluate the beforeRedirect callback
  if (isFunction(beforeRedirect)) {
    var responseDetails = {
      headers: response.headers,
      statusCode: statusCode,
    };
    var requestDetails = {
      url: currentUrl,
      method: method,
      headers: requestHeaders,
    };
    beforeRedirect(this._options, responseDetails, requestDetails);
    this._sanitizeOptions(this._options);
  }

  // Perform the redirected request
  this._performRequest();
};

// Wraps the key/value object of protocols with redirect functionality
function wrap(protocols) {
  // Default settings
  var exports = {
    maxRedirects: 21,
    maxBodyLength: 10 * 1024 * 1024,
  };

  // Wrap each protocol
  var nativeProtocols = {};
  Object.keys(protocols).forEach(function (scheme) {
    var protocol = scheme + ":";
    var nativeProtocol = nativeProtocols[protocol] = protocols[scheme];
    var wrappedProtocol = exports[scheme] = Object.create(nativeProtocol);

    // Executes a request, following redirects
    function request(input, options, callback) {
      // Parse parameters, ensuring that input is an object
      if (isURL(input)) {
        input = spreadUrlObject(input);
      }
      else if (isString(input)) {
        input = spreadUrlObject(parseUrl(input));
      }
      else {
        callback = options;
        options = validateUrl(input);
        input = { protocol: protocol };
      }
      if (isFunction(options)) {
        callback = options;
        options = null;
      }

      // Set defaults
      options = Object.assign({
        maxRedirects: exports.maxRedirects,
        maxBodyLength: exports.maxBodyLength,
      }, input, options);
      options.nativeProtocols = nativeProtocols;
      if (!isString(options.host) && !isString(options.hostname)) {
        options.hostname = "::1";
      }

      assert.equal(options.protocol, protocol, "protocol mismatch");
      debug("options", options);
      return new RedirectableRequest(options, callback);
    }

    // Executes a GET request, following redirects
    function get(input, options, callback) {
      var wrappedRequest = wrappedProtocol.request(input, options, callback);
      wrappedRequest.end();
      return wrappedRequest;
    }

    // Expose the properties on the wrapped protocol
    Object.defineProperties(wrappedProtocol, {
      request: { value: request, configurable: true, enumerable: true, writable: true },
      get: { value: get, configurable: true, enumerable: true, writable: true },
    });
  });
  return exports;
}

function noop() { /* empty */ }

function parseUrl(input) {
  var parsed;
  /* istanbul ignore else */
  if (useNativeURL) {
    parsed = new URL(input);
  }
  else {
    // Ensure the URL is valid and absolute
    parsed = validateUrl(url.parse(input));
    if (!isString(parsed.protocol)) {
      throw new InvalidUrlError({ input });
    }
  }
  return parsed;
}

function resolveUrl(relative, base) {
  /* istanbul ignore next */
  return useNativeURL ? new URL(relative, base) : parseUrl(url.resolve(base, relative));
}

function validateUrl(input) {
  if (/^\[/.test(input.hostname) && !/^\[[:0-9a-f]+\]$/i.test(input.hostname)) {
    throw new InvalidUrlError({ input: input.href || input });
  }
  if (/^\[/.test(input.host) && !/^\[[:0-9a-f]+\](:\d+)?$/i.test(input.host)) {
    throw new InvalidUrlError({ input: input.href || input });
  }
  return input;
}

function spreadUrlObject(urlObject, target) {
  var spread = target || {};
  for (var key of preservedUrlFields) {
    spread[key] = urlObject[key];
  }

  // Fix IPv6 hostname
  if (spread.hostname.startsWith("[")) {
    spread.hostname = spread.hostname.slice(1, -1);
  }
  // Ensure port is a number
  if (spread.port !== "") {
    spread.port = Number(spread.port);
  }
  // Concatenate path
  spread.path = spread.search ? spread.pathname + spread.search : spread.pathname;

  return spread;
}

function removeMatchingHeaders(regex, headers) {
  var lastValue;
  for (var header in headers) {
    if (regex.test(header)) {
      lastValue = headers[header];
      delete headers[header];
    }
  }
  return (lastValue === null || typeof lastValue === "undefined") ?
    undefined : String(lastValue).trim();
}

function createErrorType(code, message, baseClass) {
  // Create constructor
  function CustomError(properties) {
    Error.captureStackTrace(this, this.constructor);
    Object.assign(this, properties || {});
    this.code = code;
    this.message = this.cause ? message + ": " + this.cause.message : message;
  }

  // Attach constructor and set default properties
  CustomError.prototype = new (baseClass || Error)();
  Object.defineProperties(CustomError.prototype, {
    constructor: {
      value: CustomError,
      enumerable: false,
    },
    name: {
      value: "Error [" + code + "]",
      enumerable: false,
    },
  });
  return CustomError;
}

function destroyRequest(request, error) {
  for (var event of events) {
    request.removeListener(event, eventHandlers[event]);
  }
  request.on("error", noop);
  request.destroy(error);
}

function isSubdomain(subdomain, domain) {
  assert(isString(subdomain) && isString(domain));
  var dot = subdomain.length - domain.length - 1;
  return dot > 0 && subdomain[dot] === "." && subdomain.endsWith(domain);
}

function isString(value) {
  return typeof value === "string" || value instanceof String;
}

function isFunction(value) {
  return typeof value === "function";
}

function isBuffer(value) {
  return typeof value === "object" && ("length" in value);
}

function isURL(value) {
  return URL && value instanceof URL;
}

// Exports
module.exports = wrap({ http: http, https: https });
module.exports.wrap = wrap;

```

### node_modules/isarray/index.js

```javascript
module.exports = Array.isArray || function (arr) {
  return Object.prototype.toString.call(arr) == '[object Array]';
};

```

### node_modules/data-uri-to-buffer/dist/index.js

```javascript
/**
 * Returns a `Buffer` instance from the given data URI `uri`.
 *
 * @param {String} uri Data URI to turn into a Buffer instance
 * @returns {Buffer} Buffer instance from Data URI
 * @api public
 */
export function dataUriToBuffer(uri) {
    if (!/^data:/i.test(uri)) {
        throw new TypeError('`uri` does not appear to be a Data URI (must begin with "data:")');
    }
    // strip newlines
    uri = uri.replace(/\r?\n/g, '');
    // split the URI up into the "metadata" and the "data" portions
    const firstComma = uri.indexOf(',');
    if (firstComma === -1 || firstComma <= 4) {
        throw new TypeError('malformed data: URI');
    }
    // remove the "data:" scheme and parse the metadata
    const meta = uri.substring(5, firstComma).split(';');
    let charset = '';
    let base64 = false;
    const type = meta[0] || 'text/plain';
    let typeFull = type;
    for (let i = 1; i < meta.length; i++) {
        if (meta[i] === 'base64') {
            base64 = true;
        }
        else if (meta[i]) {
            typeFull += `;${meta[i]}`;
            if (meta[i].indexOf('charset=') === 0) {
                charset = meta[i].substring(8);
            }
        }
    }
    // defaults to US-ASCII only if type is not provided
    if (!meta[0] && !charset.length) {
        typeFull += ';charset=US-ASCII';
        charset = 'US-ASCII';
    }
    // get the encoded data portion and decode URI-encoded chars
    const encoding = base64 ? 'base64' : 'ascii';
    const data = unescape(uri.substring(firstComma + 1));
    const buffer = Buffer.from(data, encoding);
    // set `.type` and `.typeFull` properties to MIME type
    buffer.type = type;
    buffer.typeFull = typeFull;
    // set the `.charset` property
    buffer.charset = charset;
    return buffer;
}
export default dataUriToBuffer;
//# sourceMappingURL=index.js.map
```

### node_modules/fetch-blob/index.js

```javascript
/*! fetch-blob. MIT License. Jimmy Wärting <https://jimmy.warting.se/opensource> */

// TODO (jimmywarting): in the feature use conditional loading with top level await (requires 14.x)
// Node has recently added whatwg stream into core

import './streams.cjs'

// 64 KiB (same size chrome slice theirs blob into Uint8array's)
const POOL_SIZE = 65536

/** @param {(Blob | Uint8Array)[]} parts */
async function * toIterator (parts, clone = true) {
  for (const part of parts) {
    if ('stream' in part) {
      yield * (/** @type {AsyncIterableIterator<Uint8Array>} */ (part.stream()))
    } else if (ArrayBuffer.isView(part)) {
      if (clone) {
        let position = part.byteOffset
        const end = part.byteOffset + part.byteLength
        while (position !== end) {
          const size = Math.min(end - position, POOL_SIZE)
          const chunk = part.buffer.slice(position, position + size)
          position += chunk.byteLength
          yield new Uint8Array(chunk)
        }
      } else {
        yield part
      }
    /* c8 ignore next 10 */
    } else {
      // For blobs that have arrayBuffer but no stream method (nodes buffer.Blob)
      let position = 0, b = (/** @type {Blob} */ (part))
      while (position !== b.size) {
        const chunk = b.slice(position, Math.min(b.size, position + POOL_SIZE))
        const buffer = await chunk.arrayBuffer()
        position += buffer.byteLength
        yield new Uint8Array(buffer)
      }
    }
  }
}

const _Blob = class Blob {
  /** @type {Array.<(Blob|Uint8Array)>} */
  #parts = []
  #type = ''
  #size = 0
  #endings = 'transparent'

  /**
   * The Blob() constructor returns a new Blob object. The content
   * of the blob consists of the concatenation of the values given
   * in the parameter array.
   *
   * @param {*} blobParts
   * @param {{ type?: string, endings?: string }} [options]
   */
  constructor (blobParts = [], options = {}) {
    if (typeof blobParts !== 'object' || blobParts === null) {
      throw new TypeError('Failed to construct \'Blob\': The provided value cannot be converted to a sequence.')
    }

    if (typeof blobParts[Symbol.iterator] !== 'function') {
      throw new TypeError('Failed to construct \'Blob\': The object must have a callable @@iterator property.')
    }

    if (typeof options !== 'object' && typeof options !== 'function') {
      throw new TypeError('Failed to construct \'Blob\': parameter 2 cannot convert to dictionary.')
    }

    if (options === null) options = {}

    const encoder = new TextEncoder()
    for (const element of blobParts) {
      let part
      if (ArrayBuffer.isView(element)) {
        part = new Uint8Array(element.buffer.slice(element.byteOffset, element.byteOffset + element.byteLength))
      } else if (element instanceof ArrayBuffer) {
        part = new Uint8Array(element.slice(0))
      } else if (element instanceof Blob) {
        part = element
      } else {
        part = encoder.encode(`${element}`)
      }

      this.#size += ArrayBuffer.isView(part) ? part.byteLength : part.size
      this.#parts.push(part)
    }

    this.#endings = `${options.endings === undefined ? 'transparent' : options.endings}`
    const type = options.type === undefined ? '' : String(options.type)
    this.#type = /^[\x20-\x7E]*$/.test(type) ? type : ''
  }

  /**
   * The Blob interface's size property returns the
   * size of the Blob in bytes.
   */
  get size () {
    return this.#size
  }

  /**
   * The type property of a Blob object returns the MIME type of the file.
   */
  get type () {
    return this.#type
  }

  /**
   * The text() method in the Blob interface returns a Promise
   * that resolves with a string containing the contents of
   * the blob, interpreted as UTF-8.
   *
   * @return {Promise<string>}
   */
  async text () {
    // More optimized than using this.arrayBuffer()
    // that requires twice as much ram
    const decoder = new TextDecoder()
    let str = ''
    for await (const part of toIterator(this.#parts, false)) {
      str += decoder.decode(part, { stream: true })
    }
    // Remaining
    str += decoder.decode()
    return str
  }

  /**
   * The arrayBuffer() method in the Blob interface returns a
   * Promise that resolves with the contents of the blob as
   * binary data contained in an ArrayBuffer.
   *
   * @return {Promise<ArrayBuffer>}
   */
  async arrayBuffer () {
    // Easier way... Just a unnecessary overhead
    // const view = new Uint8Array(this.size);
    // await this.stream().getReader({mode: 'byob'}).read(view);
    // return view.buffer;

    const data = new Uint8Array(this.size)
    let offset = 0
    for await (const chunk of toIterator(this.#parts, false)) {
      data.set(chunk, offset)
      offset += chunk.length
    }

    return data.buffer
  }

  stream () {
    const it = toIterator(this.#parts, true)

    return new globalThis.ReadableStream({
      // @ts-ignore
      type: 'bytes',
      async pull (ctrl) {
        const chunk = await it.next()
        chunk.done ? ctrl.close() : ctrl.enqueue(chunk.value)
      },

      async cancel () {
        await it.return()
      }
    })
  }

  /**
   * The Blob interface's slice() method creates and returns a
   * new Blob object which contains data from a subset of the
   * blob on which it's called.
   *
   * @param {number} [start]
   * @param {number} [end]
   * @param {string} [type]
   */
  slice (start = 0, end = this.size, type = '') {
    const { size } = this

    let relativeStart = start < 0 ? Math.max(size + start, 0) : Math.min(start, size)
    let relativeEnd = end < 0 ? Math.max(size + end, 0) : Math.min(end, size)

    const span = Math.max(relativeEnd - relativeStart, 0)
    const parts = this.#parts
    const blobParts = []
    let added = 0

    for (const part of parts) {
      // don't add the overflow to new blobParts
      if (added >= span) {
        break
      }

      const size = ArrayBuffer.isView(part) ? part.byteLength : part.size
      if (relativeStart && size <= relativeStart) {
        // Skip the beginning and change the relative
        // start & end position as we skip the unwanted parts
        relativeStart -= size
        relativeEnd -= size
      } else {
        let chunk
        if (ArrayBuffer.isView(part)) {
          chunk = part.subarray(relativeStart, Math.min(size, relativeEnd))
          added += chunk.byteLength
        } else {
          chunk = part.slice(relativeStart, Math.min(size, relativeEnd))
          added += chunk.size
        }
        relativeEnd -= size
        blobParts.push(chunk)
        relativeStart = 0 // All next sequential parts should start at 0
      }
    }

    const blob = new Blob([], { type: String(type).toLowerCase() })
    blob.#size = span
    blob.#parts = blobParts

    return blob
  }

  get [Symbol.toStringTag] () {
    return 'Blob'
  }

  static [Symbol.hasInstance] (object) {
    return (
      object &&
      typeof object === 'object' &&
      typeof object.constructor === 'function' &&
      (
        typeof object.stream === 'function' ||
        typeof object.arrayBuffer === 'function'
      ) &&
      /^(Blob|File)$/.test(object[Symbol.toStringTag])
    )
  }
}

Object.defineProperties(_Blob.prototype, {
  size: { enumerable: true },
  type: { enumerable: true },
  slice: { enumerable: true }
})

/** @type {typeof globalThis.Blob} */
export const Blob = _Blob
export default Blob

```

### node_modules/axios/index.js

```javascript
import axios from './lib/axios.js';

// This module is intended to unwrap Axios default export as named.
// Keep top-level export same with static properties
// so that it can keep same with es module or cjs
const {
  Axios,
  AxiosError,
  CanceledError,
  isCancel,
  CancelToken,
  VERSION,
  all,
  Cancel,
  isAxiosError,
  spread,
  toFormData,
  AxiosHeaders,
  HttpStatusCode,
  formToJSON,
  getAdapter,
  mergeConfig
} = axios;

export {
  axios as default,
  Axios,
  AxiosError,
  CanceledError,
  isCancel,
  CancelToken,
  VERSION,
  all,
  Cancel,
  isAxiosError,
  spread,
  toFormData,
  AxiosHeaders,
  HttpStatusCode,
  formToJSON,
  getAdapter,
  mergeConfig
}

```

### node_modules/axios/lib/platform/index.js

```javascript
import platform from './node/index.js';
import * as utils from './common/utils.js';

export default {
  ...utils,
  ...platform
}

```

### node_modules/axios/lib/platform/browser/index.js

```javascript
import URLSearchParams from './classes/URLSearchParams.js'
import FormData from './classes/FormData.js'
import Blob from './classes/Blob.js'

export default {
  isBrowser: true,
  classes: {
    URLSearchParams,
    FormData,
    Blob
  },
  protocols: ['http', 'https', 'file', 'blob', 'url', 'data']
};

```

### node_modules/axios/lib/platform/node/index.js

```javascript
import URLSearchParams from './classes/URLSearchParams.js'
import FormData from './classes/FormData.js'

export default {
  isNode: true,
  classes: {
    URLSearchParams,
    FormData,
    Blob: typeof Blob !== 'undefined' && Blob || null
  },
  protocols: [ 'http', 'https', 'file', 'data' ]
};

```

### node_modules/axios/lib/defaults/index.js

```javascript
'use strict';

import utils from '../utils.js';
import AxiosError from '../core/AxiosError.js';
import transitionalDefaults from './transitional.js';
import toFormData from '../helpers/toFormData.js';
import toURLEncodedForm from '../helpers/toURLEncodedForm.js';
import platform from '../platform/index.js';
import formDataToJSON from '../helpers/formDataToJSON.js';

/**
 * It takes a string, tries to parse it, and if it fails, it returns the stringified version
 * of the input
 *
 * @param {any} rawValue - The value to be stringified.
 * @param {Function} parser - A function that parses a string into a JavaScript object.
 * @param {Function} encoder - A function that takes a value and returns a string.
 *
 * @returns {string} A stringified version of the rawValue.
 */
function stringifySafely(rawValue, parser, encoder) {
  if (utils.isString(rawValue)) {
    try {
      (parser || JSON.parse)(rawValue);
      return utils.trim(rawValue);
    } catch (e) {
      if (e.name !== 'SyntaxError') {
        throw e;
      }
    }
  }

  return (encoder || JSON.stringify)(rawValue);
}

const defaults = {

  transitional: transitionalDefaults,

  adapter: ['xhr', 'http', 'fetch'],

  transformRequest: [function transformRequest(data, headers) {
    const contentType = headers.getContentType() || '';
    const hasJSONContentType = contentType.indexOf('application/json') > -1;
    const isObjectPayload = utils.isObject(data);

    if (isObjectPayload && utils.isHTMLForm(data)) {
      data = new FormData(data);
    }

    const isFormData = utils.isFormData(data);

    if (isFormData) {
      return hasJSONContentType ? JSON.stringify(formDataToJSON(data)) : data;
    }

    if (utils.isArrayBuffer(data) ||
      utils.isBuffer(data) ||
      utils.isStream(data) ||
      utils.isFile(data) ||
      utils.isBlob(data) ||
      utils.isReadableStream(data)
    ) {
      return data;
    }
    if (utils.isArrayBufferView(data)) {
      return data.buffer;
    }
    if (utils.isURLSearchParams(data)) {
      headers.setContentType('application/x-www-form-urlencoded;charset=utf-8', false);
      return data.toString();
    }

    let isFileList;

    if (isObjectPayload) {
      if (contentType.indexOf('application/x-www-form-urlencoded') > -1) {
        return toURLEncodedForm(data, this.formSerializer).toString();
      }

      if ((isFileList = utils.isFileList(data)) || contentType.indexOf('multipart/form-data') > -1) {
        const _FormData = this.env && this.env.FormData;

        return toFormData(
          isFileList ? {'files[]': data} : data,
          _FormData && new _FormData(),
          this.formSerializer
        );
      }
    }

    if (isObjectPayload || hasJSONContentType ) {
      headers.setContentType('application/json', false);
      return stringifySafely(data);
    }

    return data;
  }],

  transformResponse: [function transformResponse(data) {
    const transitional = this.transitional || defaults.transitional;
    const forcedJSONParsing = transitional && transitional.forcedJSONParsing;
    const JSONRequested = this.responseType === 'json';

    if (utils.isResponse(data) || utils.isReadableStream(data)) {
      return data;
    }

    if (data && utils.isString(data) && ((forcedJSONParsing && !this.responseType) || JSONRequested)) {
      const silentJSONParsing = transitional && transitional.silentJSONParsing;
      const strictJSONParsing = !silentJSONParsing && JSONRequested;

      try {
        return JSON.parse(data);
      } catch (e) {
        if (strictJSONParsing) {
          if (e.name === 'SyntaxError') {
            throw AxiosError.from(e, AxiosError.ERR_BAD_RESPONSE, this, null, this.response);
          }
          throw e;
        }
      }
    }

    return data;
  }],

  /**
   * A timeout in milliseconds to abort a request. If set to 0 (default) a
   * timeout is not created.
   */
  timeout: 0,

  xsrfCookieName: 'XSRF-TOKEN',
  xsrfHeaderName: 'X-XSRF-TOKEN',

  maxContentLength: -1,
  maxBodyLength: -1,

  env: {
    FormData: platform.classes.FormData,
    Blob: platform.classes.Blob
  },

  validateStatus: function validateStatus(status) {
    return status >= 200 && status < 300;
  },

  headers: {
    common: {
      'Accept': 'application/json, text/plain, */*',
      'Content-Type': undefined
    }
  }
};

utils.forEach(['delete', 'get', 'head', 'post', 'put', 'patch'], (method) => {
  defaults.headers[method] = {};
});

export default defaults;

```

### node_modules/buffer-from/index.js

```javascript
/* eslint-disable node/no-deprecated-api */

var toString = Object.prototype.toString

var isModern = (
  typeof Buffer !== 'undefined' &&
  typeof Buffer.alloc === 'function' &&
  typeof Buffer.allocUnsafe === 'function' &&
  typeof Buffer.from === 'function'
)

function isArrayBuffer (input) {
  return toString.call(input).slice(8, -1) === 'ArrayBuffer'
}

function fromArrayBuffer (obj, byteOffset, length) {
  byteOffset >>>= 0

  var maxLength = obj.byteLength - byteOffset

  if (maxLength < 0) {
    throw new RangeError("'offset' is out of bounds")
  }

  if (length === undefined) {
    length = maxLength
  } else {
    length >>>= 0

    if (length > maxLength) {
      throw new RangeError("'length' is out of bounds")
    }
  }

  return isModern
    ? Buffer.from(obj.slice(byteOffset, byteOffset + length))
    : new Buffer(new Uint8Array(obj.slice(byteOffset, byteOffset + length)))
}

function fromString (string, encoding) {
  if (typeof encoding !== 'string' || encoding === '') {
    encoding = 'utf8'
  }

  if (!Buffer.isEncoding(encoding)) {
    throw new TypeError('"encoding" must be a valid string encoding')
  }

  return isModern
    ? Buffer.from(string, encoding)
    : new Buffer(string, encoding)
}

function bufferFrom (value, encodingOrOffset, length) {
  if (typeof value === 'number') {
    throw new TypeError('"value" argument must not be a number')
  }

  if (isArrayBuffer(value)) {
    return fromArrayBuffer(value, encodingOrOffset, length)
  }

  if (typeof value === 'string') {
    return fromString(value, encodingOrOffset)
  }

  return isModern
    ? Buffer.from(value)
    : new Buffer(value)
}

module.exports = bufferFrom

```

### node_modules/ws/index.js

```javascript
'use strict';

const WebSocket = require('./lib/websocket');

WebSocket.createWebSocketStream = require('./lib/stream');
WebSocket.Server = require('./lib/websocket-server');
WebSocket.Receiver = require('./lib/receiver');
WebSocket.Sender = require('./lib/sender');

WebSocket.WebSocket = WebSocket;
WebSocket.WebSocketServer = WebSocket.Server;

module.exports = WebSocket;

```

### node_modules/debug/src/index.js

```javascript
/**
 * Detect Electron renderer process, which is node, but we should
 * treat as a browser.
 */

if (typeof process !== 'undefined' && process.type === 'renderer') {
  module.exports = require('./browser.js');
} else {
  module.exports = require('./node.js');
}

```

### node_modules/mime-db/index.js

```javascript
/*!
 * mime-db
 * Copyright(c) 2014 Jonathan Ong
 * Copyright(c) 2015-2022 Douglas Christopher Wilson
 * MIT Licensed
 */

/**
 * Module exports.
 */

module.exports = require('./db.json')

```

### node_modules/isexe/index.js

```javascript
var fs = require('fs')
var core
if (process.platform === 'win32' || global.TESTING_WINDOWS) {
  core = require('./windows.js')
} else {
  core = require('./mode.js')
}

module.exports = isexe
isexe.sync = sync

function isexe (path, options, cb) {
  if (typeof options === 'function') {
    cb = options
    options = {}
  }

  if (!cb) {
    if (typeof Promise !== 'function') {
      throw new TypeError('callback not provided')
    }

    return new Promise(function (resolve, reject) {
      isexe(path, options || {}, function (er, is) {
        if (er) {
          reject(er)
        } else {
          resolve(is)
        }
      })
    })
  }

  core(path, options || {}, function (er, is) {
    // ignore EACCES because that just means we aren't allowed to run it
    if (er) {
      if (er.code === 'EACCES' || options && options.ignoreErrors) {
        er = null
        is = false
      }
    }
    cb(er, is)
  })
}

function sync (path, options) {
  // my kingdom for a filtered catch
  try {
    return core.sync(path, options || {})
  } catch (er) {
    if (options && options.ignoreErrors || er.code === 'EACCES') {
      return false
    } else {
      throw er
    }
  }
}

```

### text-to-speech/https/index.js

```javascript
const https = require("https");
const fs = require("fs");

const url = "https://api.deepgram.com/v1/speak?model=aura-asteria-en";
const apiKey = "DEEPGRAM_API_KEY"; // Replace with your Deepgram API key
const data = JSON.stringify({
  text: "Hello, how can I help you today?",
});

const options = {
  method: "POST",
  headers: {
    Authorization: `Token ${apiKey}`,
    "Content-Type": "application/json",
  },
};

const req = https.request(url, options, (res) => {
  if (res.statusCode !== 200) {
    console.error(`HTTP error! Status: ${res.statusCode}`);
    return;
  }

  const dest = fs.createWriteStream("output.mp3");
  res.pipe(dest);
  dest.on("finish", () => {
    console.log("File saved successfully.");
  });
});

req.on("error", (error) => {
  console.error("Error:", error);
});

req.write(data);
req.end();

```

### text-to-speech/fetch/index.js

```javascript
const fs = require("fs");

const url = "https://api.deepgram.com/v1/speak?model=aura-asteria-en";
const apiKey = "DEEPGRAM_API_KEY"; // Replace with your Deepgram API key
const outputFilePath = "output_file.mp3";

const body = JSON.stringify({
  text: "Hello, how can I help you today?",
});

const headers = {
  Authorization: `Token ${apiKey}`,
  "Content-Type": "application/json",
};

const options = {
  method: "POST",
  headers: headers,
  body: body,
};

fetch(url, options)
  .then((response) => {
    if (!response.ok) {
      throw new Error("Failed to make request:", response.statusText);
    }
    return response.blob();
  })
  .then((blob) => {
    const reader = blob.stream().getReader();

    const fileStream = fs.createWriteStream(outputFilePath);
    reader.read().then(function processText({ done, value }) {
      if (done) {
        console.log("File downloaded successfully.");
        return;
      }
      fileStream.write(Buffer.from(value));
      return reader.read().then(processText);
    });
  })
  .catch((error) => {
    console.error("Error:", error);
  });

```

### text-to-speech/axios/index.js

```javascript
const axios = require("axios");
const fs = require("fs");

const url = "https://api.deepgram.com/v1/speak?model=aura-asteria-en";
const apiKey = "DEEPGRAM_API_KEY"; // Replace with your Deepgram API key
const data = {
  text: "Hello, how can I help you today?",
};

const config = {
  headers: {
    Authorization: `Token ${apiKey}`,
    "Content-Type": "application/json",
  },
  responseType: "stream", // Ensure the response is treated as a stream
};

axios
  .post(url, data, config)
  .then((response) => {
    if (response.status !== 200) {
      console.error(`HTTP error! Status: ${response.status}`);
      return;
    }

    const dest = fs.createWriteStream("output.mp3");
    response.data.pipe(dest);
    dest.on("finish", () => {
      console.log("File saved successfully.");
    });
  })
  .catch((error) => {
    console.error("Error:", error.message);
  });

```

