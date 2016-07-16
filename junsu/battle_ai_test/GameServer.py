import tornado.tcpserver
from tornado import gen
import tornado.ioloop


class GameServer(tornado.tcpserver.TCPServer):

    def __init__(self, battle_ai_list):
        tornado.tcpserver.TCPServer.__init__()
        self.battle_ai_list = battle_ai_list  # battle_ai_list is dict() , key is username

    def handle_stream(self, stream, address):
        tornado.ioloop.IOLoop.spawn_callback(self.__accept_handler, stream)

    @gen.coroutine
    def __accept_handler(self, stream):
        # accept client
        # get ai_ name ;;
        data = yield stream.read_bytes(256, partial=True)
        self.battle_ai_list['username'] = stream

    @gen.coroutine
    def __room_handler(self, room):
        room.game.onStart()
        try:
            # TODO : __how to handle player conn
            for player in room.player_list:
                self.__player_handler(player)
            pass
        except Exception as e:
            room.game.onError()
            print e
            pass
        finally:
            room.game.onEnd()

    def __player_handler(self, player):
        pass
