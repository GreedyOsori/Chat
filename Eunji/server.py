# -*- coding:utf-8 -*-
import socket
import sys
from thread import *

HOST = '' # all available interfaces
PORT = 3223

#소켓 생성
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(5) #Waiting MAX 5 clients
clients = []
print 'Welcome to the server.'

#Function for handling connections.
def clientThread(conn, clients):
    while 1:
        #Receive from client
        data = conn.recv(1024)
        received = str(data)
        for i in clients:
            i.send("Received " + data + "\n")
    conn.close()

while 1:
    conn, addr = sock.accept()
    clients.append(conn)
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    start_new_thread(clientThread, (conn, clients))

sock.close()
sys.exit()


