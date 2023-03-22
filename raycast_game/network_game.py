import socket
from game_settings import *
import _thread
import time
import json
import pickle

# server side logic


class HelloMsg:

    def __init__(self, msg='', client_id='0'):

        self.client_id = client_id
        self.msg = f'Player {client_id} connected'

    @property
    def pid(self):

        return self.client_id

    def set_client_id(self, client_id):
        self.msg = f'Player {client_id} connected'
        self.client_id = client_id


class Client:

    def __init__(self, game, server=LOCAL_SERVER_IP, port=PORT):
        self.game = game
        self.client_id = '0'
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if server:
            self.server = server
        else:
            self.server = LOCAL_SERVER_IP

        if port:
            self.port = port
        else:
            self.port = PORT

        self.address = (self.server, self.port)

        self.client_pos = {
            '0': PLAYER_POS,
            '1': PLAYER_POS,
            '2': (2.5, 6.5),
            '3': (12.1, 2.1)
        }

    def connect(self) -> bytes:
        data = ''
        try:
            self.client.connect(self.address)
            data: bytes = self.client.recv(DATA_RECV_CHUNK)
            #time.sleep(2)
            #data: HelloMsg = pickle.loads(data)

        except Exception as err:
            print('error')

        return data

    def get_init_pos(self) -> tuple:
        """
        returns pair of values: x,y
        """
        return self.client_pos[self.client_id]

    def set_client_id(self, num):
        self.client_id = str(num)

    def get_client_id(self):
        return str(self.client_id)

    def send_msg(self, msg: str):
        """for service use only"""
        self.client.send(msg.encode())

    def send_data(self, data):
        """for data exchanging"""
        self.client.send(data)

    def close(self):
        self.client.close()


class PlayerDataStruct:

    def __init__(self, player_id, pos: tuple = (0, 0), angle=0.0, walk=False, health=0):
        self.player_id = player_id
        self.x, self.y = pos
        self.angle = angle
        self.health = health
        self.sin, self.cos = 0, 0
        self.is_walking = walk
        self.alive = True

        # shot state
        self.shot = False
        self.damage = 0
        self.hit = {}

        # ray_cast info
        self.ray_cast_visible = {}

    def set_params(self, pos: tuple, angle, polars=(0, 0), walk=False, health=0):
        self.x, self.y = pos
        self.angle = angle
        self.health = health
        self.sin, self.cos = polars
        self.is_walking = walk

    def set_shot_state(self, shot: bool, damage: int, hit: dict):
        self.damage = damage
        self.shot = shot
        self.hit = hit

    def set_alive_status(self, alive: bool):
        self.alive = alive

    def get_alive_status(self):
        return self.alive

    def get_shot_state(self):
        return self.shot, self.damage, self.hit.copy()

    def get_params(self):
        return self.x, self.y, self.angle, self.health, self.sin, self.cos

    def set_player_id(self, player_id):
        self.player_id = player_id

    def get_player_id(self):
        return self.player_id

    def get_player_data(self):
        return self.x, self.y, self.angle, self.health, self.sin, self.cos, self.is_walking

    def set_ray_cast_result(self, ray_cast: dict):
        self.ray_cast_visible = ray_cast

    def get_ray_cast_result(self):
        return self.ray_cast_visible.copy()

    def set_pos(self, x, y):
        self.x, self.y = x, y

    def get_pos(self):
        return self.x, self.y

    def set_angle(self, angle):
        self.angle = angle

    def get_angle(self):
        return self.angle

    def show(self):
        print(f'player_id: {self.player_id}; pos:({self.x}, {self.y}); angle: {self.angle}; health: {self.health};')


class ClientPlayerDataStruct(PlayerDataStruct):
    """struct we will pack into binary with pickle module
        and send to the server
    """
    def __init__(self, player_id='0'):
        x, y, angle, health = 0, 0, 0, 0
        walk = False
        super().__init__(player_id, (x, y), angle, walk, health)


class ServerPlayerDataStruct(PlayerDataStruct):
    """what we will store in server memory"""
    def __init__(self, conn, player_id="0"):
        x, y, angle, health = 0, 0, 0, 0
        walk = False
        super().__init__(player_id, (x, y), angle, walk, health)
