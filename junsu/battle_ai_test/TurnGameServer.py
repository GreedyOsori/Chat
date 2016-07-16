from GameServer import GameServer
from tornado import gen

class TurnGameServer(GameServer):

    @gen.coroutine
    def __player_handler(self, player):
        pass

