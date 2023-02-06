import pygame as pg
from settings import *


class Player:
    def __init__(self, app):
        self.app = app
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE

    def update(self):
        pass

    @property
    def pos(self) -> tuple:
        return self.x, self.y

    @property
    def map_pos(self) -> tuple:
        return int(self.x), int(self.y)