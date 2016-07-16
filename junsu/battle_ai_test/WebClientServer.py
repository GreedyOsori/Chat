import tornado.websocket
import tornado.ioloop
from Room import Room


class WebClientServer(tornado.websocket.WebSocketHandler):
    def initialize(self, web_client_list=set(), battle_ai_list=dict(), player_server=None):
        self.web_client_list = web_client_list  # set()
        self.battle_ai_list = battle_ai_list  # dict()
        self.player_server = player_server

    # accept web_client
    def open(self, *args, **kwargs):
        self.web_client_list.add(self)
        pass

    def on_message(self, message):
        # all received message is battle request

        # make attendee object

        # !! case 1 : make new room
        # !! make player object
        # !! !! get player stream
        try:
            p1 = self.battle_ai_list.pop('player1')
            p2 = self.battle_ai_list.pop('player2')

            # !! make player list
            player_list = [p1, p2]
        except Exception as e:
            print e
            # concurrent access error

        # make room
        room = Room(player_list)
        room.add_attendee(self)
        # fire and forget go!! *** PlayerServer.__play_handler()
        tornado.ioloop.IOLoop.spawn_callback(self.player_server.__game_handler, room)

        # =================================================================
        # case 2 : join existing room
        pass

    def close(self):
        self.web_client_list.pop(self)
