import socket
import threading

from kivy_chat import Chat
from encryption import encryptDecrypt

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
import random
from kivy.core.window import Window

#-----------------FAST---SETTINGS-----------------------------#

HOST = '127.0.0.1' 
PORT = 65432 
MY_NAME = 'CoolMan'
MY_COLOR = [1, 1, 1, 1]     # color of your own messages
OTHER_COLOR = [.8,.9,.8,1]  # color of the interlocutor's messages

#-------------------------------------------------------------#

INTERLOCUTOR_NAME = ''
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

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

    def send_message(self, text):
        global MY_COLOR
        protected_text = encryptDecrypt('E', text)
        sock.send(protected_text.encode())
        self.message_field.text = ''
        self.append_message_to_scroll('Me: {} '.format(text), MY_COLOR)
            
    def accept_message(self, protected_text):
        global OTHER_COLOR
        text = encryptDecrypt('D', protected_text)
        self.append_message_to_scroll('{}: {} '.format(INTERLOCUTOR_NAME, text), OTHER_COLOR)
            

chat = ClientChat()
class OnlineClientApp(App):
    def build(self):
        return chat


if __name__ == '__main__':
    create_thread(connection)
    OnlineClientApp().run()