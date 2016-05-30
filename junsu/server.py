from socket import *
import threading
from Message import Message

class Server:

    def __init__(self):
        self.server_sock = socket(AF_INET, SOCK_STREAM)
        self.server_sock.bind(("127.0.0.1", 9097))
        self.server_sock.listen(5)

        self.client_list = {}
        self.client_list['room1'] = []
        self.client_list['room2'] = []
        self.client_list['room3'] = []

        print 'Server socket setting is done!!\n'

    def broadcast(self, client_sock, num_room, message):
        # client_list have ( sock, addr_info, name )
        # message have ( num_room, name, msg )

        for i in self.client_list[num_room]:
            if(i[0] != client_sock):
                try:
                    i[0].send(message)
                except Exception as e:
                    print e.message
                    i[0].close()
                    self.client_list[num_room].remove(i)

    def serve_client(self, client_sock, client_addr):
        # "recv num_room'#'name'#'msg"
        message = client_sock.recv(128)
        room, name, msg = message.split('#')

        self.client_list[room].append((client_sock,client_addr,name))
        while True:
            try:
                message = client_sock.recv(128)
                if not message:
                    self.client_list[room].remove((client_sock,client_addr,name))
                    client_sock.close()
                    return
            except Exception as e:
                print e.message
                client_sock.close()

            self.broadcast(client_sock, room, message)

    def do(self):
        while True:
            print 'waiting for client ......\n'
            client = self.server_sock.accept()
            print 'welcome client!!\n'

            client_th = threading.Thread(target=self.serve_client,args = client)
            client_th.start()

        client_th.join()


server = Server()
server.do()

