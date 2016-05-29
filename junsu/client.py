from socket import *
import threading
from Message import Message

class Client:
    def __init__(self):
        self.client_sock = socket(AF_INET, SOCK_STREAM)

        self.write_thread = threading.Thread(target=self.__write_th)
        self.read_thread = threading.Thread(target=self.__read_th)

    def __write_th(self):
        while True:
            try:
                msg = raw_input()
                if msg == "exit":
                    message = self.room+'#'+self.name+'#'+"bye~!!!!!!!!!!!!!!"
                    self.client_sock.send(message)
                    self.__close()
                    break
                message = self.room+'#'+self.name+'#'+msg
                self.client_sock.send(message)
            except Exception as e:
                print e.message
                self.__close()
                return

    def __read_th(self):
        while True:
            try:
                msg = self.client_sock.recv(128)
                message = msg.split('#')

                print "%s : %s"%(message[1], message[2])
            except Exception as e:
                print e.message
                self.client_sock.close()
                return

    def __connect(self):
        try:
            self.client_sock.connect(('127.0.0.1', 9097))
        except Exception as e:
            print e.message

    def __close(self):
        self.client_sock.close()
    def do(self):
        self.__connect()

        # server accept client ......
        self.name = raw_input("Your name : ")

        while(True):
            room_choice = raw_input("room choice!!\n1.room1\n2.room2\n3.room3\n-> ")
            if room_choice == '1':
                room_choice = 'room1'
                break
            if room_choice == '2':
                room_choice = 'room2'
                break
            if room_choice == '3':
                room_choice = 'room3'
                break
        self.room = room_choice
        message = self.room+'#'+self.name+'#'
        self.client_sock.send(message)

        self.write_thread.start()
        self.read_thread.start()

client = Client()
client.do()
