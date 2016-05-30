import random

class BaskinRobbins:
    def __init__(self, player_list):
        self.player_list = player_list
        self.game_table = 1 # 1 to 31~
        self.end = False

    def gameOver(self, lose_player):
        for player in self.player_list:
            if player == lose_player:
                player.lose() # player API
            player.win() # all player win exceptlose_player

    def gameGo(self):
        self.game_table = 1
        while self.end == False: # not end
            for current_player in self.player_list:
                this_turn_su = self.gameRequest(current_player) #
                while type(this_turn_su) != type(self.game_table):
                    this_turn_su = self.gameErrorAndReRequest(current_player)

                while this_turn_su > 3 or this_turn_su < 1: # this_turn_su
                    this_turn_su = self.gameErrorAndReRequest(current_player) # error control this turn only 1,2,3

                self.game_table += this_turn_su
                if self.game_table >= 31:
                    self.end = True
                    self.sendAllPlayer('Player '+current_player.name+' is Call 31!!')
                    break
                self.sendAllPlayer('GameTable Update :'+str(self.game_table))


    def gameRequest(self, current_player):
        return current_player.su(self.game_table) # simple Su by random

    def gameErrorAndReRequest(self, current_player):
        current_player.print_player('worng input')
        return current_player.su(self.game_table)

    def sendAllPlayer(self,msg):
        for player in self.player_list:
            player.print_player(msg)

class Player: # su(game_table)
    def __init__(self, name):
        self.name = name

    def su(self, game_table):
        return random.randrange(1,4) # 1,2,3

    def print_player(self, msg):
        print self.name+':'+msg

    def win(self):
        print self.name+'WIN!!'

    def lose(self):
        print self.name+'lose T,T'

seungmin = Player('SeungMin')
hara     = Player('Hara')

GameServer = BaskinRobbins([seungmin,hara]) # seungmin, hara is player

GameServer.gameGo()