import functools
import tornado.ioloop
import tornado.websocket
import tornado
import tornado.web
from tornado.tcpserver import TCPServer
from tornado import gen
import tornado.ioloop
import time

S_PORT = 7707
client_list = []
web_client_list = set()


class SubHandler(tornado.web.RequestHandler):
    pass


class MainHandler(tornado.websocket.WebSocketHandler):
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
        ''' message is parsed ... .... '''


        ## in make room condition // c1, c2 is socket
        client_1 = None
        client_2 = None
        server.client_list.remove(client_1)
        server.client_list.remove(client_2)

        room = None
        tornado.ioloop.IOLoop.spawn_callback(server.__room_handler__, client_1, room)
        tornado.ioloop.IOLoop.spawn_callback(server.__room_handler__, client_2, room)


    def on_close(self):
        # if self.id in clients:
        #     del clients[self.id]
        print 'onClose'


class ChatServer(TCPServer):

    def __init__(self):
        TCPServer.__init__(self)
        self.client_list = []

    #@gen.coroutine
    def handle_stream(self, stream, address):
        self.client_list.append(stream)
        time.sleep(30)
        print server.client_list
        tornado.ioloop.IOLoop.current().spawn_callback(self.__client_handler__, stream)

    def __room_handler__(self, stream, room):
        room.onStart()
        while True:
            room.onAction()
            if room.errorCase:
                break
        room.onEnd()

    @gen.coroutine
    def __client_handler__(self, stream):
        while True:
            message = yield stream.read_bytes(256, partial=True)
            for client in self.client_list:
                yield client.write(message)
            for ws in web_client_list:
                ws.write_message(message)


if __name__ == '__main__':

    io_loop = tornado.ioloop.IOLoop.current()

    server = ChatServer()
    server.listen(8000)

    app = tornado.web.Application([
        (r"/bb", SubHandler),
        (r"/", MainHandler),
    ])
    app.listen(8808)
    print "io loop start!!!!!"

    io_loop.start()