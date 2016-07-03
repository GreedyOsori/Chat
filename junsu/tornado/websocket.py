import tornado.ioloop
import tornado.web
import tornado.websocket

class MainHandler (tornado.web.RequestHandler):

    def get(self):
        self.render('index.html')

class StoryHandler (tornado.web.RequestHandler):
    def get(self, s, v):
        self.write(s)
        self.write(v);


class ArgHandler (tornado.web.RequestHandler):

    def get(self, *args):
        self.write("Hello");
        self.write(self.get_argument("Id"));
        print self.get_argument("Id");

    def post(self, *args):
        self.write("post : Hello ");
        self.write(self.get_argument("Id"));
        print self.get_argument("Id");

clients = {}


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


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/story/([0-9]+)/([a-z]+)", StoryHandler),
        (r"/aa", ArgHandler),
        (r"/bb", SubHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8808)
    tornado.ioloop.IOLoop.instance().start()
