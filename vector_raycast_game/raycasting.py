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

        dir_x, dir_y = self.game.player.dir_values  # dir vector
        plane_x, plane_y = self.game.player.plane_dir_values  # plane vector

        for x in range(0, WIDTH, DRAW_DENSE_FACTOR):
            p_pos_x, p_pos_y = self.game.player.pos  # player position vector
            map_x, map_y = self.game.player.map_pos  # map position
            camera_x = (2*x) / (WIDTH - 1)  # ratio of screen plane

            if camera_x <= 1:
                ray_dir_x = dir_x - (plane_x - (plane_x * camera_x))
                ray_dir_y = dir_y - (plane_y - (plane_y * camera_x))
            else:
                ray_dir_x = dir_x + plane_x * (camera_x - 1)
                ray_dir_y = dir_y + plane_y * (camera_x - 1)

            delta_dist_x = 1e30 if ray_dir_x == 0 \
                else abs(1 / ray_dir_x)
            delta_dist_y = 1e30 if ray_dir_y == 0 \
                else abs(1 / ray_dir_y)

            step_x, side_dist_x = (-1, (p_pos_x - map_x - 0.000001) * delta_dist_x) if ray_dir_x < 0 \
                else (1, (map_x + 1.0 - p_pos_x) * delta_dist_x)

            step_y, side_dist_y = (-1, (p_pos_y - map_y - 0.000001) * delta_dist_y) if ray_dir_y < 0 \
                else (1, (map_y + 1.0 - p_pos_y) * delta_dist_y)

            wall_detected = False
            self.is_north_south = False
            while not wall_detected:
                if side_dist_x < side_dist_y:
                    side_dist_x += delta_dist_x
                    map_x += step_x
                    self.is_north_south = True
                else:
                    side_dist_y += delta_dist_y
                    map_y += step_y
                    self.is_north_south = False

                if (map_x, map_y) in self.game.map.world_map:
                    wall_detected = True

            if self.is_north_south:
                depth = (side_dist_x - delta_dist_x)
            else:
                depth = (side_dist_y - delta_dist_y)

            project_height = int(HEIGHT / depth)
            object_to_render = project_height, depth, (ray_dir_x, ray_dir_y)
            self.render_objects(object_to_render, (map_x, map_y), x)

    def render_objects(self, obj_to_rend, map_pos, x):
        # unpack values
        proj_height, depth, ray_dir = obj_to_rend
        ray_dir_x, ray_dir_y = ray_dir

        pos_x, pos_y = self.game.player.pos
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
        #print('ok')

        # value of wall_x (offset)
        if self.is_north_south:
            wall_x = pos_y + depth * ray_dir_y
        else:
            wall_x = pos_x + depth * ray_dir_x
        wall_x -= math.floor(wall_x)

        # x coordinate of texture
        texture_x = int(wall_x * TEXTURE_SIZE)  # TEXTURE_SIZE HERE STANDS FOR TEXTURE WIDTH (W)
        if self.is_north_south and ray_dir_x > 0:
            texture_x = TEXTURE_SIZE - texture_x - 1  # TEXTURE_SIZE HERE STANDS FOR TEXTURE WIDTH (W)
        if not self.is_north_south and ray_dir_y < 0:
            texture_x = TEXTURE_SIZE - texture_x - 1

        # how much to increase the texture coordinate per screen pixel
        step = 1.0 * TEXTURE_SIZE / proj_height

        # Starting texture coordinate
        tex_pos = (draw_start - self.pitch - HALF_HEIGHT + proj_height / 2) * step


        #texture = pg.surfarray.array3d(texture)

        wall_column = self.textures[texture_num].subsurface(
            x % TEXTURE_SIZE, 0, DRAW_DENSE_FACTOR, TEXTURE_SIZE
        )
        wall_column = pg.transform.scale(wall_column, (DRAW_DENSE_FACTOR, draw_end - draw_start))
        wall_pos = (x, draw_start)

        self.game.screen.blit(wall_column, wall_pos)
        # for y in range(draw_start, draw_end, 1):
        #     texture_y = int(tex_pos) & (TEXTURE_SIZE - 1)
        #     tex_pos += step







        #pg.draw.line(self.screen, color, (x, draw_start), (x, draw_end), DRAW_DENSE_FACTOR)
        #print('ok')
        # pg.draw.rect(self.game.screen, color, )

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

