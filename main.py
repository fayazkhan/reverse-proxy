# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///

import argparse
import asyncio
import urllib.parse


class Server:
    def __init__(self, backend):
        print(f"Using backend: {backend}")
        self.backend_url = urllib.parse.urlparse(backend)

    async def serve_forever(self):
        server = await asyncio.start_server(
            self._handle_request, '127.0.0.1', 8888)

        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        print(f'Serving on {addrs}')

        async with server:
            await server.serve_forever()

    async def _handle_request(self, reader, writer):
        request = await self._read_message(reader)
        addr = writer.get_extra_info('peername')
        print(f"Received {request!r} from {addr!r}")
        response = await self._forward_request(request)
        print(f"Send: {response!r}")
        writer.write(response)
        await writer.drain()

        print("Close the connection")
        writer.close()
        await writer.wait_closed()

    async def _read_message(self, reader):
        message = b''
        content_length = None
        # Read the request line and headers
        while True:
            line = await reader.readline()
            print(f"Read line: {line!r}")
            if line.startswith(b'Content-Length:'):
                # If Content-Length is present, read the specified number of bytes
                content_length = int(line.split(b':', 1)[1].strip())
            message += line
            if not line.strip():
                break
        # Read the body if Content-Length is specified
        if content_length is not None:
            body = await reader.readexactly(content_length)
            print(f"Read body: {body!r}")
            message += body
        return message

    async def _forward_request(self, request):
        print(f"Forwarding request to {self.backend_url}")
        updated_request = request.replace(
            b'Host: 127.0.0.1:8888', f'Host: {self.backend_url.hostname}:{self.backend_url.port}'.encode())
        print(f"Sending updated request: {updated_request!r}")
        reader, writer = await asyncio.open_connection(
            self.backend_url.hostname,
            int(self.backend_url.port or (443 if self.backend_url.scheme == 'https' else 80)),
            ssl=bool(self.backend_url.scheme == 'https'))
        writer.write(updated_request)
        await writer.drain()
        response = await self._read_message(reader)
        print(f"Received response: {response!r}")
        writer.close()
        await writer.wait_closed()
        return response


async def main():
    argparser = argparse.ArgumentParser(description="Simple HTTP Server")
    argparser.add_argument("backend", help="Backend server to use", default="http://example.com")
    backend = argparser.parse_args().backend
    await Server(backend).serve_forever()


if __name__ == "__main__":
    asyncio.run(main())

