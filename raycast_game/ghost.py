from game_settings import *
from player import Player, PlayerModel
from network_game import Client

"""bot for tests"""


class ObjectHandlerPlug:
    def __init__(self):
        self.no_npc = True


class App:
    def __init__(self):
        self.HOST = self.network_game = True
        self.object_handler = ObjectHandlerPlug()

        self.client = Client(self)
        self.ghost = Ghost(self)

    def update(self):
        pass


class Ghost(Player):
    """network bot"""
    def __init__(self, game):
        super().__init__(game)


class GhostModel(PlayerModel):

    def __init__(self, game, player_id, path='resources/sprites/npc/soldier/0.png',
                 pos=(2.5, 6.5), scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, player_id, path, pos, scale, shift, animation_time)


if __name__ == '__main__':
    pass
