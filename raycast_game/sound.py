import pygame as pg
from random import randint


class Sound:
    def __init__(self, game, no_sound=False):
        self.game = game
        pg.mixer.init()
        self.path = 'resources/sound/'
        #self.path = 'resources/sound/theme1.mp3'
        self.shotgun = pg.mixer.Sound(self.path + 'shotgun.wav')
        self.npc_pain = pg.mixer.Sound(self.path + 'npc_pain.wav')
        self.npc_death = pg.mixer.Sound(self.path + 'npc_death.wav')
        self.npc_shot = pg.mixer.Sound(self.path + 'npc_attack.wav')
        self.player_pain = pg.mixer.Sound(self.path + 'player_pain.wav')

        if not no_sound:
            pg.mixer.music.load(self.path + f'theme{randint(1, 3)}.mp3')  #
            pg.mixer.music.play()
        #

    @staticmethod
    def volume(vol=1.0):
        pg.mixer.music.set_volume(vol)



