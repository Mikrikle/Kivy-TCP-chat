from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.graphics import RoundedRectangle, Color

class Chat(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, 1)
        self.orientation = 'vertical'
        self.messages = GridLayout(cols=1, spacing=10, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        self.messages.bind(minimum_height=self.messages.setter('height'))
        messages_scroll = ScrollView(size_hint=(1, .9), size=(Window.width, Window.height))
        messages_scroll.add_widget(self.messages)
        self.messages.add_widget(Label(text='Chat App', size_hint_y=None, height=40))
        btn_box = BoxLayout(size_hint=(1,.08))
        self.message_field = TextInput(multiline=False)
        btn_box.add_widget(self.message_field)
        btn_box.add_widget(Button(text='>', size_hint=(.1,1), on_release=lambda btn: self.send_message(self.message_field.text)))
        self.add_widget(messages_scroll)
        self.add_widget(btn_box)

    def send_message(self, text):
        pass
            
    def accept_message(self, text):
        pass
    
    def notification_of_client(self, addr):
        message_widget = Button(background_color=(1, .5,.5,1), text='Client {} connected'.format(addr), size_hint_y=None, height=40)
        self.messages.add_widget(message_widget)
    
    def append_message_to_scroll(self, text, color):
        message_widget = Label(text=text, size_hint_y=None, size_hint_x=1,  height=40, halign="left", valign="middle", text_size=(self.width, None), color=color, padding_x=10)
        self.messages.add_widget(message_widget)
