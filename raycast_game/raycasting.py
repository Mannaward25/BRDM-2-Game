import pygame as pg
import math
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
        self.floor_tiles_hor = []
        self.floor_tiles_vert = []

    def get_objects_to_render(self):
        self.objects_to_render = []
        for ray, values in enumerate(self.raycasting_result):
            depth, proj_height, texture, offset = values

            if proj_height < HEIGHT:
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, proj_height))
                top_floor_y = HALF_HEIGHT + proj_height // 2

                wall_pos = (ray * SCALE, (HALF_HEIGHT - proj_height // 2))
                #self.floor_to_render(top_floor_y, offset, ray)

            else:
                texture_height = TEXTURE_SIZE * HEIGHT / proj_height
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE - texture_height // 2,
                    SCALE, texture_height
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)

            self.objects_to_render.append((depth, wall_column, wall_pos))

    def floor_to_render(self, top_floor_y, offset, ray):

        for depth, pos in self.floor_tiles_hor:

            proj_height = SCREEN_DIST / depth + 0.00001
            floor_row = self.textures[FLOOR_TEXTURE].subsurface(
                0, (TEXTURE_SIZE - SCALE) * offset, TEXTURE_SIZE, SCALE
            )
            floor_row = pg.transform.scale(floor_row, (proj_height, SCALE))
            floor_pos = (0, (top_floor_y + ray))  # FIXME!!!
            self.objects_to_render.append((depth, floor_row, floor_pos))

    def ray_cast(self):
        self.raycasting_result = []  # clearing every time method has been called
        self.floor_tiles_vert = []
        self.floor_tiles_hor = []
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
                elif tile_hor in self.game.map.open_space:

                    self.floor_tiles_hor.append((depth_hor, tile_hor))

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
                elif tile_vert in self.game.map.open_space:

                    self.floor_tiles_vert.append((depth_vert, tile_vert))

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
            # raycasting result
            self.raycasting_result.append((depth, proj_height, texture, offset))

            ray_angle += DELTA_ANGLE


    def update(self):
        self.ray_cast()
        self.get_objects_to_render()

    def rand_color(self):
        return (rd.randint(0, 255),
                rd.randint(0, 255),
                rd.randint(0, 255))


class FloorRayCasting(RayCasting):
    def __init__(self, game):
        super().__init__(game)

    def floor_ray_cast(self):
        depth = self.game.raycasting.depth
        project_height = self.game.raycasting.project_height

    def update(self):
        self.floor_ray_cast()
