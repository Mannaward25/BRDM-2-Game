import pygame as pg
import math
from numba import njit, prange
import numpy as np
import random as rd
from game_settings import *


class RayCasting:

    def __init__(self, game):
        self.game = game

    def ray_cast(self):
        dir_x, dir_y = self.game.player.dir_values
        plane_x, plane_y = self.game.player.plane_dir_values
        for x in range(WIDTH):
            camera_x = (2 * x) / (WIDTH - 1)  # x coord in camera space
            ray_dir_x = dir_x + plane_x * camera_x
            ray_dir_y = dir_y + plane_y * camera_x

    def update(self):
        self.ray_cast()

    def rand_color(self):
        return (rd.randint(0, 255),
                rd.randint(0, 255),
                rd.randint(0, 255))


class VectorRayCast:

    def __init__(self, game):
        self.game = game
        self.raycasting_result = []
        self.objects_to_render = []

    def ray_cast(self):
        pass

    def update(self):
        self.ray_cast()
