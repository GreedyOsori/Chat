import socket
import threading

class OneCli:
    def __init__(self, conn, sockList):
        self.conn = conn
        self.sockList = sockList
        threading._start_new_thread(self.sendingMsg, ())
        threading._start_new_thread(self.gettingMsg, ())

    def sendingMsg(self):
        while True:
            data = raw_input('')
            for cli in sockList:
                cli.send(data)
        for cli in sockList:
            cli.close()

    def gettingMsg(self):
        while True:
            data = self.conn.recv(1024)
            if not data:
                break
            elif data == 'quit':
                print 'disconnet', self.conn
            else:
                print 'Get :', repr(data)
        self.conn.close()



HOST = ''
PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)

sockList = []

while True:
    conn, addr = sock.accept()
    sockList.append(conn)

    print 'Connected by', addr
    '''
    def sendingMsg():
        while True:
            data = raw_input('')
            conn.send(data)
        conn.close()

    def gettingMsg():
        while True:
            data = conn.recv(1024)
            if not data:
                break
            elif data == 'quit':
                print 'disconnet', conn
            else:
                print 'Get :', repr(data)
        conn.close()

    threading._start_new_thread(sendingMsg, ())
    threading._start_new_thread(gettingMsg, ())
    '''
    conn_cli = OneCli(conn, sockList)
