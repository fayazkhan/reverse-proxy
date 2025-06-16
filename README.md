# reverse-proxy
An HTTP reverse proxy

## Getting started

```bash
    # Start a simple http server in a different terminal
    $ python -m http.server 8000
    # Use our proxy to forward requests to it
    $ python main.py http://127.0.0.1:8000
```

## Resources and references

- https://docs.python.org/3/library/asyncio-stream.html
- https://stackoverflow.com/questions/4824451/detect-end-of-http-request-body
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Messages

### Assistants used

- Google AI overview
- Github Copilot

## Design

- We use `asyncio.start_server` for the frontend server implementation
  and `asyncio.open_connection` for the backend client implementation.
- We perform minimal parsing/processing of the requests, just enough to read and forward them.

### Limitations

- No support for chunked content.
- Only supports very basic HTTP/1.x.

### Possible scaling improvements

- Implement backend connection pooling or persistence.
- Improve throughput by supporting conditional request headers like `ETag` & `Last-Modified`.
- Implement caching.
- Add parallel workers to leverage multiple CPUs.

### Possible security improvements

- Add frontend SSL support.
- Improve overall SSL handling.
- Add options for rate-limiting and limiting content length and parallel connections.
- Perform request validation.
