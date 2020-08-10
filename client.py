import socket
import threading
from kivy_chat import Chat

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
import random
from kivy.core.window import Window

#-------------------------------------------------------------#

HOST = '127.0.0.1' 
PORT = 65432 
MY_NAME = 'CoolMan'

#-------------------------------------------------------------#

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
INTERLOCUTOR_NAME = ''

def receive_data():
    global INTERLOCUTOR_NAME
    while True:
        '''recieved data from server'''
        data = sock.recv(1024).decode()
        if data.startswith('#:Command:Name-'):
            INTERLOCUTOR_NAME = data.split('-')[1]
        else:
            chat.accept_message(data)

def connection():
    global MY_NAME, sock
    sock.send('#:Command:Name-{}'.format(MY_NAME).encode())
    receive_data()

def create_thread(target):
    '''create and run thread'''
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()



class ClientChat(Chat):
    My_color = [1, 1, 1, 1]
    Other_color = [.8,.9,.8,1]
    
    def send_message(self, text):
        sock.send(text.encode())
        self.message_field.text = ''
        self.append_message_to_scroll('Me: {} '.format(text), self.My_color)
            
    def accept_message(self, text):
        self.append_message_to_scroll('{}: {} '.format(INTERLOCUTOR_NAME, text), self.Other_color)
            

chat = ClientChat()
class OnlineClientApp(App):
    def build(self):
        return chat


if __name__ == '__main__':
    create_thread(connection)
    OnlineClientApp().run()