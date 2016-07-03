from tornado.tcpserver import TCPServer
from tornado import gen
import tornado.ioloop
import functools


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


if __name__=='__main__':
    server = ChatServer()
    server.listen(8000)
    tornado.ioloop.IOLoop.current().start()