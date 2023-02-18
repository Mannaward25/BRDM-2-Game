import pygame as pg
import math
import numpy as np
from game_settings import *


class Player:

    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.dir_x, self.dir_y = INITIAL_DIRECTIONS
        self.plane_x, self.plane_y = INITIAL_PLANE
        self.angle = PLAYER_ANGLE

    def movement(self):
        sin_a = np.sin(self.angle)
        cos_a = np.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            # print(self.map_pos)
            # print(self.pos)
            dx += self.dir_x * speed
            dy += self.dir_y * speed
            # dx += speed_cos
            # dy += speed_sin
        if keys[pg.K_s]:
            dx -= self.dir_x * speed
            dy -= self.dir_y * speed
            # dx += -speed_cos
            # dy += -speed_sin
        if self.dir_x < 0 and self.dir_y < 0:
            if keys[pg.K_a]:
                dx -= self.dir_x * speed
                dy += self.dir_y * speed
            if keys[pg.K_d]:
                dx += self.dir_x * speed
                dy -= self.dir_y * speed

            if keys[pg.K_d]:
                dx -= self.dir_x * speed
                dy -= self.dir_y * speed
        else:
            if keys[pg.K_a]:
                dx += self.dir_x * speed
                dy -= self.dir_y * speed
            if keys[pg.K_d]:
                dx -= self.dir_x * speed
                dy += self.dir_y * speed

        self.check_wall_collision(dx, dy)

        # control player angle using the keys
        # if keys[pg.K_LEFT]:
        #     self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
        # if keys[pg.K_RIGHT]:
        #     self.angle += PLAYER_ROT_SPEED * self.game.delta_time
        self.angle %= math.tau

    def check_wall(self, x, y) -> bool:  # collisions
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):  # collisions
        if self.check_wall(int(self.x + dx), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy)):
            self.y += dy

    def draw(self):
        # pg.draw.line(self.game.screen, YELLOW, (self.x * BLOCK_SIZE, self.y * BLOCK_SIZE),
        #              (self.x * BLOCK_SIZE + WIDTH * math.cos(self.angle),
        #               self.y * BLOCK_SIZE + WIDTH * math.sin(self.angle)), 2)

        pg.draw.circle(self.game.screen, GREEN, (self.x * BLOCK_SIZE, self.y * BLOCK_SIZE), 15)

    def mouse_control(self):
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        if my < HALF_HEIGHT or my > HALF_HEIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        # print(f'mouse_rel:{self.rel}')
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))

        rot_speed = self.rel * MOUSE_SENSITIVITY
        old_dir_x = self.dir_x
        self.dir_x = self.dir_x * math.cos(-rot_speed) - self.dir_y * math.sin(-rot_speed)
        self.dir_y = old_dir_x * math.sin(-rot_speed) + self.dir_y * math.cos(-rot_speed)

        old_plane_x = self.plane_x
        self.plane_x = self.plane_x * math.cos(-rot_speed) - self.plane_y * math.sin(-rot_speed)
        self.plane_y = old_plane_x * math.sin(-rot_speed) + self.plane_y * math.cos(-rot_speed)

    def update(self):
        self.movement()
        self.mouse_control()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self) -> tuple:
        return int(self.x), int(self.y)

    @property
    def dir_values(self):
        return self.dir_x, self.dir_y

    @property
    def plane_dir_values(self):
        return self.plane_x, self.plane_y
