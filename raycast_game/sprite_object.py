import math

import pygame as pg
from game_settings import *


class SpriteObject:
    def __init__(self, game, path='resources/sprites/static_sprites/candlebra.png',
                 pos=(10.5, 3.5)):
        self.game = game
        self.player = game.player
        self.x, self.y = pos
        self.image = pg.image.load(path).convert_alpha()
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.image.get_width() // 2
        self.dx, self.dy, self.theta = 0, 0, 0
        self.screen_x = 0
        self.sprite_half_width = 0
        self.dist, self.norm_dist = 1, 1
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()

    def get_sprite_projection(self):
        proj = SCREEN_DIST / self.norm_dist
        proj_width, proj_height = proj * self.IMAGE_RATIO, proj

        image = pg.transform.scale(self.image, (proj_width, proj_height))

        self.sprite_half_width = proj_width // 2
        pos = self.screen_x - self.sprite_half_width, HALF_HEIGHT - proj_height // 2

        self.game.raycasting.objects_to_render.append((self.norm_dist, image, pos))

    def get_sprite(self):
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.dx, self.dy = dx, dy
        self.theta = math.atan2(dy, dx)

        delta = self.theta - self.player.angle
        # print(f'dx:{dx}, dy:{dy}, p_angle:{self.player.angle}, theta:{self.theta}, '
        #       f'theta(degr):{math.degrees(self.theta)}, delta before:{delta}')
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau

        delta_rays = delta / DELTA_ANGLE
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE

        # print(f'theta:{self.theta}, p_angle:{self.player.angle}, delta:{delta}, '
        #       f'delta_rays:{delta_rays}, self.screen_x:{self.screen_x}')

        self.dist = math.hypot(dx, dy)
        self.norm_dist = self.dist * math.cos(delta)
        if -self.IMAGE_HALF_WIDTH < self.screen_x < (WIDTH + self.IMAGE_HALF_WIDTH) and self.norm_dist > 0.5:
            self.get_sprite_projection()

    def update(self):
        self.get_sprite()
