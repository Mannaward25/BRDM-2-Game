import time

import pygame as pg  # +
import math  # +
import numpy as np
from game_settings import *  # +
from network_game import Client, ServerPlayerDataStruct, HelloMsg, ClientPlayerDataStruct
from sprite_object import AnimatedSprite
import json
import pickle


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
        self.player_data = ClientPlayerDataStruct()
        self.number_of_players = 0
        self.players = {}

        self.angle_diff = 0
        self.sin, self.cos = 0, 0

        tries = 0  # hardcode
        if self.game.HOST or self.game.network_game:
            while not self.try_connect() and tries < 3:
                print("unsuccessful connection retrial in 3 sec")
                time.sleep(4)
                tries += 1

        if self.game.network_game:
            self.x, self.y = self.client.get_init_pos()

    def try_connect(self):
        msg: bytes = self.client.connect()
        msg: HelloMsg = pickle.loads(msg)
        if msg:
            num = msg.pid
            self.client.set_client_id(num)
            print(msg, f'from Client_id {num} .__init__')
            del msg
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
        self.sin = sin_a
        self.cos = cos_a
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
        #print(self.angle)

    def update_player_instances(self, data: dict):  # unused yet
        for pid, instance in data.items():
            if pid not in self.players:
                player_struct = self.parse_data(data[pid])
                x, y, angle, sin, cos = player_struct
                self.players[pid] = PlayerModel(self.game, pid, pos=(x, y))
                self.players[pid].set_angle_diff(self.angle, angle)
                self.players[pid].position_diff((self.x, self.y), (x, y))
                self.players[pid].player_direction((self.sin, self.cos), (sin, cos))
                self.players[pid].update()

    def send_data(self):
        self.player_data.set_player_id(self.client.client_id)
        self.player_data.set_params((self.x, self.y), self.angle, (self.sin, self.cos), self.health)

        #self.client.send_data(f'{self.x},{self.y},{self.angle},{self.client.client_id}'.encode())  # send my position
        self.client.send_data(pickle.dumps(self.player_data))  # READY

    def recv_data(self) -> dict:
        recv: bytes = self.client.client.recv(DATA_RECV_CHUNK)
        #print(recv.decode('utf-8'), len(recv.decode('utf-8')))
        #msg: dict = json.loads(recv.decode('utf-8'))  # deserialized json data
        msg = pickle.loads(recv)
        return msg

    def update_server_info(self, data: dict):
        self.number_of_players = len(data) + 1

        if data:
            if data.keys() == self.players.keys():
                for pid in data.keys():
                    player_struct = self.parse_data(data[pid])
                    x, y, angle, sin, cos = player_struct
                    self.players[pid].move(x, y)
                    self.players[pid].set_angle_diff(self.angle, angle)
                    self.players[pid].position_diff((self.x, self.y), (x, y))
                    self.players[pid].show_theta()
                    self.players[pid].player_direction((self.sin, self.cos), (sin, cos))
                    self.players[pid].update()
            else:
                self.update_player_instances(data)

    def test_parse_data(self, string_data: str) -> tuple:
        x, y, angle = string_data.split(',')
        return float(x), float(y), float(angle)

    def parse_data(self, obj_data: ServerPlayerDataStruct) -> tuple:
        x, y, angle, health, sin, cos = obj_data.get_params()
        return float(x), float(y), float(angle), float(sin), float(cos)

    def update(self):  # +
        self.movement()
        self.mouse_control()
        self.recover_health()

        if self.game.network_game:
            self.send_data()
            data = self.recv_data()
            self.update_server_info(data)

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
                 pos=(2.5, 6.5), scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.player_id = player_id
        self.attack_images = self.get_images(self.path + '/attack')
        self.death_images = self.get_images(self.path + '/death')
        self.idle_images = self.get_images(self.path + '/idle')
        self.pain_images = self.get_images(self.path + '/pain')
        self.walk_images = self.get_images(self.path + '/walk')

        # rotation
        self.angle_difference = 0
        self.model_angle = 0
        self.player_angle = 0
        self.player_angle_standard = 0
        self.player_theta = 0  # player_theta
        self.sin, self.cos = 0, 0
        self.model_dir = EAST
        self.player_dir = EAST
        """
        0 - front
        1 - left_front
        2 - left
        3 - left_rear
        4 - rear
        5 - right_rear
        6 - right
        7 - right_front
        
        """

        self.dirs = {
            NORTH: 'NORTH',
            SOUTH: 'SOUTH',
            EAST: 'EAST',
            WEST: 'WEST',
            NE: 'NORTH_EAST',
            NW: 'NORTH_WEST',
            SE: 'SOUTH_EAST',
            SW: 'SOUTH_WEST'
        }

        self.player_view = {
            0: self.get_image(self.path + '/idle' + '/0.png'),
            1: self.get_image(self.path + '/idle' + '/1.png'),
            2: self.get_image(self.path + '/idle' + '/2.png'),
            3: self.get_image(self.path + '/idle' + '/3.png'),
            4: self.get_image(self.path + '/idle' + '/4.png'),
            5: self.get_image(self.path + '/idle' + '/5.png'),
            6: self.get_image(self.path + '/idle' + '/6.png'),
            7: self.get_image(self.path + '/idle' + '/7.png')
        }

    def move(self, x, y):
        self.x = x
        self.y = y

    def directions(self, player_polar, model_polar):
        p_sin, p_cos = player_polar
        m_sin, m_cos = model_polar

        # model_direction
        self.model_dir = self.get_direction(m_sin, m_cos, self.player_theta)
        self.player_dir = self.get_direction(p_sin, p_cos, self.player_angle_standard)

    @staticmethod
    def get_direction(sin, cos, standard_angle):
        player_const = math.radians(PLAYER_MODEL_CONSTANT)
        sin += 0.000000001
        cos += 0.000000001

        if (cos > 0 and (sin > 0 or sin < 0)) and standard_angle <= player_const:
            return EAST
        elif (cos < 0 and (sin > 0 or sin < 0)) and standard_angle <= player_const:
            return WEST
        elif (sin < 0 and (cos > 0 or cos < 0)) and HALF_PI - player_const < standard_angle < HALF_PI + player_const:
            return NORTH
        elif (sin > 0 and (cos > 0 or cos < 0)) and HALF_PI - player_const < standard_angle < HALF_PI + player_const:
            return SOUTH
        elif (cos > 0 and sin > 0) and player_const < standard_angle < HALF_PI - player_const:
            return SE
        elif (cos < 0 < sin) and player_const < standard_angle < HALF_PI - player_const:
            return SW
        elif (cos > 0 > sin) and player_const < standard_angle < HALF_PI - player_const:
            return NE
        elif (cos < 0 > sin) and player_const < standard_angle < HALF_PI - player_const:
            return NW

    def check_directions_variables(self):
        if not self.player_dir:
            self.player_dir = EAST
        if not self.model_dir:
            self.model_dir = EAST

        px, py = self.player_dir
        mx, my = self.model_dir
        return px, py, mx, my

    def is_complanar(self) -> bool:
        px, py, mx, my = self.check_directions_variables()

        if ((px == mx) and px != 0) or ((py == my) and py != 0):
            return True
        return False

    def is_perpend(self) -> bool:
        """is perpendicular"""
        px, py, mx, my = self.check_directions_variables()

        if ((px, py) == NORTH or (px, py) == SOUTH) and ((mx, my) == EAST or (mx, my) == WEST):
            return True
        elif ((px, py) == EAST or (px, py) == WEST) and ((mx, my) == NORTH or (mx, my) == SOUTH):
            return True
        elif ((px, py) == NE or (px, py) == SW) and ((mx, my) == NW or (mx, my) == SE):
            return True
        elif ((px, py) == NW or (px, py) == SE) and ((mx, my) == NE or (mx, my) == SW):
            return True
        return False

    def is_right(self) -> bool:
        px, py, mx, my = self.check_directions_variables()

        if ((px, py) == NORTH and (mx, my) == EAST) or ((px, py) == SOUTH and (mx, my) == WEST):
            return True
        elif ((px, py) == EAST and (mx, my) == SOUTH) or ((px, py) == WEST and (mx, my) == NORTH):
            return True
        elif ((px, py) == NW and (mx, my) == NE) or ((px, py) == SE and (mx, my) == SW):
            return True
        elif ((px, py) == NE and (mx, my) == SE) or ((px, py) == SW and (mx, my) == NW):
            return True

        elif (px, py) == NORTH and ((mx, my) == NE or (mx, my) == SE):
            return True
        elif (px, py) == SOUTH and ((mx, my) == NW or (mx, my) == SW):
            return True
        elif (px, py) == EAST and ((mx, my) == SW or (mx, my) == SE):
            return True
        elif (px, py) == WEST and ((mx, my) == NW or (mx, my) == NE):
            return True

        elif (px, py) == NW and ((mx, my) == NORTH or (mx, my) == EAST):
            return True
        elif (px, py) == SE and ((mx, my) == EAST or (mx, my) == SOUTH):
            return True
        elif (px, py) == SW and ((mx, my) == NORTH or (mx, my) == WEST):
            return True
        elif (px, py) == NE and ((mx, my) == EAST or (mx, my) == SOUTH):
            return True

        return False

    def rotation_image(self, player_polar, model_polar):
        angle_degrees = math.degrees(self.player_theta)
        p_sin, p_cos = player_polar
        m_sin, m_cos = model_polar

        self.directions(player_polar, model_polar)
        left_border = H_PI_DEG - PLAYER_MODEL_CONSTANT  # 90 deg - const
        right_border = H_PI_DEG + PLAYER_MODEL_CONSTANT
        print(f'angle: ({angle_degrees} degrees); '
              f'player_dir: {self.dirs[self.player_dir]}; '
              f'model_dir: {self.dirs[self.model_dir]}; '
              f'is_complanar: {self.is_complanar()}, is_perpend: {self.is_perpend()}, is_right: {self.is_right()}')

        if angle_degrees < PLAYER_MODEL_CONSTANT and not self.is_complanar() and not self.is_perpend():
            return self.player_view[0]
        elif angle_degrees < PLAYER_MODEL_CONSTANT and self.is_complanar() and not self.is_perpend():
            return self.player_view[4]
        elif left_border < angle_degrees <= H_PI_DEG and self.is_perpend():
            if self.is_right():
                return self.player_view[6]
            return self.player_view[2]
        elif PLAYER_MODEL_CONSTANT < angle_degrees <= left_border and not self.is_complanar() and not self.is_perpend():
            if self.is_right():
                return self.player_view[7]
            return self.player_view[1]
        elif PLAYER_MODEL_CONSTANT < angle_degrees <= left_border and self.is_complanar() and not self.is_perpend():
            if self.is_right():
                return self.player_view[5]
            return self.player_view[3]
        else:
            return self.player_view[0]

        # elif PLAYER_MODEL_CONSTANT < abs(angle_degrees) <= left_border and not self.is_complanar() and not self.is_perpend():
        #     if self.is_right():
        #         return self.player_view[7]
        #     return self.player_view[1]


    def get_image(self, path):
        img = pg.image.load(path).convert_alpha()
        return img

    def set_angle_diff(self, player_angle, model_angle):
        self.model_angle = model_angle
        self.player_angle = player_angle
        self.player_angle_standard = self.standardize_angle(player_angle)
        diff1 = abs(player_angle - model_angle)
        diff2 = abs(diff1 - math.tau)
        min_diff = min(diff1, diff2)
        self.angle_difference = min_diff

    def standardize_angle(self, angle):
        if (angle % HALF_PI) == 0 and angle // HALF_PI > 0:
            angle = HALF_PI
        elif (angle % HALF_PI) != 0 and (angle // HALF_PI) % 2 == 0:
            angle = angle % HALF_PI
        elif (angle % HALF_PI) != 0 and (angle // HALF_PI) % 2 == 1:
            angle = HALF_PI - (angle % HALF_PI)
        elif (angle % HALF_PI) == 0 and angle // HALF_PI == 0:
            angle = 0.0

        return angle

    def position_diff(self, player_pos, model_pos):
        px, py = player_pos
        mx, my = model_pos
        diff_x, diff_y = abs(px - mx), abs(py - my)

        player_theta_tmp = math.atan2(diff_y, diff_x)
        player_theta = abs(player_theta_tmp - self.model_angle)

        self.player_theta = self.standardize_angle(player_theta)  # player_theta

    def player_direction(self, player_polar, model_polar):  # player_polar(sin, cos), model_polar(sin, cos)
        self.image = self.rotation_image(player_polar, model_polar)

    def show_theta(self):
        print(self.player_theta, f'{math.degrees(self.player_theta)} degrees')

    def update(self):
        self.check_animation_time()
        self.get_sprite()
        #self.animate(self.idle_images)
