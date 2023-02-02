import pygame as pg
from game_settings import *

_ = False

# mini_map = [
#     [1, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 1],
#     [4, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 2],
#     [2, _, _, 1, 1, 1, 1, _, _, _, 1, 1, 1, _, _, 2],
#     [2, _, _, _, _, _, 1, _, _, _, _, _, 5, _, _, 2],
#     [2, _, _, _, _, _, 5, _, _, _, _, _, 1, _, _, 2],
#     [2, _, _, 1, 1, 1, 1, _, _, _, _, _, _, _, _, 2],
#     [2, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 2],
#     [4, _, _, 1, _, _, _, 1, _, _, _, _, _, _, _, 2],
#     [1, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 2, 5, 4, 1]
# ]

mini_map = [
   [1, 1, 2, 3, 1, 1, 13, 13, 1, 1, 14, 22, 22, 23, 22, 1],
   [7, _, _, _, 10, _, _, _, 1, _, _, 1, _, _, _, 15],
    [4, _, _, _, _, _, _, _, _, _, _, 1, _, _, _, 16],
   [5, _, _, _, 12, _, _, _, 1, _, _, 1, _, _, _, 17],
   [6, _, _, _, 11, _, _, _, 1, _, _, _, _, _, _, 18],
    [1, 8, 1, 9, 1, 1, 1, 1, 1, 1, _, 1, _, _, _, 19],
    [1, _, _, _, _, _, _, _, _, _, _, 1, _, _, _, 20],
    [13, _, _, _, 1, _, _, _, _, _, _, 1, _, _, _, 21],
    [1, 24, 24, 24, 1, 1, 1, 1, 1, 1, 13, 1, 22, 22, 22, 22]
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

