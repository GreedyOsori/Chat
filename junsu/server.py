from socket import *
import threading
import signal


class Server:
    def __init__(self):
        self.server_sock = socket(AF_INET, SOCK_STREAM)
        self.server_sock.bind(("127.0.0.1", 9094))
        self.server_sock.listen(5)
        print 'Server socket setting is done!!\n'

        self.shared_buf = ''

        self.client_list = []


    def broadcast(self, client_sock):
        for i in self.client_list:
            if(i[0] != client_sock):
                i[0].send(self.shared_buf)

    def serve_client(self, client_sock, client_info):
        print 'work for client'

        #signal.signal(signal.SIGUSR1, lambda client_sock : client_sock.send(self.shared_buf))
        while True:
            self.shared_buf = client_sock.recv(128)
            print self.shared_buf
            self.broadcast(client_sock)
            #signal.siginterrupt(signal.SIGUSR1, False)
            # if it is not main thread, we cannot do things related to signal



    def do(self):
        while True:
            print 'waiting for client ......\n'
            client = self.server_sock.accept()
            print 'welcome client!!\n'

            self.client_list.append(client)
            client_th = threading.Thread(target=self.serve_client,args = client)
            client_th.start()


server = Server()
server.do()













