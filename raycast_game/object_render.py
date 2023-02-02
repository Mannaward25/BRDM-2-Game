import pygame as pg
from game_settings import *


class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('resources/textures/sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        self.default_textures = {
            1: self.get_texture('resources/textures/1.png'),
            2: self.get_texture('resources/textures/2.png'),
            3: self.get_texture('resources/textures/3.png'),
            4: self.get_texture('resources/textures/4.png'),
            5: self.get_texture('resources/textures/5.png')
        }

        self.custom_textures = {
            1: self.get_texture('resources/textures/dacha/1_right.JPG'),
            2: self.get_texture('resources/textures/dacha/2_right.JPG'),
            3: self.get_texture('resources/textures/dacha/3_right.JPG'),

        }

    def draw(self):
        self.draw_background()
        self.render_game_objects()

    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))

        # floor
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        list_of_objects = sorted(self.game.raycasting.objects_to_render,  # find out
                                 key=lambda t: t[0], reverse=True)

        for depth, image, pos in list_of_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self) -> dict:
        return {
            1: self.get_texture('resources/textures/dacha/1_right.JPG'),
            2: self.get_texture('resources/textures/dacha/2_right.JPG'),
            3: self.get_texture('resources/textures/dacha/3_right.JPG'),
            4: self.get_texture('resources/textures/dacha/1_front.JPG'),
            5: self.get_texture('resources/textures/dacha/2_front.JPG'),
            6: self.get_texture('resources/textures/dacha/3_front.JPG'),
            7: self.get_texture('resources/textures/dacha/4_front.JPG'),
            8: self.get_texture('resources/textures/dacha/1_left.JPG'),
            9: self.get_texture('resources/textures/dacha/2_left.JPG'),
            10: self.get_texture('resources/textures/dacha/1_rear.JPG'),
            11: self.get_texture('resources/textures/dacha/2_rear.JPG'),
            12: self.get_texture('resources/textures/dacha/3_rear.JPG'),
            13: self.get_texture('resources/textures/dacha/1_win.JPG'),
            14: self.get_texture('resources/textures/dacha/1_door.JPG'),
            15: self.get_texture('resources/textures/dacha/1_yard.JPG'),
            16: self.get_texture('resources/textures/dacha/2_yard.JPG'),
            17: self.get_texture('resources/textures/dacha/3_yard.JPG'),
            18: self.get_texture('resources/textures/dacha/4_yard.JPG'),
            19: self.get_texture('resources/textures/dacha/5_yard.JPG'),
            20: self.get_texture('resources/textures/dacha/6_yard.JPG'),
            21: self.get_texture('resources/textures/dacha/7_yard.JPG'),
            22: self.get_texture('resources/textures/dacha/8_yard.JPG'),
            23: self.get_texture('resources/textures/dacha/9_yard.JPG'),
            24: self.get_texture('resources/textures/4.png'),

        }
