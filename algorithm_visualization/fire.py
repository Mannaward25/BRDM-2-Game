import pygame as pg
from pygame import gfxdraw
from settings import *
from numba import njit, prange
from random import randint
import numpy as np


class DoomFire:

    def __init__(self, game, switch_on=True):
        self.game = game
        self.switch_on = switch_on

        self.palette = self.get_palette()
        self.fire_array = self.get_fire_array()
        self.fire_surf = pg.Surface([PIXEL_SIZE * FIRE_WIDTH, HEIGHT])
        self.rnd = 0
        self.sound = False

        if self.switch_on:
            self.sound = Sound()

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
        self.fire_surf.fill(BLACK)
        for y, row in enumerate(self.fire_array):
            for x, color_index in enumerate(row):
                if color_index:
                    color = self.palette[color_index]
                    gfxdraw.box(self.fire_surf, (x * PIXEL_SIZE, y * PIXEL_SIZE,
                                                 PIXEL_SIZE - 1, PIXEL_SIZE - 1), color)
        for i in range(FIRE_REPS):
            self.game.screen.blit(self.fire_surf, (self.fire_surf.get_width() * i, 0))

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
        if self.switch_on:
            self.do_fire()

    def draw(self):
        # self.draw_palette()
        if self.switch_on:
            self.draw_fire()


class Sound:

    def __init__(self):
        pg.mixer.init()
        self.path = 'assets/'
        pg.mixer.music.load(self.path + f'fire.mp3')  #
        pg.mixer.music.play(loops=(-1))
