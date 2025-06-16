# reverse-proxy
An HTTP reverse proxy

## Getting started


## Resources and references

- https://docs.astral.sh/uv/
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
- Only supports HTTP/1.x.

## Scaling

## Security
