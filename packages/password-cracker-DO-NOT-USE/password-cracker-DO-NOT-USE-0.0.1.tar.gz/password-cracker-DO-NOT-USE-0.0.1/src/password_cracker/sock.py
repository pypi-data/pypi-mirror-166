import os
import socket
from pathlib import Path


class Socket:
    def __init__(self):
        self.BUFFER_SIZE = 2048
        self.ADDR = ('123.45.67.8', 5000)
        self.set_conn()

    def set_conn(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(self.ADDR)

    def send(self, fp):
        filename = Path(fp).name
        filesize = os.path.getsize(filename)

        self.socket.send(f"{filename}:{filesize}".encode())

        with open(filename, "rb") as f:
            while True:
                # read the bytes from the file
                bytes_read = f.read(self.BUFFER_SIZE)
                if not bytes_read:
                    # file transmitting is done
                    break
                self.socket.sendall(bytes_read)
        self.socket.close()