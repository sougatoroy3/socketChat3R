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
host='192.168.1.5' #replace it with your IP
port=58323         #replace it with your port number
s=socket()
s.bind((host, port))
chatOb=None

class Chat(BoxLayout):

    def __init__(self):
        super(Chat, self).__init__()

    def clickAction(self):
        global conn
        textMsg=self.ids['EntryBox'].text
        if textMsg != '':
            self.ids['ChatBox'].text+='\nYou: '+textMsg
            self.ids['EntryBox'].text=''
            conn.sendall(textMsg.encode())

class ChatAppInterface(App):
    def build(self):
        global chatOb
        chatOb = Chat()
        Window.size=(400,500)
        return chatOb

def getHostConnected():
    global conn, chatOb
    import time
    time.sleep(1)
    s.listen(1)
    chatOb.ids['ChatBox'].text='Waiting for connection'
    conn, addr=s.accept()
    chatOb.ids['ChatBox'].text='Connected with: '+str(addr)
    while 1:
        try:
            data=conn.recv(1024)
            chatOb.ids['ChatBox'].text+='\nOther: '+data.decode()
        except:
            getHostConnected()
    conn.close()

if __name__=='__main__':
    _thread.start_new_thread(getHostConnected, ())
    ChatAppInterface().run()