import tornado.ioloop
from TurnGameServer import TurnGameServer
from WebClientServer import WebClientServer
from TurnGameServer import TurnGameServer

## first
class MainServer:
    def __init__(self):
        self.battle_ai_list = dict()
        self.web_client_list = set()

        self.tcp_server = TurnGameServer(self.battle_ai_lists)
        self.websocketHandler = WebClientServer(self.web_client_list)

    def run(self):
        io_loop = tornado.ioloop.IOLoop.current()

        self.tcp_server.listen(8000)
        app = tornado.web.Application([
            (r"/", self.websocketHandler, dict(battle_ai_list=self.battle_ai_list, web_client_list=self.web_client_list, player_server=self.tcp_server)),
        ])
        app.listen(8800)
        print "io loop start!!!!!"

        io_loop.start()

if __name__ == "__main__":
    main_server = MainServer()
    main_server.run()



