# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///
"""This script implements a simple HTTP server that forwards requests to a specified backend server.
It reads incoming HTTP requests, forwards them to the backend, and returns the response to the client.
"""
import argparse
import asyncio
import urllib.parse


class Server:
    """Proxy server implementation"""
    def __init__(self, backend):
        print(f"Using backend: {backend}")
        self.backend_url = urllib.parse.urlparse(backend)

    async def serve_forever(self):
        """Starts the proxy server."""
        server = await asyncio.start_server(
            self._handle_request, '127.0.0.1', 8888)

        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        print(f'Serving on {addrs}')

        async with server:
            await server.serve_forever()

    async def _handle_request(self, reader, writer):
        """Handles incoming requests."""
        request = await self._read_message(reader, replace_host=True)
        addr = writer.get_extra_info('peername')
        print(f"Received request from {addr!r}")
        response = await self._forward_request(request)
        writer.write(response)
        await writer.drain()
        print("Close the connection")
        writer.close()
        await writer.wait_closed()

    async def _read_message(self, reader, replace_host=False):
        """Reads a complete HTTP message from the reader."""
        message = b''
        content_length = None
        while True:
            line = await reader.readline()
            print(f"Read header: {line!r}")
            if not line.strip():
                message += b'\r\n'  # End of headers
                break
            elif line.startswith(b'Content-Length:'):
                # If Content-Length is present, read the specified number of bytes
                content_length = int(line.split(b':', 1)[1].strip())
            elif replace_host and line.startswith(b'Host:'):
                # Replace the Host header with the backend server's host
                if self.backend_url.port:
                    new_host = f'Host: {self.backend_url.hostname}:{self.backend_url.port}\r\n'
                else:
                    new_host = f'Host: {self.backend_url.hostname}\r\n'
                line = new_host.encode()
                print(f"Replaced Host header with: {new_host!r}")
            message += line
        # Read the body if Content-Length is specified
        if content_length is not None:
            body = await reader.readexactly(content_length)
            print(f"Read body: {body!r}")
            message += body
        return message

    async def _forward_request(self, request):
        """Forwards the request to the backend server."""
        reader, writer = await asyncio.open_connection(
            self.backend_url.hostname,
            int(self.backend_url.port or (443 if self.backend_url.scheme == 'https' else 80)),
            ssl=bool(self.backend_url.scheme == 'https'))
        writer.write(request)
        await writer.drain()
        response = await self._read_message(reader)
        writer.close()
        await writer.wait_closed()
        return response


async def main():
    argparser = argparse.ArgumentParser(description="Simple HTTP Server")
    argparser.add_argument("backend", nargs='?', help="Backend server to use", default="http://example.com")
    backend = argparser.parse_args().backend
    await Server(backend).serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
