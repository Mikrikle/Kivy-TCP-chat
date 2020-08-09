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

#-------------------------------------------------------------#

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

def receive_data():
    while True:
        '''recieved data from server'''
        chat.accept_message(sock.recv(1024).decode())

def create_thread(target):
    '''create and run thread'''
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()



class ClientChat(Chat):
    def send_message(self, text):
        sock.send(text.encode())
        self.message_field.text = ''
        self._append_message_to_scroll('Client (me): < {} >'.format(text))
            
    def accept_message(self, text):
        self._append_message_to_scroll('Server: < {} >'.format(text))
            

chat = ClientChat()
class OnlineClientApp(App):
    def build(self):
        return chat



if __name__ == '__main__':
    create_thread(receive_data)
    OnlineClientApp().run()