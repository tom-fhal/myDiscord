import socket
import threading
import tkinter
from connect_bd import *
from customtkinter import CTkTextbox

class ChatRoomClient:
    def __init__(self, host, port, username,frame_chat,id_canal):
        self.host = host
        self.port = port
        self.username = username
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tabview = CTkTextbox(frame_chat, width=800,height=550)
        self.i=1
        self.id_canal = id_canal
        self.query = Query()
        self.display_message()

    def connect(self):
        self.client_socket.connect((self.host, self.port))
        print("Connected to server")
        self.client_socket.send(self.username.encode())

        # Start listening for messages from server
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

    def send_message(self, message):
        self.client_socket.send(f"{self.username}: {message}".encode())
        
    def display_message(self):
        cursor = self.query.conn.cursor()
        sqlQuery = f"SELECT text FROM messages INNER JOIN utilisateurs ON messages.id_utilisateur = utilisateurs.id_utilisateur WHERE id_canal LIKE {self.id_canal};"
        cursor.execute(sqlQuery)
        result = cursor.fetchall()
        cursor.close()

        for message in result: 
            self.tabview.insert(f"{self.i}.0",f"{message[0]}\n")
            self.i+=1

    def receive_messages(self):
        while True:
            message = self.client_socket.recv(1024).decode()
            self.tabview.insert(f"{self.i}.0",f"{message}\n")
            self.query.AddNewMessage(self.id_canal,message,self.username)
            self.i +=1
            self.tabview.grid(row=0,column=0,sticky="n")
            #ajoute le message la base de données

    def disconnect(self):
        self.client_socket.close()
