import socket
import threading
from kivy_chat import Chat

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
import random
from kivy.core.window import Window


HOST = '127.0.0.1' 
PORT = 65432        
connection_established = False
conn, addr = None, None
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)

def receive_data():
    while True:
        '''recieved data from server'''
        chat.accept_message(conn.recv(1024).decode())

def waiting_for_connection():
    '''start listening'''
    global connection_established, conn, addr
    conn, addr = sock.accept()
    chat.notification_of_client(addr)
    connection_established = True
    receive_data()

def create_thread(target):
    '''create and run thread'''
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()



class ServerChat(Chat):
    My_color = [1, 1, 1, 1]
    Other_color = [.8,.9,.8,1]

    def send_message(self, text):
        if connection_established:
            conn.send(text.encode())
            self.message_field.text = ''
            self.append_message_to_scroll('Me: {} '.format(text), self.My_color)
        else:
            print('No clients')
            
    def accept_message(self, text):
        self.append_message_to_scroll('Client: {} '.format(text), self.Other_color)
            

chat = ServerChat()
class OnlineServerApp(App):
    def build(self):
        return chat


if __name__ == '__main__':
    create_thread(waiting_for_connection)
    OnlineServerApp().run()
    