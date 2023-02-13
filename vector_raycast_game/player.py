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
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a]:
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]:
            dx += -speed_sin
            dy += speed_cos

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
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
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
        self.angle += self.rel * MOUSE_SENSITIVITY

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
