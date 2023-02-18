import pygame as pg
import math
from numba import njit, prange
import numpy as np
import random as rd
from game_settings import *


class RayCasting:

    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.textures = self.game.object_renderer.test_wall_textures

    def ray_cast(self):

        dir_x, dir_y = self.game.player.dir_values
        plane_x, plane_y = self.game.player.plane_dir_values

        p_pos_x, p_pos_y = self.game.player.pos  # player position

        for x in range(WIDTH):
            map_x, map_y = self.game.player.map_pos  # map position
            camera_x = (2 * x) / (WIDTH - 1)  # x coord in camera space
            ray_dir_x = dir_x + plane_x * camera_x
            ray_dir_y = dir_y + plane_y * camera_x

            delta_dist_x = 1e30 if ray_dir_x == 0 else abs(1 / ray_dir_x)
            delta_dist_y = 1e30 if ray_dir_y == 0 else abs(1 / ray_dir_y)

            step_x, side_dist_x = (-1, (p_pos_x - map_x) * delta_dist_x) if ray_dir_x < 0 \
                else (1, (map_x + 1.0 - p_pos_x) * delta_dist_x)

            step_y, side_dist_y = (-1, (p_pos_y - map_y) * delta_dist_y) if ray_dir_y < 0 \
                else (1, (map_y + 1.0 - p_pos_y) * delta_dist_y)

            wall_detected = False
            is_north_south = False
            while not wall_detected:
                if side_dist_x < side_dist_y:
                    side_dist_x += delta_dist_x
                    map_x += step_x
                    is_north_south = False
                else:
                    side_dist_y += delta_dist_y
                    map_y += step_y
                    is_north_south = True

                if (map_x, map_y) in self.game.map.world_map:
                    wall_detected = True

            if is_north_south:
                depth = (side_dist_x - delta_dist_x)
            else:
                depth = (side_dist_y - delta_dist_y)

            project_height = HEIGHT / depth
            self.render_objects(project_height, (map_x, map_y), x)

    def render_objects(self, proj_height, map_pos, x):
        draw_start = -proj_height / 2 + HALF_HEIGHT
        draw_end = proj_height / 2 + HALF_HEIGHT
        texture_num = self.game.map.world_map[map_pos]
        color = self.textures[texture_num]

        if draw_start < 0:
            draw_start = 0
        if draw_end >= HEIGHT:
            draw_end = HEIGHT - 1
        print('ok')
        pg.draw.line(self.screen, color, (x, draw_start), (x, draw_end), 2)
        print('ok')
        # pg.draw.rect(self.game.screen, color, )

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
