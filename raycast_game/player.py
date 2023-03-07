import time

import pygame as pg  # +
import math  # +
import numpy as np
from game_settings import *  # +
from network_game import Client
from sprite_object import AnimatedSprite
import json


class Player:

    def __init__(self, game):  # +
        self.game = game  # +
        self.x, self.y = PLAYER_POS  # +
        self.x_prev, self.y_prev = PLAYER_POS  # do not sure, this is using somewhere
        self.angle = PLAYER_ANGLE  # +
        self.no_tau_angle = PLAYER_ANGLE
        self.rel = 0
        self.shot = False
        self.health = PLAYER_MAX_HEALTH
        self.health_recovery_delay = 700
        self.time_prev = pg.time.get_ticks()

        # networking
        self.client: Client = self.game.client
        self.number_of_players = 0
        self.players = {}

        tries = 0  # hardcode
        if self.game.HOST or self.game.network_game:
            while not self.try_connect() and tries < 3:
                print("unsuccessful connection retrial in 3 sec")
                time.sleep(4)
                tries += 1
            self.create_player_instances()

        if self.game.network_game:
            self.x, self.y = self.client.get_init_pos()

    def try_connect(self):
        msg = self.client.connect()
        if msg:
            num = int(msg.split(' ')[-1]) if msg else 0
            self.number_of_players = num
            self.client.set_client_id(num)
            print(msg, f'from Client_id {num} .__init__')
            return True
        return False

    def recover_health(self):
        if self.check_health_recovery_delay() and self.health < PLAYER_MAX_HEALTH:
            self.health += 1

    def check_health_recovery_delay(self):
        time_now = pg.time.get_ticks()
        if time_now - self.time_prev > self.health_recovery_delay:
            self.time_prev = time_now
            return True

    def check_game_win(self):
        if not any([npc.alive for npc in self.game.object_handler.npc_list]):
            self.game.object_renderer.victory()
            pg.display.flip()
            pg.time.delay(1500)
            self.game.new_game()

    def check_game_over(self):
        if self.health < 1:
            self.game.object_renderer.game_over()
            pg.display.flip()
            pg.time.delay(1500)
            self.game.new_game()

    def get_damage(self, damage):
        self.health -= damage
        self.game.object_renderer.player_damage()
        self.game.sound.player_pain.play()
        self.check_game_over()

    def single_fire_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shot and not self.game.weapon.reloading:
                self.game.sound.shotgun.play()
                self.shot = True
                self.game.weapon.reloading = True

    def movement(self):  # +
        sin_a = math.sin(self.angle)  # +
        cos_a = math.cos(self.angle)  # +
        dx, dy = 0, 0  # +
        speed = PLAYER_SPEED * self.game.delta_time  # +
        speed_sin = speed * sin_a  # +
        speed_cos = speed * cos_a  # +

        keys = pg.key.get_pressed()  # +
        if keys[pg.K_w]:  # +
            dx += speed_cos  # +
            dy += speed_sin  # +
        if keys[pg.K_s]:  # +
            dx += -speed_cos  # +
            dy += -speed_sin  # +
        if keys[pg.K_a]:  # +
            dx += speed_sin * 0.8  # +
            dy += -speed_cos * 0.8  # +
        if keys[pg.K_d]:  # +
            dx += -speed_sin  # +
            dy += speed_cos  # +

        self.check_wall_collision(dx, dy)  # +

        # control player angle using the keys
        # if keys[pg.K_LEFT]:
        #     self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
        # if keys[pg.K_RIGHT]:
        #     self.angle += PLAYER_ROT_SPEED * self.game.delta_time
        self.angle %= math.tau  # +

    def check_wall(self, x, y) -> bool:  # collisions  # +
        return (x, y) not in self.game.map.world_map  # +

    def check_wall_collision(self, dx, dy):  # collisions  # +
        scale = PLAYER_SIZE_SCALE / self.game.delta_time  # +
        if self.check_wall(int(self.x + dx * scale), int(self.y)):  # +
            self.x += dx  # +
        if self.check_wall(int(self.x), int(self.y + dy * scale)):  # +
            self.y += dy  # +

    def draw(self):  # +
        pg.draw.line(self.game.screen, YELLOW, (self.x * BLOCK_SIZE, self.y * BLOCK_SIZE),  # +
                     (self.x * BLOCK_SIZE + WIDTH * math.cos(self.angle),  # +
                      self.y * BLOCK_SIZE + WIDTH * math.sin(self.angle)), 2)  # +

        pg.draw.circle(self.game.screen, GREEN, (self.x * BLOCK_SIZE, self.y * BLOCK_SIZE), 15)  # +

    def mouse_control(self):
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        if my < HALF_HEIGHT or my > HALF_HEIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY

    def create_player_instances(self):  # unused yet
        for pid in range(1, self.number_of_players - 1):
            self.players[pid + 1] = PlayerModel(self.game, pid + 1)

    def send_data(self):
        self.client.send_data(f'{self.x},{self.y},{self.angle},{self.client.client_id}'.encode())  # send my position

    def recv_data(self):
        recv = self.client.client.recv(DATA_RECV_CHUNK)
        print(recv.decode('utf-8'))

    def update(self):  # +
        self.movement()
        self.mouse_control()
        self.recover_health()

        if self.game.network_game:
            self.send_data()
            self.recv_data()

        if not self.game.object_handler.no_npc:
            self.check_game_win()

    @property  # +
    def pos(self):
        return self.x, self.y

    @property  # +
    def map_pos(self) -> tuple:
        return int(self.x), int(self.y)


class PlayerModel(AnimatedSprite):

    def __init__(self, game, player_id, path='resources/sprites/npc/soldier/0.png',
                 pos=(10.5, 5.5), scale=0.6, shift=0.08, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.player_id = player_id

    def move(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        self.check_animation_time()
        self.get_sprite()
