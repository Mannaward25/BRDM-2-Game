import math
import os
from collections import deque
import pygame as pg
from game_settings import *


class SpriteObject:
    def __init__(self, game, path='resources/sprites/static_sprites/candlebra.png',
                 pos=(9.2, 1.2), scale=0.7, shift=0.4):
        self.game = game
        self.player = game.player  # we are going to need player pos
        self.x, self.y = pos   # position of the sprite
        self.image = pg.image.load(path).convert_alpha()  # loading sprite image
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.image.get_width() // 2
        self.dx, self.dy, self.theta = 0, 0, 0
        self.screen_x = 0
        self.sprite_half_width = 0
        self.dist, self.norm_dist = 1, 1  # norm dist for eliminating fishbowl effect
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()
        self.SPRITE_SCALE = scale
        self.SPRITE_HEIGHT_SHIFT = shift

    def get_sprite_projection(self):
        proj = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE
        proj_width, proj_height = proj * self.IMAGE_RATIO, proj

        image = pg.transform.scale(self.image, (proj_width, proj_height))
        height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT
        self.sprite_half_width = proj_width // 2
        pos = self.screen_x - self.sprite_half_width, HALF_HEIGHT - proj_height // 2 + height_shift

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
        if -self.IMAGE_HALF_WIDTH < self.screen_x < (WIDTH + self.IMAGE_HALF_WIDTH) and self.norm_dist > 0.3:
            self.get_sprite_projection()

    def update(self):
        self.get_sprite()


class AnimatedSprite(SpriteObject):
    def __init__(self, game, path='resources/sprites/animated_sprites/green_light/0.png',
                 pos=(9.2, 4.5), scale=0.7, shift=0.4, animation_time=90):
        super().__init__(game, path, pos, scale, shift)
        self.animation_time = animation_time
        self.path = path.rsplit('/', 1)[0]
        print(self.path)
        self.images = self.get_images(self.path)
        self.animation_time_prev = pg.time.get_ticks()
        self.animation_trigger = False

    def update(self):
        super().update()
        self.check_animation_time()
        self.animate(self.images)

    def animate(self, images: deque):
        if self.animation_trigger:
            images.rotate(-1)
            self.image = images[0]

    def check_animation_time(self):
        self.animation_trigger = False
        time_now = pg.time.get_ticks()
        if time_now - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = time_now
            self.animation_trigger = True

    def get_images(self, path) -> deque:
        images = deque()
        for file_name in os.listdir(path):
            full_path = os.path.join(path, file_name)
            if os.path.isfile(full_path):
                img = pg.image.load(path + '/' + file_name).convert_alpha()
                images.append(img)
        return images
