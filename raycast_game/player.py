import pygame as pg  # +
import math  # +
from game_settings import *  # +
from network_game import Client, ServerPlayerDataStruct, HelloMsg, ClientPlayerDataStruct
from sprite_object import AnimatedSprite
import pickle
import time


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

        self.ray_cast_visible = {}  # {pid: bool(value)}
        self.hit = {}  # {pid: bool(value)}
        self.eye_contact = {}  # {pid: bool(value)}
        self.alive = True

        self.angle_diff = 0
        self.sin, self.cos = 0, 0
        self.is_walking = False

        tries = 0  # hardcode
        if self.game.HOST or self.game.network_game:
            while not self.try_connect() and tries < 3:
                print("unsuccessful connection retrial in 3 sec")
                time.sleep(3)
                tries += 1

        if self.game.network_game:
            self.x, self.y = self.client.get_init_pos()

    def try_connect(self):
        msg: bytes = self.client.connect()
        if msg:
            msg: HelloMsg = pickle.loads(msg)
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
        if self.health < 1 and not self.game.network_game:
            self.game.object_renderer.game_over()
            pg.display.flip()
            pg.time.delay(1500)
            self.game.new_game()
        elif self.health < 1 and self.game.network_game:
            self.game.object_renderer.game_over()
            pg.display.flip()
            pg.time.delay(400)
            self.alive = False

    def reset_player_params(self):  # for network game
        pg.time.delay(400)
        self.x, self.y = self.client.get_init_pos()
        self.health = 100
        self.angle = PLAYER_ANGLE
        self.alive = True

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

    def send_data(self):
        self.player_data.set_player_id(self.client.client_id)
        self.player_data.set_params((self.x, self.y), self.angle,
                                    (self.sin, self.cos),
                                    self.is_walking, self.health)

        self.player_data.set_ray_cast_result(self.ray_cast_visible.copy())  # pack deep copy
        self.player_data.set_shot_state(self.shot, self.game.weapon.damage, self.hit.copy())  # send damage info!
        self.player_data.set_alive_status(self.alive)

        self.client.send_data(pickle.dumps(self.player_data))

    def recv_data(self) -> dict:
        recv: bytes = self.client.client.recv(DATA_RECV_CHUNK)
        msg = pickle.loads(recv)
        return msg

    def eye_contact_check(self, pid, other_ray_cast_val: dict):  # rc_val = {pid: bool(value)}
        if self.ray_cast_visible[pid] and other_ray_cast_val.get(self.client.client_id, False):
            self.eye_contact[pid] = True
        else:
            self.eye_contact[pid] = False

    def delete_player_instance(self, data: dict):
        if len(data) < len(self.players):  # deletes quited players
            pid_to_delete = None
            for pid, instance in self.players.items():
                if pid not in data:
                    pid_to_delete = pid

            print(f'player id {pid_to_delete} quit the server')
            del self.players[pid_to_delete]
            del self.ray_cast_visible[pid_to_delete]
            del self.eye_contact[pid_to_delete]
            del self.hit[pid_to_delete]

    def update_player_instances(self, data: dict):
        self.delete_player_instance(data)  # check invalid player instances

        for pid, instance in data.items():
            if pid not in self.players:
                player_struct = self.parse_data(data[pid])

                x, y, angle, sin, cos, walk, shot, dmg, rc_val, hp, hit, alive = player_struct  # unpack hit value
                # do we see other player?
                self.ray_cast_visible[pid] = self.player_to_player_ray_cast(other_pos=(x, y))
                # does other player see us?
                self.eye_contact_check(pid, rc_val)

                self.players[pid] = PlayerModel(self.game, pid, pos=(x, y))
                self.players[pid].set_angle_diff(self.angle, angle)
                self.players[pid].position_diff((self.x, self.y), (x, y))
                self.players[pid].set_other_params(walk)
                self.players[pid].set_alive_status(alive)
                self.players[pid].update_model((self.sin, self.cos), (sin, cos))

    def update_server_info(self, data: dict):
        self.number_of_players = len(data) + 1

        if data:
            if data.keys() == self.players.keys():
                for pid in data.keys():
                    player_struct = self.parse_data(data[pid])
                    x, y, angle, sin, cos, walk, shot, dmg, rc_val, hp, hit, alive = player_struct  # unpack hit value
                    # do we see other player?
                    self.ray_cast_visible[pid] = self.player_to_player_ray_cast(other_pos=(x, y))
                    # does other player see us?
                    self.eye_contact_check(pid, rc_val)

                    self.players[pid].move(x, y)
                    self.players[pid].set_angle_diff(self.angle, angle)
                    self.players[pid].position_diff((self.x, self.y), (x, y))
                    self.players[pid].set_other_params(walk)

                    # check if we hit other player
                    if hit.get(self.client.client_id, False):
                        print('shot')
                        shot = True

                    if shot:
                        self.game.sound.shotgun.set_volume(self.players[pid].calc_shot_volume())
                        self.game.sound.shotgun.play()

                    self.players[pid].set_shot_status(shot)

                    if self.eye_contact[pid] and self.shot and self.players[pid].check_hit():
                        self.hit[pid] = True
                        self.players[pid].make_pain()
                        print(self.hit, shot)
                    else:
                        self.hit[pid] = False

                    if self.eye_contact[pid] and hit.get(self.client.client_id, False):
                        print(f'i have  {self.health}hp and get damage = ', dmg)
                        self.get_damage(dmg)

                    self.players[pid].set_alive_status(alive)
                    self.players[pid].update_model((self.sin, self.cos), (sin, cos))
            else:
                self.update_player_instances(data)
        else:
            self.delete_player_instance(data)  # check invalid player instances

    def test_parse_data(self, string_data: str) -> tuple:
        x, y, angle = string_data.split(',')
        return float(x), float(y), float(angle)

    def parse_data(self, obj_data: ServerPlayerDataStruct, raycast=False) -> tuple:
        if raycast:
            x, y = obj_data.get_pos()
            return float(x), float(y)
        else:
            x, y, angle, hp, sin, cos, walk = obj_data.get_player_data()
            shot, dmg, hit = obj_data.get_shot_state()
            rc_val: dict = obj_data.get_ray_cast_result()
            alive = obj_data.get_alive_status()
            return (float(x), float(y), float(angle), float(sin), float(cos),
                    bool(walk), bool(shot), int(dmg), rc_val, int(hp), hit, bool(alive))

    def player_to_player_ray_cast(self, other_pos) -> bool:
        # calc theta
        if self.pos == other_pos:
            return True

        other_x, other_y = other_pos
        dx = other_x - self.x
        dy = other_y - self.y
        other_map_pos = int(other_x), int(other_y)
        theta = math.atan2(dy, dx)

        # calc ray cast
        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0

        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = theta
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
            if tile_hor == other_map_pos:
                player_dist_h = depth_hor
                break
            if tile_hor in self.game.map.world_map:
                wall_dist_h = depth_hor
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
            if tile_vert == other_map_pos:
                player_dist_v = depth_vert
                break
            if tile_vert in self.game.map.world_map:
                wall_dist_v = depth_vert
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        player_dist = max(player_dist_v, player_dist_h)
        wall_dist = max(wall_dist_v, wall_dist_h)

        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        return False

    def update(self):  # +

        self.movement()
        self.mouse_control()
        self.recover_health()

        if self.game.network_game:

            self.send_data()
            data = self.recv_data()

            if not self.alive:
                self.reset_player_params()

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
                 pos=(2.5, 6.5), scale=0.6, shift=0.38, animation_time=360):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.player_id = player_id
        self.attack_images = self.get_images(self.path + '/attack')
        self.death_images = self.get_images(self.path + '/death')
        self.idle_images = self.get_images(self.path + '/idle')
        self.pain_images = self.get_images(self.path + '/pain')
        self.walk_images = self.get_images(self.path + '/walk')

        self.frame_counter = 0  # death
        self.attack_frame_counter = 0
        self.pain_frame_counter = 0
        self.attack_animation_trigger = False
        self.pain_animation_trigger = False

        # rotation
        self.angle_difference = 0
        self.player_pos = (0, 0)
        self.model_pos = pos
        self.model_angle = 0
        self.player_angle = 0
        self.player_angle_standard = 0
        self.model_angle_standard = 0
        self.player_theta = 0  # player_theta
        self.sin, self.cos = 0, 0
        self.model_dir = EAST
        self.player_dir = EAST
        self.pos_diff_x = 0
        self.pos_diff_y = 0

        # state flags
        self.is_walking = False
        self.alive = True
        self.pain = False
        self.is_attacking = False
        self.ray_cast_visible = False

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

        self.model_dir = self.get_direction(m_sin, m_cos, self.model_angle_standard)
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
        elif (sin < 0 and (cos > 0 or cos < 0)) and HALF_PI - player_const < standard_angle <= HALF_PI:
            return NORTH
        elif (sin > 0 and (cos > 0 or cos < 0)) and HALF_PI - player_const < standard_angle <= HALF_PI:
            return SOUTH
        elif (cos > 0 and sin > 0) and player_const < standard_angle <= HALF_PI - player_const:
            return SE
        elif (cos < 0 < sin) and player_const < standard_angle <= HALF_PI - player_const:
            return SW
        elif (cos > 0 > sin) and player_const < standard_angle <= HALF_PI - player_const:
            return NE
        elif (cos < 0 > sin) and player_const < standard_angle <= HALF_PI - player_const:
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

        self.directions(player_polar, model_polar)
        left_border = H_PI_DEG - PLAYER_MODEL_CONSTANT  # 90 deg - const
        # print(f'angle: ({angle_degrees} degrees); '
        #       f'player_dir: {self.dirs[self.player_dir]}; '
        #       f'model_dir: {self.dirs[self.model_dir]}; '
        #       f'is_complanar: {self.is_complanar()}, is_perpend: {self.is_perpend()}, is_right: {self.is_right()}')

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

    def get_image(self, path):
        img = pg.image.load(path).convert_alpha()
        return img

    def set_angle_diff(self, player_angle, model_angle):
        self.model_angle = model_angle
        self.player_angle = player_angle
        self.player_angle_standard = self.standardize_angle(player_angle)
        self.model_angle_standard = self.standardize_angle(model_angle)
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
        self.model_pos = model_pos
        self.player_pos = player_pos
        px, py = player_pos
        mx, my = model_pos
        diff_x, diff_y = abs(px - mx), abs(py - my)
        self.pos_diff_x, self.pos_diff_y = diff_x, diff_y

        player_theta_tmp = math.atan2(diff_y, diff_x)
        player_theta = abs(player_theta_tmp - self.model_angle)

        self.player_theta = self.standardize_angle(player_theta)  # player_theta

    def idle_moves(self, player_polar, model_polar):  # player_polar(sin, cos), model_polar(sin, cos)
        self.image = self.rotation_image(player_polar, model_polar)

    def show_walk(self):
        """test function"""
        print(f'is walking {self.is_walking}')

    def set_other_params(self, walk):
        self.is_walking = walk

    def animate_attack(self):
        if not self.is_complanar() and not self.is_perpend():
            if self.game.global_trigger and self.attack_frame_counter < len(self.attack_images):

                self.attack_images.rotate(-1)
                self.image = self.attack_images[0]
                self.attack_frame_counter += 1
        elif self.is_perpend():
            if self.is_right():
                self.image = self.player_view[6]
            else:
                self.image = self.player_view[2]
            self.attack_animation_trigger = False
        else:
            self.image = self.player_view[4]
            self.attack_animation_trigger = False

    def animate_death(self):
        if not self.alive:
            if self.game.global_trigger and self.frame_counter < len(self.death_images) - 1:
                self.death_images.rotate(-1)
                self.image = self.death_images[0]
                self.frame_counter += 1

    def reset_frame_counter(self):
        if self.frame_counter >= len(self.death_images) - 1:
            self.frame_counter = 0

        if self.attack_frame_counter >= len(self.attack_images) - 1:
            self.attack_frame_counter = 0
            self.attack_animation_trigger = False

        if self.pain_frame_counter >= len(self.pain_images) - 1:
            self.pain_frame_counter = 0
            self.pain_animation_trigger = False

    def animate_pain(self):
        if self.game.global_trigger and self.attack_frame_counter < len(self.pain_images):
            self.pain_images.rotate(-1)
            self.image = self.pain_images[0]
            self.pain_frame_counter += 1
            self.pain = False

    def walking(self):
        """includes self.animate_walk()"""
        if not self.is_complanar() and not self.is_perpend():
            self.animate(self.walk_images)
        elif self.is_perpend():
            if self.is_right():
                self.image = self.player_view[6]
            else:
                self.image = self.player_view[2]
        else:
            self.image = self.player_view[4]

    def check_hit(self) -> bool:
        if HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width:
            return True
        return False

    def make_pain(self):
        self.game.sound.npc_pain.play()
        self.pain = True

    def calc_shot_volume(self) -> float:  # 0 to 1
        vol = 1 / math.hypot(self.pos_diff_x, self.pos_diff_y)
        return vol

    def set_alive_status(self, alive: bool):
        self.alive = alive

    def set_shot_status(self, shot: bool):
        self.is_attacking = shot

    def update_model(self, player_polar, model_polar):

        if self.alive:
            if self.pain or self.pain_animation_trigger:
                if self.pain:
                    self.pain_animation_trigger = self.pain
                self.animate_pain()
            elif self.is_walking:
                self.walking()
            elif self.is_attacking or self.attack_animation_trigger:
                if self.is_attacking:
                    self.attack_animation_trigger = self.is_attacking
                self.animate_attack()
            else:
                self.idle_moves(player_polar, model_polar)
        else:
            self.animate_death()

        self.check_animation_time()
        self.get_sprite()
        self.reset_frame_counter()
