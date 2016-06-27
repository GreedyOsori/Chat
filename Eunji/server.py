# -*- encoding: utf-8 -*-
from socket import *
import threading

class Server:
    def __init__(self):
        # Set up socket
        self.server_sock = socket(AF_INET, SOCK_STREAM)
        self.server_sock.bind(("127.0.0.1", 5021))
        self.server_sock.listen(5)
        print 'Server socket setting is done!!'

        #initialize vals
        self.shared_buf = ''  #메세지 저장 버퍼
        self.cID = ''  # Client ID 부여, 버퍼?
        self.rNum = 0  # Room number, default 0
        self.room = {}

    def broadcast(self, client):
        for k in self.room.keys():
            if self.room[k] == self.rNum:
                if self.shared_buf == "bye":
                    k.send(self.shared_buf)
                    k.send('\nClient %s disconnected' % self.cID)
                    k.remove(client)
                    self.p_dic()
                else:
                    if k != client:
                        k.send(self.shared_buf)

    def p_dic(self):
        for k in sorted(self.room.keys()):
            print 'Key:', k, '->', self.room[k]

    def serve_client(self, client_sock, num):
        self.cID = client_sock.recv(128)
        self.rNum = client_sock.recv(128)
        self.room[client_sock] = self.rNum
        client_sock.send('Welcome to room%s' % self.rNum)

        for k in self.room.keys():
            if self.room[k] == self.rNum:
                if k != client_sock:
                    k.send('%s is Invited' % self.cID)
        while True:
            self.shared_buf = client_sock.recv(1024)
            print self.shared_buf
            self.broadcast(client_sock)

    def do(self):
        while True:
            try:
                client = self.server_sock.accept()
                client_th = threading.Thread(target=self.serve_client, args=client)
                client_th.start()
            except Exception, e:
                print e


if __name__ == '__main__':
    try:
        server = Server()
        server.do()
    except KeyboardInterrupt:
        print 'Quited'
