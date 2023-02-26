import pygame as pg
from settings import *


class ObjectRender:
    def __init__(self, game):
        self.game = game
        self.textures = self.load_textures()

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_textures(self):
        return {
            1: self.get_texture('resources/3.png')
        }

    def render_game_objects(self):

        for step in range(0, WIDTH, TEXTURE_SIZE):
            for offset_y in range(0, HALF_HEIGHT, 2):
                proj_width = (HEIGHT - HALF_HEIGHT + offset_y) / HEIGHT
                texture_floor = self.textures[1].subsurface(
                    0, offset_y % TEXTURE_SIZE, TEXTURE_SIZE, 2
                )
                texture_floor = pg.transform.scale(texture_floor, (TEXTURE_SIZE * proj_width, 2))
                self.game.screen.blit(texture_floor, (0 + step, HEIGHT - TEXTURE_SIZE + offset_y))

    def draw(self):
        self.render_game_objects()

