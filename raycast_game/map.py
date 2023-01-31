import pygame as pg
from game_settings import *

_ = False

mini_map = [
    [1, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 1],
    [4, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 2],
    [2, _, _, 1, 1, 1, 1, _, _, _, 1, 1, 1, _, _, 2],
    [2, _, _, _, _, _, 1, _, _, _, _, _, 5, _, _, 2],
    [2, _, _, _, _, _, 5, _, _, _, _, _, 1, _, _, 2],
    [2, _, _, 1, 1, 1, 1, _, _, _, _, _, _, _, _, 2],
    [2, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 2],
    [4, _, _, 1, _, _, _, 1, _, _, _, _, _, _, _, 2],
    [1, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 2, 5, 4, 1]
]


class Map:
    def __init__(self, game):
        self.game = game
        self.mini_map = mini_map
        self.world_map = {}
        self.get_map()

    def get_map(self):
        for y, row in enumerate(self.mini_map):
            for x, value in enumerate(row):
                if value:
                    self.world_map[(x, y)] = value

    def draw(self):
        [pg.draw.rect(self.game.screen, DARK_GRAY, (pos[0] * BLOCK_SIZE, pos[1] * BLOCK_SIZE,
                                                    BLOCK_SIZE, BLOCK_SIZE), 2)
         for pos in self.world_map]

