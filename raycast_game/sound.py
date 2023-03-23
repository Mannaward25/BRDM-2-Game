import pygame as pg
from random import randint


class Sound:
    def __init__(self, game, no_sound=False):
        self.game = game
        self.no_sound = no_sound
        pg.mixer.init()
        self.path = 'resources/sound/'
        self.shotgun = pg.mixer.Sound(self.path + 'shotgun.wav')
        self.npc_pain = pg.mixer.Sound(self.path + 'npc_pain.wav')
        self.npc_death = pg.mixer.Sound(self.path + 'npc_death.wav')
        self.npc_shot = pg.mixer.Sound(self.path + 'npc_attack.wav')
        self.player_pain = pg.mixer.Sound(self.path + 'player_pain.wav')
        self.hover = pg.mixer.Sound(self.path + 'hover.wav')
        self.click = pg.mixer.Sound(self.path + 'click.wav')

    @staticmethod
    def volume(vol=1.0):
        pg.mixer.music.set_volume(vol)

    def main_menu(self):

        pg.mixer.music.load(self.path + f'main_menu.mp3')  #
        self.volume(0.5)
        pg.mixer.music.play(loops=(-1))

    def main_game(self):
        if not self.no_sound and self.game.game_start_flag:
            pg.mixer.music.load(self.path + f'theme{randint(1, 3)}.mp3')  #
            self.volume(0.5)
            pg.mixer.music.play(loops=(-1))
        elif self.game.menu_flag:
            self.main_menu()

    @staticmethod
    def stop():
        pg.mixer.music.stop()


