import _thread 
from glob import glob
import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from socket import *
conn=''
host='192.168.1.5'
port=58323
s=socket()
chatOb=None

class Chat(BoxLayout):

    def __init__(self):
        super(Chat, self).__init__()
    
    def clickAction(self):
        global s
        textMsg=self.ids['EntryBox'].text
        if textMsg != '':
            self.ids['ChatBox'].text+='\nYou: '+textMsg
            self.ids['EntryBox'].text=''
            s.sendall(textMsg.encode())

class ChatAppInterface(App):
    def build(self):
        global chatOb
        chatOb = Chat()
        Window.size=(400,500)
        return chatOb

def getClientConnected():
    global chatOb
    import time
    time.sleep(1)
    try:
        s.connect((host, port))
        chatOb.ids['ChatBox'].text='Successfully Connected '
    except:
        chatOb.ids['ChatBox'].text='Unable to connect '
        return
    while 1:
        try:
            data=s.recv(1024)
            chatOb.ids['ChatBox'].text+='\nOther: '+data.decode()
        except:
            chatOb.ids['ChatBox'].text='Peer has disconnected'
            break
    s.close()

if __name__=='__main__':
    _thread.start_new_thread(getClientConnected, ())
    ChatAppInterface().run()