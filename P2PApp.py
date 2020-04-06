#
# P2P Text-Chat Application:
# This application uses a P2P connection to exchange text messages with anothe P2PGui. In
# order to connect, one user must chose to listen and another must connect chose to connect
# to the first's listening "host:port". The host port by default is "127.0.0.1:4500".
# Emojis can also be included in the messages by typing their aliases into the command line.
#
# Created by Elijah Smith
#
# Based off of this code by user teddy-k:
# https://code.activestate.com/recipes/578591-primitive-peer-to-peer-chat/
#
import tkinter as tki
from tkinter.font import Font
import emoji
import select
import socket
import threading
import time

PORT = 4500
HOST = '127.0.0.1'

class Chat_Server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True
        self.conn = None
        self.addr = None
        self.daemon = True

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        print("Listening for connections on", HOST, ":", PORT)
        self.conn, self.addr = s.accept()

        with self.conn:
            print("Connected")
            while self.running:
                ready, steady, nah = select.select([self.conn], [self.conn], [])
                if ready:
                    data = self.conn.recv(4096)
                    data = bytes.decode(data, 'utf-8')
                    if not data:
                        print("Server broken")
                        break
                    gui.printToLabel('Them: ' + emoji.emojize(data, use_aliases=True))
            time.sleep(0)
        print("Server closed. Type \"exit()\" to quit.")

    def kill(self):
        self.running = False


class Chat_Client(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.host = None
        self.sock = None
        self.running = True
        self.daemon = True

    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, PORT))
        with self.sock:
            print("Connected")
            while self.running:
                ready, steady, nah = select.select([self.sock], [self.sock], [])
                if ready:
                    data = self.sock.recv(4096)
                    data = bytes.decode(data, 'utf-8')
                    if not data:
                        print("Client broken")
                        break
                    gui.printToLabel('Them: ' + emoji.emojize(data, use_aliases=True))
            time.sleep(0)
        print("Client closed. Type \"exit()\" to quit.")

    def kill(self):
        self.running = False


class P2PGui(tki.Frame):

    def __init__(self):

        self.root = tki.Tk(className=" P2P Text Messenger")
        tki.Frame.__init__(self, self.root)

        self.lv0 = tki.StringVar()
        self.lv1 = tki.StringVar()
        self.lv2 = tki.StringVar()
        self.lv3 = tki.StringVar()
        self.lv4 = tki.StringVar()
        self.lv5 = tki.StringVar()
        self.lv6 = tki.StringVar()
        self.tv0 = tki.StringVar()

        self.createWidgets()
        self.pack()

    def createWidgets(self):
        self.root.bind('<Return>', self.submitText)

        topframe = tki.Frame(self)
        topframe.pack(side=tki.TOP)

        bottomframe = tki.Frame(self)
        bottomframe.pack(side=tki.BOTTOM)

        lab0 = tki.Label(topframe, textvariable=self.lv0)
        lab1 = tki.Label(topframe, textvariable=self.lv1)
        lab2 = tki.Label(topframe, textvariable=self.lv2)
        lab3 = tki.Label(topframe, textvariable=self.lv3)
        lab4 = tki.Label(topframe, textvariable=self.lv4)
        lab5 = tki.Label(topframe, textvariable=self.lv5)
        lab6 = tki.Label(topframe, textvariable=self.lv6)

        lblfont = Font(family="Sans Serif", size=12)
        labels = [lab0, lab1, lab2, lab3, lab4, lab5, lab6]
        for l in labels:
            l.configure(font=lblfont)
            l.configure(anchor='w')
            l.configure(width=42)
            l.pack()

        textentry = tki.Entry(bottomframe, width=53, fg="black", textvariable=self.tv0)
        textentry.pack(side=tki.LEFT)

        submitbutton = tki.Button(bottomframe, width=7,
                                  text="Send", command=self.submitText)
        submitbutton.pack(side=tki.RIGHT)

    def submitText(self, event=None):
        text = self.tv0.get().encode('utf-8')
        try:
            chat_client.sock.sendall(text)
        except:
            Exception()
        try:
            chat_server.conn.sendall(text)
        except:
            Exception()

        text = "Me: " + emoji.emojize(self.tv0.get(), use_aliases=True)
        self.moveLabelsUp()
        self.lv6.set(text)
        self.tv0.set("")


    def printToLabel(self, text):
        self.moveLabelsUp()
        self.lv6.set(text)

    def moveLabelsUp(self):
        self.lv0.set(self.lv1.get())
        self.lv1.set(self.lv2.get())
        self.lv2.set(self.lv3.get())
        self.lv3.set(self.lv4.get())
        self.lv4.set(self.lv5.get())
        self.lv5.set(self.lv6.get())

    def start(self):
        self.root.mainloop()


# Asks for user input and starts application
print("Peer To Peer Chat Server!")
print("---------------------------------------------------------------------------------")
print("Use Emojis by typing their corresponding aliases. For example, try \":thumbsup:\"")
print("---------------------------------------------------------------------------------")
print("Disconnect from a peer by closing the text chat window ")
print("---------------------------------------------------------------------------------")

ip_addr = input('Enter the IP address you would like to connect to below or type \"listen\" to await a connection\n')

chat_server = Chat_Server()
chat_client = Chat_Client()

if ip_addr.lower() == 'listen':
    chat_server.start()
else:
    chat_client.host = ip_addr
    chat_client.start()

gui = P2PGui()
gui.start()



















