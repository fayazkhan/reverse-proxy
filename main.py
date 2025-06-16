import argparse
import asyncio


class Server:
    def __init__(self, backend):
        print(f"Using backend: {backend}")
        self.backend = backend

    async def serve_forever(self):
        server = await asyncio.start_server(
            self._handle_request, '127.0.0.1', 8888)

        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        print(f'Serving on {addrs}')

        async with server:
            await server.serve_forever()

    async def _handle_request(self, reader, writer):
        data = await reader.read(100)
        message = data.decode()
        addr = writer.get_extra_info('peername')

        print(f"Received {message!r} from {addr!r}")

        print(f"Send: {message!r}")
        writer.write(data)
        await writer.drain()

        print("Close the connection")
        writer.close()
        await writer.wait_closed()

    async def _forward_request(self, request):
        # Here you would implement the logic to forward the request to the backend
        print(f"Forwarding request to {self.backend}")
        # Simulate a response from the backend
        return b"HTTP/1.1 200 OK\r\nContent-Length: 12\r\n\r\nHello World!"


async def main():
    argparser = argparse.ArgumentParser(description="Simple HTTP Server")
    argparser.add_argument("backend", help="Backend server to use")
    backend = argparser.parse_args().backend
    await Server(backend).serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
