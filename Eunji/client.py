from socket import *
import threading


class Client:
    def __init__(self):
        self.client_sock = socket(AF_INET, SOCK_STREAM)
        self.write_thread = threading.Thread(target=self.write_th)
        self.read_thread = threading.Thread(target=self.read_th)
        self.name = ''
        self.rNum = 0

    def write_th(self):
        while True:
            message = raw_input('[' + self.name + '] : ')

            if message == "bye":
                self.client_sock.send('[' + self.name + '] : ' + message + '\n')
                self.close()
            self.client_sock.send('[' + self.name + '] : ' + message)

    def read_th(self):
        while True:
            message = self.client_sock.recv(1024)
            print message

    def make_name(self):
        self.name = raw_input('What is your Name? : ')
        self.client_sock.send(self.name)

    def chz_room(self):
        self.rNum = raw_input('\nPlz choose the room number\n 1. Room1\n 2. Room2\n 3. Room3\n >> ')
        self.client_sock.send(self.rNum)

    def connect(self):
        self.client_sock.connect(('127.0.0.1', 5021))

    def close(self):
        self.client_sock.close()

    def do(self):
        self.connect()
        self.make_name()
        self.chz_room()

        self.write_thread.start()
        self.read_thread.start()


if __name__ == '__main__':
    try:
        client = Client()
        client.do()
    except KeyboardInterrupt:
        print 'Quited'


