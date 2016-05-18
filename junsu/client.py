from socket import *
import threading


class Client:
    def __init__(self, name):
        self.client_sock = socket(AF_INET, SOCK_STREAM)

        self.write_thread = threading.Thread(target=self.write_th)
        self.read_thread = threading.Thread(target=self.read_th)

        self.name = name

    def write_th(self):
        print 'do write'
        self.client_sock.send("WELCOME!!!   " + self.name)
        while True:
            message = raw_input()
            if message == "exit":
                self.close()
            self.client_sock.send( self.name +" : "+message)

    def read_th(self):
        print 'do read'
        while True:
            message = self.client_sock.recv(128)
            print message + '\n'


    def connect(self):
        self.client_sock.connect(('127.0.0.1', 9094))

    def close(self):
        self.client_sock.close()
    def do(self):
        self.connect()
        self.write_thread.start()
        self.read_thread.start()

n = raw_input("input your name : ")

client = Client(n)
client.do()



