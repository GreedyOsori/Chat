import functools
import tornado.ioloop
import tornado.websocket
import tornado
import socket
import tornado.web

S_PORT = 7707
client_list = []


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


def chat(sock, fd, event):
    print "chat"
    msg = sock.recv(128)
    broadcast(sock, msg)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class SubHandler(tornado.websocket.WebSocketHandler):

    def open(self, *args):
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


if __name__ == '__main__':
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    server_sock.bind(("", S_PORT))
    server_sock.listen(5)

    io_loop = tornado.ioloop.IOLoop.current()
    ## set function partially
    accept_c = functools.partial(accept_client, server_sock)
    io_loop.add_handler(server_sock.fileno(), accept_c, io_loop.READ)
    app = tornado.web.Application([
        (r"/bb", SubHandler),
        (r"/", MainHandler),
    ])
    app.listen(8808)
    print "sdfsafasf!!"

    io_loop.start()