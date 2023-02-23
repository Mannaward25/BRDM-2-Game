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
        self.test_textures = self.game.object_renderer.test_wall_textures
        self.textures = self.game.object_renderer.wall_textures
        #self.screen_array = pg.surfarray.array3d(pg.Surface(RES))
        #self.black_array = pg.surfarray.array3d(pg.Surface(RES))
        self.is_north_south = False
        self.pitch = PITCH

    def ray_cast(self):

        dir_x, dir_y = self.game.player.dir_values  # dir vector -  angle analog
        plane_x, plane_y = self.game.player.plane_dir_values  # plane vector

        # ray_angle = math.atan2(dir_y, dir_x)
        # sin_a = math.sin(ray_angle)
        # cos_a = math.cos(ray_angle)
        p_pos_x, p_pos_y = self.game.player.pos  # player position vector
        player_angle = math.atan2(dir_y, dir_x)

        for x in range(0, WIDTH, DRAW_DENSE_FACTOR):
            map_x, map_y = self.game.player.map_pos  # map position
            camera_x = (2*x) / (WIDTH - 1)  # ratio of screen plane

            if camera_x <= 1:
                ray_dir_x = dir_x - (plane_x - (plane_x * camera_x))
                ray_dir_y = dir_y - (plane_y - (plane_y * camera_x))
            else:
                ray_dir_x = dir_x + plane_x * (camera_x - 1)
                ray_dir_y = dir_y + plane_y * (camera_x - 1)

            ray_angle = math.atan2(ray_dir_y, ray_dir_x)
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            delta_dist_x = 1e30 if ray_dir_x == 0 \
                else abs(1 / ray_dir_x)
            delta_dist_y = 1e30 if ray_dir_y == 0 \
                else abs(1 / ray_dir_y)

            delta_dist_x_raw = 1e30 if ray_dir_x == 0 \
                else math.sqrt(1 + (ray_dir_y * ray_dir_y) / (ray_dir_x * ray_dir_x))
            delta_dist_y_raw = 1e30 if ray_dir_y == 0 \
                else math.sqrt(1 + (ray_dir_x * ray_dir_x) / (ray_dir_y * ray_dir_y))

            side_dist_x_raw = ((p_pos_x - map_x - 0.000001) * delta_dist_x_raw) if ray_dir_x < 0 \
                else (map_x + 1 - p_pos_x) * delta_dist_x_raw

            side_dist_y_raw = ((p_pos_y - map_y - 0.000001) * delta_dist_y_raw) if ray_dir_y < 0 \
                else ((map_y + 1 - p_pos_y) * delta_dist_y_raw)

            step_x, side_dist_x, dist_x_vert = (-1, ((p_pos_x - map_x - 0.000001) * delta_dist_x),
                                                map_x - 0.000001) if ray_dir_x < 0 \
                else (1, ((map_x + 1.0 - p_pos_x) * delta_dist_x), (map_x + 1))

            step_y, side_dist_y, dist_y_hor = (-1, ((p_pos_y - map_y - 0.000001) * delta_dist_y),
                                               (map_y - 0.000001)) if ray_dir_y < 0 \
                else (1, ((map_y + 1.0 - p_pos_y) * delta_dist_y), (map_y + 1))

            wall_detected = False
            self.is_north_south = False
            x_offset, y_offset, offset = 0, 0, 0
            while not wall_detected:
                if side_dist_x < side_dist_y:
                    side_dist_x += delta_dist_x
                    side_dist_x_raw += delta_dist_x_raw
                    map_x += step_x
                    self.is_north_south = True
                else:
                    side_dist_y += delta_dist_y
                    side_dist_y_raw += delta_dist_y_raw
                    map_y += step_y
                    self.is_north_south = False

                if (map_x, map_y) in self.game.map.world_map:

                    if self.is_north_south:  # set up texturing system
                        #delta_x = (side_dist_x - delta_dist_x + plane_x) * cos_a
                        #delta_y = (side_dist_x - delta_dist_x) * sin_a
                        delta_x = (side_dist_y_raw - delta_dist_y_raw) * cos_a
                        delta_y = (side_dist_x_raw - delta_dist_x_raw) * sin_a
                        x_offset = delta_y
                        x_offset %= 1
                        offset = x_offset
                        offset = (1 - x_offset) if sin_a > 0 else x_offset

                        if x == 900 or x == WIDTH - 2:
                            print(f'sn | ray number: {x} | map_pos: [{map_x}; {map_y}] | p_pos: [{p_pos_x + delta_x}; {p_pos_y + delta_y}]')
                    else:
                        #delta_x = (side_dist_y - delta_dist_y) * cos_a
                        #delta_y = (side_dist_y - delta_dist_y + plane_y) * sin_a
                        delta_x = (side_dist_y_raw - delta_dist_y_raw) * cos_a
                        delta_y = (side_dist_x_raw - delta_dist_x_raw) * sin_a
                        y_offset = delta_x
                        y_offset %= 1
                        offset = y_offset
                        offset = y_offset if cos_a > 0 else (1 - y_offset)

                        if x == 900 or x == WIDTH - 2:
                            print(f'ew | ray number: {x} | map_pos: [{map_x}; {map_y}] | p_pos: [{p_pos_x + delta_x}; {p_pos_y + delta_y}]')
                    wall_detected = True

            if self.is_north_south:
                depth = (side_dist_x - delta_dist_x)
            else:
                depth = (side_dist_y - delta_dist_y)

            project_height = int(HEIGHT / abs(depth))
            object_to_render = project_height, depth, (ray_dir_x, ray_dir_y)
            self.render_objects(object_to_render, (map_x, map_y), x, offset)

    def render_objects(self, obj_to_rend, map_pos, x, offset):
        # unpack values
        proj_height, depth, ray_dir = obj_to_rend

        draw_start = int(-proj_height / 2 + HALF_HEIGHT + self.pitch)
        draw_end = int(proj_height / 2 + HALF_HEIGHT + self.pitch)
        texture_num = self.game.map.world_map[map_pos]
        color = self.test_textures[texture_num]

        if draw_start < 0:
            draw_start = 0
        if draw_end >= HEIGHT:
            draw_end = HEIGHT - 1

        if self.is_north_south:
            color = self.side_bright(color)

        wall_column = self.textures[texture_num].subsurface(
            offset * (TEXTURE_SIZE - DRAW_DENSE_FACTOR), 0, DRAW_DENSE_FACTOR, TEXTURE_SIZE
        )
        wall_column = pg.transform.scale(wall_column, (DRAW_DENSE_FACTOR, draw_end - draw_start))
        wall_pos = (x * DRAW_DENSE_FACTOR, draw_start)

        self.game.screen.blit(wall_column, wall_pos)

    def side_bright(self, color):
        return tuple(map(lambda x: int(x / 2), color))

    def update(self):
        self.ray_cast()
        #self.draw()

    def rand_color(self):
        return (rd.randint(0, 255),
                rd.randint(0, 255),
                rd.randint(0, 255))

    def draw(self):
        pass
        #pg.surfarray.blit_array(self.game.screen, self.screen_array)

