# Echo client program
import socket

class EchoClient(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self, host='127.0.0.1', port=50007, timeout=0.5):
        self._host = host
        self._port = int(port)
        self._timeout = float(timeout)
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.settimeout(self._timeout)
        self._buffer = 1024

    def connect(self):
        self._sock.connect((self._host, self._port))

    def disconnect(self):
        self._sock.close()

    def send(self, data):
        self._sock.sendall(data)

    def read(self):
        return self._sock.recv(self._buffer).strip()
