import socket
import threading
import os

PORT = 5050
SERVER = socket.gethostbyaddr(socket.gethostname())
ADDR = (SERVER , PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

