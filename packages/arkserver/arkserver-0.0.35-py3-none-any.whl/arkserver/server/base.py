from arklibrary import Stream, Ini
from lib import get_host, get_port, get_name
import socket
import selectors
import types
from pathlib import Path


class Base:
    PATH = Path.cwd() / Path('config.ini')

    def __init__(self, name: str = None, host: str = None, port: str = None, timeout=5):
        self.name = name or get_name() or 'Nameless'
        self.host = host or get_host()
        self.port = port or get_port()
        self.address = f"{self.host}:{self.port}"

        self.selector = selectors.DefaultSelector()
        self.lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lsock.settimeout(timeout)

        self.client_sockets = {}
        self.client_keys = {}
        self.servers = {}
        self.data = {}

        self.__connected = False

    @property
    def connected(self):
        return self.__connected

    def _connect(self):
        self.lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.lsock.bind((self.host, self.port))
        self.lsock.listen()
        print(f"Listening on {self.host}:{self.port} (press CTRL-C to close server)")
        self.lsock.setblocking(False)
        self.selector.register(self.lsock, selectors.EVENT_READ, data=None)
        self.__connected = True

    def _disconnect(self):
        addresses = list(self.client_keys.keys())
        for addr in addresses:
            self._send_disconnect(addr)
            self._disconnect_client(addr)
        self.selector.close()
        self.__connected = False

    def _read(self, addr: str):
        sock = self.client_sockets[addr]
        fragments = bytearray()
        try:
            while True:
                chunk = bytearray(sock.recv(4096))  # Should be ready to read
                if not chunk:
                    break
                fragments += chunk
        except BlockingIOError:
            recv_data = bytes(fragments)
            stream = Stream(stream=recv_data)
            print(f'\033[93mReceived from client ({addr}): {stream.body}\033[0m')
            return recv_data
        except ConnectionResetError:
            """ When the client forces the connection to close: ctrl-c """
            return None

    def _write(self, stream: Stream):
        print(f'\033[93mSending to client ({stream.to_address}): {stream.body}\033[0m')
        sock = self.client_sockets[stream.to_address]
        key = self.client_keys[stream.to_address]
        encoded = stream.encode()
        size = f"{len(encoded)}".rjust(Stream.SIZE, '0').encode()
        sent = sock.send(size + encoded)
        key.data.outb = key.data.outb[sent:]

    def _disconnect_client(self, addr):
        print(f"Closing connection to {addr}")
        sock = self.client_sockets[addr]
        self.selector.unregister(sock)
        sock.close()
        del self.client_keys[addr]
        del self.client_sockets[addr]

    def _send_disconnect(self, addr):
        sock = self.client_sockets[addr]
        data = self.client_keys[addr].data
        sent = sock.send("exit".encode())  # Should be ready to write
        data.outb = data.outb[sent:]

    def _accept_wrapper(self, key):
        sock = key.fileobj
        conn, (host, port) = sock.accept()  # Shoulbd be ready to read
        client_address = f"{host}:{port}"
        print(f"Accepted connection from {client_address}")

        self.client_sockets[client_address] = sock
        self.client_keys[client_address] = key

        conn.setblocking(False)
        data = types.SimpleNamespace(addr=client_address, inb=b"", outb=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.selector.register(conn, events, data=data)
        return client_address

    def _service_connection(self, key, mask):
        data = key.data
        addr = data.addr
        self.client_sockets[addr] = key.fileobj
        self.client_keys[addr] = key
        stream = None

        if mask & selectors.EVENT_READ:
            read = self._read(addr)
            if read:
                stream = Stream.new(read)
                stream.from_address = addr
                data.outb += read
            else:
                self._disconnect_client(addr)
        if mask & selectors.EVENT_WRITE:
            if stream:
                if stream.type == 'api':
                    self.api_functions(stream)
                elif stream.type == "client":
                    self.client_functions(stream)

    def run(self):
        self._connect()
        try:
            while True:
                events = self.selector.select(timeout=None)
                for selector_key, mask in events:
                    if selector_key.data is None:
                        self._accept_wrapper(selector_key)
                    else:
                        self._service_connection(selector_key, mask)
        except KeyboardInterrupt:
            print("\nCaught keyboard interrupt, exiting:")
        finally:
            self._disconnect()
            print("All connections closed.")


    def __repr__(self):
        attr = {
            'connected': self.connected,
            'host': self.host,
            'port': self.port,
            'name': self.name
        }
        items = []
        for k, v in attr.items():
            items.append(f"\033[34m{k}\033[90m=\033[0m{repr(v)}\033[0m")
        args = ', '.join(items)
        return f'<\033[96mServer\033[0m({args})>\033[0m'
