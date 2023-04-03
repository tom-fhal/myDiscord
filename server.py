import socket
import threading
from connect_bd import *

class ChatRoomServer:
    def __init__(self, port):
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', port))
        self.clients = []

    def start(self):
        self.server_socket.listen(5)
        print(f"Server for chat room on port {self.port} started.")
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"New connection from {client_address}")
            self.clients.append(client_socket)
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        # print(f"{username} connected to chat room on port {self.port}")
        # welcome_message = f"Welcome to the chat room on port {self.port}, {username}!"
        # client_socket.send(welcome_message.encode())
        # broadcast_message = f"{username} has joined the chat room."
        # self.broadcast(broadcast_message)
        username = client_socket.recv(1024).decode().strip()
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if not message:
                    break
                broadcast_message = f"{message}"
                self.broadcast(broadcast_message)
            except:
                client_socket.close()
                break

    def broadcast(self, message):
        for client in self.clients:
            client.send(message.encode('ascii'))


    def stop(self):
        self.server_socket.close()
        print(f"Server for chat room on port {self.port} stopped.")


query = Query()
channels = query.getAllChannels()
listServer = []
for channel in channels:
    listServer.append(ChatRoomServer(channel[5]))

for server in listServer:
    threading.Thread(target=server.start).start()