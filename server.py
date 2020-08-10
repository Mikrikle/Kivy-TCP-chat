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
MY_NAME = 'Server!'
MY_COLOR = [1, 1, 1, 1]     # color of your own messages
OTHER_COLOR = [.8,.9,.8,1]  # color of the interlocutor's messages

#-------------------------------------------------------------#

INTERLOCUTOR_NAME = ''
connection_established = False
conn, addr = None, None
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)

def receive_data():
    global INTERLOCUTOR_NAME
    while True:
        '''recieved data from server'''
        data = conn.recv(1024).decode()
        if data.startswith('#:Command:Name-'):
            INTERLOCUTOR_NAME = data.split('-')[1]
        else:
            chat.accept_message(data)

def waiting_for_connection():
    '''start listening'''
    global connection_established, conn, addr, MY_NAME
    conn, addr = sock.accept()
    chat.notification_of_client(addr)
    connection_established = True
    conn.send('#:Command:Name-{}'.format(MY_NAME).encode())
    receive_data()

def create_thread(target):
    '''create and run thread'''
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()



class ServerChat(Chat):
    
    def send_message(self, text):
        global MY_COLOR
        if connection_established:
            protected_text = encryptDecrypt('E', text)
            conn.send(protected_text.encode())
            self.message_field.text = ''
            self.append_message_to_scroll('Me: {} '.format(text), MY_COLOR)
        else:
            print('No clients')
            
    def accept_message(self, protected_text):
        global OTHER_COLOR, INTERLOCUTOR_NAME
        text = encryptDecrypt('D', protected_text)
        self.append_message_to_scroll('{}: {} '.format(INTERLOCUTOR_NAME, text),  OTHER_COLOR)
            

chat = ServerChat()
class OnlineServerApp(App):
    def build(self):
        return chat


if __name__ == '__main__':
    create_thread(waiting_for_connection)
    OnlineServerApp().run()
    