from game_settings import *
from player import Player, PlayerModel
from network_game import Client, ClientPlayerDataStruct, ServerPlayerDataStruct, HelloMsg

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
        while True:
            self.ghost.update()


class Ghost(Player):
    """network bot"""
    def __init__(self, game):
        super().__init__(game)

    def show_data(self, data: dict):
        for pid in data.keys():
            data[pid].show()

    def update(self):
        if self.game.network_game:
            self.send_data()
            data = self.recv_data()
            self.show_data(data)
            self.update_server_info(data)


class GhostModel(PlayerModel):

    def __init__(self, game, player_id, path='resources/sprites/npc/soldier/0.png',
                 pos=(2.5, 6.5), scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, player_id, path, pos, scale, shift, animation_time)


if __name__ == '__main__':
    app = App()
    app.update()
