import functools
import tornado.ioloop
import tornado.websocket
import tornado
import socket
import tornado.web
from tornado.tcpserver import TCPServer
from tornado import gen
import tornado.ioloop


S_PORT = 7707
client_list = []
web_client_list = set()

def accept_client(s_sock, fd, events):
    client_sock, client_addr = s_sock.accept()
    print "connection is ok"
    client_list.append(client_sock)

    chat_c = functools.partial(chat, client_sock)
    io_loop.add_handler(client_sock.fileno(), chat_c, io_loop.READ)
    print 'add handler is ok'


def broadcast(sock, msg):
    for c_sock in client_list:
        if sock != c_sock:
            c_sock.send(msg)
    for ws in web_client_list:
        ws.write_message(msg)


def chat(sock, fd, event):
    print "chat"
    msg = sock.recv(128)
    broadcast(sock, msg)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class SubHandler(tornado.websocket.WebSocketHandler):

    def open(self, *args):
        web_client_list.add(self)
        self.write_message("It's opened")
        # print self.get_argument("Id")
        # self.id = self.get_argument("Id")
        self.stream.set_nodelay(True)
        # clients[self.id]  = {"id" : self.id, "object" : self}
        print "good"

    def on_message(self, message):
        # print "clients %s received a message to console : %s" (self.id, message)
        print "client ", message

    def on_close(self):
        # if self.id in clients:
        #     del clients[self.id]
        print 'onClose'


class ChatServer(TCPServer):

    def __init__(self):
        TCPServer.__init__(self)
        self.clients = []

    @gen.coroutine
    def handle_stream(self, stream, address):
        self.clients.append(stream)
        print address, 'joined'
        io_loop = tornado.ioloop.IOLoop.current()
        tornado.ioloop.IOLoop.current().spawn_callback(self.__client_handler__, stream)

    @gen.coroutine
    def __client_handler__(self, stream):
        while True :
            message = yield stream.read_bytes(256, partial=True)
            for client in self.clients:
                yield client.write(message)
            for ws in web_client_list:
                ws.write_message(message)



if __name__ == '__main__':
    ##server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    ##server_sock.bind(("", S_PORT))
    ##server_sock.listen(5)



    io_loop = tornado.ioloop.IOLoop.current()
    ## set function partially
    ##accept_c = functools.partial(accept_client, server_sock)
    ##io_loop.add_handler(server_sock.fileno(), accept_c, io_loop.READ)

    server = ChatServer()
    server.listen(8000)

    app = tornado.web.Application([
        (r"/bb", SubHandler),
        (r"/", MainHandler),
    ])
    app.listen(8808)
    print "io loop start!!!!!"

    io_loop.start()