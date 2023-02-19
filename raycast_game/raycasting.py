import pygame as pg
import math
from numba import njit, prange
import numpy as np
import random as rd
from game_settings import *


class RayCasting:

    def __init__(self, game):
        self.game = game
        self.raycasting_result = []
        self.objects_to_render = []
        self.textures = self.game.object_renderer.wall_textures
        self.depth = 1
        self.project_height = 0

        #  floor params
        self.floor_texture = self.game.mode7.floor_text
        self.texture_size = self.game.mode7.texture_size
        self.floor_array = self.game.mode7.floor_array
        self.screen_array = self.game.mode7.screen_array
        self.mod = HALF_HEIGHT / DEG_FOV  # FOV 60 deg

    def get_objects_to_render(self):
        self.objects_to_render = []
        for ray, values in enumerate(self.raycasting_result):
            depth, proj_height, texture, offset = values

            if proj_height < HEIGHT:
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, proj_height))

                wall_pos = (ray * SCALE, (HALF_HEIGHT - proj_height // 2))

            else:
                texture_height = TEXTURE_SIZE * HEIGHT / proj_height
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE - texture_height // 2,
                    SCALE, texture_height
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)

            self.objects_to_render.append((depth, wall_column, wall_pos))

    def ray_cast(self):
        self.raycasting_result = []  # clearing every time method has been called

        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos
        texture_vert, texture_hor = 1, 1

        ray_angle = self.game.player.angle - HALF_FOV + 0.0001
        for ray in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            # horizontal lines of tiles
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a

            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for i in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map:
                    texture_hor = self.game.map.world_map[tile_hor]
                    break

                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            # verticals lines of tiles
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a

            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.world_map:
                    texture_vert = self.game.map.world_map[tile_vert]
                    break

                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            # depth, texture, offset
            if depth_hor < depth_vert:
                depth, texture = depth_hor, texture_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor
            else:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)

            # pg.draw.line(self.game.screen, YELLOW, (BLOCK_SIZE * ox, BLOCK_SIZE * oy),
            #              (BLOCK_SIZE * ox + BLOCK_SIZE * depth * cos_a,
            #               BLOCK_SIZE * oy + BLOCK_SIZE * depth * sin_a), 2)  #  2D raycasting

            # remove fishbowl effect
            depth *= math.cos(self.game.player.angle - ray_angle)

            # projection
            proj_height = SCREEN_DIST / (depth + 0.0001)

            # draw walls in old way (no textures, only white darkening)
            # color = [255 / (1 + depth ** 5 * 0.00002)] * 3   # dependence of color and distance to wall
            # pg.draw.rect(self.game.screen, color,
            #              (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height))
            # ----------------------------------
            # new way with textures
            # floor casting
            #self.floor_ray_cast(ray, (ox, oy), ray_angle)
            # raycasting result
            self.raycasting_result.append((depth, proj_height, texture, offset))

            # self.game.mode7.screen_array = self.game.mode7.render_frame(
            #     self.game.mode7.floor_array,
            #     self.game.mode7.screen_array,
            #     self.game.mode7.texture_size,
            #     (ox, oy),
            #     ray_angle
            # )

            ray_angle += DELTA_ANGLE

    @staticmethod
    @njit(fastmath=True, parallel=True)
    def floor_render(ray_x, screen_array, floor_array,
                     texture_size, pos, angle):
        player_x, player_y = pos
        text_w, text_h = texture_size[0], texture_size[1]
        ray_x = ray_x * 2

        sin = math.sin(angle)
        cos = math.cos(angle)

        for ray_y in range(HALF_HEIGHT, HEIGHT, 2):
            # x, y, z
            x = HALF_WIDTH - ray_x
            y = ray_y + FOCAL_LEN
            z = ray_y - HALF_HEIGHT + 0.001

            # rotation
            rx = ((x * cos) - y * sin)
            ry = (x * sin + y * cos)

            # projection
            floor_x = (rx / z - player_y) * MODE_SEVEN_SCALE
            floor_y = (ry / z + player_x) * MODE_SEVEN_SCALE

            # floor pos and color
            floor_pos = int(floor_x % text_w), int(floor_y % text_h)
            floor_col = floor_array[floor_pos]

            # fill screen
            screen_array[ray_x, ray_y] = floor_col

        return screen_array

    def floor_ray_cast(self, rays, pos, ray_angle):
        player_angle = self.game.player.angle
        self.game.mode7.screen_array = self.floor_render(rays, self.screen_array, self.floor_array,
                                                         self.texture_size, pos, player_angle)

    # @staticmethod
    # @njit(fastmath=True, parallel=True)
    # def floor_render(ray_x, screen_array, floor_array, texture_size, pos, angle, ray_angle, mod):
    #     player_x, player_y = pos
    #     text_w, text_h = texture_size[0], texture_size[1]
    #     ray_x = ray_x * 2
    #
    #     rot_i = angle + ray_angle
    #     # sin = math.sin(angle)
    #     # cos = math.cos(angle)
    #     sin = np.sin(rot_i)
    #     cos = np.cos(rot_i)
    #     cos2 = np.cos(np.deg2rad(ray_x / mod - HALF_DEG_FOV))
    #
    #     for ray_y in range(HALF_HEIGHT, HEIGHT - 1, 2):
    #         # x, y, z
    #         n = (HALF_HEIGHT / HALF_HEIGHT - ray_y) / cos2
    #         floor_x, floor_y = player_x + cos * n, player_y + sin * n
    #         # floor pos and color
    #         floor_pos = int(floor_x * 2 % text_w), int(floor_y * 2 % text_h)
    #         floor_col = floor_array[floor_pos]
    #
    #         # fill screen
    #         screen_array[ray_x, ray_y] = floor_col
    #
    #     return screen_array

    def update(self):
        self.ray_cast()
        self.get_objects_to_render()
        #self.game.mode7.draw()  # THERE IS FLOOR RENDERING

    def rand_color(self):
        return (rd.randint(0, 255),
                rd.randint(0, 255),
                rd.randint(0, 255))

