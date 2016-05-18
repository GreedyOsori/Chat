import socket
import threading

HOST = '127.0.0.1'
PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

print 'Connect Success!....'

def sendingMsg():
    while True:
        data = raw_input('')
        sock.send(data)
    sock.close()

def gettingMsg():
    while True:
        data = sock.recv(1024)
        print 'From Server :', repr(data)
    sock.close()

threading._start_new_thread(sendingMsg, ())
threading._start_new_thread(gettingMsg, ())

while True:
    pass