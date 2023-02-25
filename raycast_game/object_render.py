import math

import pygame as pg  # +
from game_settings import *  # +
from pygame import gfxdraw
from random import randint, shuffle
from numba import njit, prange
import numpy as np


class ObjectRenderer:  # +
    def __init__(self, game):  # +
        self.game = game  # +
        self.screen = game.screen  # +
        self.wall_textures = self.load_wall_textures()  # +
        self.sky_image = self.get_texture('resources/textures/sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        self.blood_screen = self.get_texture('resources/textures/blood_screen.png', RES)
        self.digit_size = 90
        self.digit_images = [self.get_texture(f'resources/textures/digits/{i}.png',
                                              [self.digit_size] * 2) for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))
        self.game_over_image = self.get_texture('resources/textures/game_over.png', RES)
        self.victory_image = self.get_texture('resources/textures/win.png', RES)
        #self.doom_fire = self.game.doom_fire

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
        #self.doom_fire.draw()
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()

    def game_over(self):
        self.screen.blit(self.game_over_image, (0, 0))

    def victory(self):
        self.screen.blit(self.victory_image, (0, 0))

    def draw_player_health(self):
        health = str(self.game.player.health)
        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], (i * self.digit_size, 0))
        self.screen.blit(self.digits['10'], ((i + 1) * self.digit_size, 0))

    def player_damage(self):
        self.screen.blit(self.blood_screen, (0, 0))

    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        # print(f'sky_offset:{self.sky_offset}, mouse_rel:{self.game.player.rel}')
        #doom_fire_surf = self.doom_fire.fire_surf

        # for i in range(FIRE_REPS):
        #     self.screen.blit(doom_fire_surf, (doom_fire_surf.get_width() * i - self.sky_offset, 0 - HALF_HEIGHT))
        #     self.screen.blit(doom_fire_surf, (doom_fire_surf.get_width() * i + WIDTH - self.sky_offset,
        #                                       0 - HALF_HEIGHT))
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))  # simple sky
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))  # simple sky

        # floor
        #pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        list_of_objects = sorted(self.game.raycasting.objects_to_render,  # find out
                                 key=lambda t: t[0], reverse=True)

        for depth, image, pos in list_of_objects:
            self.screen.blit(image, pos)

    @staticmethod  # +
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):  # +
        texture = pg.image.load(path).convert_alpha()  # +
        return pg.transform.scale(texture, res)  # +

    def load_wall_textures(self) -> dict:  # +
        return {  # +
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
            25: self.get_texture('resources/textures/3.png'),
        }


class DoomFire:

    def __init__(self, game):
        self.game = game
        self.palette = self.get_palette()
        self.fire_array = self.get_fire_array()
        self.fire_surf = pg.Surface([PIXEL_SIZE * FIRE_WIDTH, HEIGHT])
        self.rnd = 0

    @staticmethod
    @njit(fastmath=True, parallel=True)
    def render_fire(fire_array, rnd):
        for x in prange(FIRE_WIDTH):
            for y in prange(1, FIRE_HEIGHT):
                color_index = fire_array[y][x]
                if color_index:
                    fire_array[y - 1][(x - rnd + 1) % FIRE_WIDTH] = color_index - rnd % 2
                else:
                    fire_array[y - 1][x] = 0
        return fire_array

    def do_fire_test(self):
        self.rnd = randint(0, 30)
        self.fire_array = np.array(self.fire_array)
        self.fire_array = self.render_fire(self.fire_array, self.rnd)

    def do_fire(self):
        for x in range(FIRE_WIDTH):
            for y in range(1, FIRE_HEIGHT):
                color_index = self.fire_array[y][x]
                if color_index:
                    rnd = randint(0, 3)
                    self.fire_array[y - 1][(x - rnd + 1) % FIRE_WIDTH] = color_index - rnd % 2
                else:
                    self.fire_array[y - 1][x] = 0

    def draw_fire(self):
        #self.fire_surf.fill(BLACK)
        for y, row in enumerate(self.fire_array):
            for x, color_index in enumerate(row):
                if color_index:
                    color = self.palette[color_index]
                    gfxdraw.box(self.fire_surf, (x * PIXEL_SIZE, y * PIXEL_SIZE,
                                                 PIXEL_SIZE - 1, PIXEL_SIZE - 1), color)
        # for i in range(FIRE_REPS):
        #     self.game.screen.blit(self.fire_surf, (self.fire_surf.get_width() * i, 0))

    def get_fire_array(self):
        fire_array = [[0 for i in range(FIRE_WIDTH)] for j in range(FIRE_HEIGHT)]
        for i in range(FIRE_WIDTH):
            fire_array[FIRE_HEIGHT - 1][i] = len(self.palette) - 1
        return fire_array

    def draw_palette(self):  # test method
        size = 90
        for i, color in enumerate(self.palette):
            pg.draw.rect(self.game.screen, color, (i * size, HEIGHT // 2, size - 5, size - 5))

    @staticmethod
    def get_palette():
        palette = [(0, 0, 0)]
        for i, color in enumerate(FLAME_COLORS[:-1]):
            c1, c2 = color, FLAME_COLORS[i + 1]
            for step in range(STEP_BETWEEN_COLORS):
                c = pg.Color(c1).lerp(c2, (step + 0.5) / STEP_BETWEEN_COLORS)
                palette.append(c)
        return palette

    def update(self):
        #self.do_fire_test() # test method with numba rendering
        self.do_fire()

    def draw(self):
        # self.draw_palette()
        self.draw_fire()


class Mode7:
    def __init__(self, game):
        self.game = game
        self.textures = self.game.object_renderer.wall_textures
        self.floor_text = self.textures[FLOOR_TEXTURE]
        self.texture_size = self.floor_text.get_size()

        self.floor_array = pg.surfarray.array3d(self.floor_text)

        self.player_pos = self.game.player.x, self.game.player.y
        self.player_ang = self.game.player.angle
        self.screen_array = pg.surfarray.array3d(pg.Surface(RES))

    def get_player_pos(self):
        self.player_pos = self.game.player.x, self.game.player.y

    def get_player_ang(self):
        self.player_ang = self.game.player.angle

    def update(self):
        self.get_player_ang()
        self.get_player_pos()
        self.screen_array = self.render_frame(self.floor_array, self.screen_array,
                                              self.texture_size, self.player_pos, self.player_ang)

    @staticmethod
    @njit(fastmath=True, parallel=True)  # unused
    def render_frame(floor_array, screen_array, texture_size, pos, angle):

        sin, cos = math.sin(angle), math.cos(angle)

        # iterating over screen array
        for ix in range(0, WIDTH, 1):
            for jy in range(HALF_HEIGHT, HEIGHT, 2):
                # x, y, z
                x = HALF_WIDTH - ix
                y = jy + FOCAL_LEN
                z = jy - HALF_HEIGHT + 0.01

                rx = (x * cos - y * sin)
                ry = (x * sin + y * cos)
                # projection

                floor_x = (rx / z - pos[1] * 2) * MODE_SEVEN_SCALE
                floor_y = (ry / z + pos[0] * 2) * MODE_SEVEN_SCALE

                # floor pos and color
                floor_pos = int(floor_x % texture_size[0]), \
                    int(floor_y % texture_size[1])
                floor_col = floor_array[floor_pos]

                # fill screen
                screen_array[ix, jy] = floor_col

        return screen_array

    def draw(self):
        pg.surfarray.blit_array(self.game.screen, self.screen_array)
