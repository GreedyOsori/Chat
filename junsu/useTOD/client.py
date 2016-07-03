import socket

import threading
import time


class Client:

    def __init__(self):
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.write_thread = threading.Thread(target=self.__write_th)
        self.read_thread = threading.Thread(target=self.__read_th)

        self.id = ''

    def __write_th(self):
        while True:
            msg = raw_input("send msg : ")
            self.client_sock.send(msg)

    def __read_th(self):
        while True:
            msg =  self.client_sock.recv(128)
            print msg

    def do(self):

        self.client_sock.connect(('127.0.0.1', 7707))

        self.write_thread.start()
        self.read_thread.start()

client = Client()
client.do()
