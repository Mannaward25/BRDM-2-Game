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


class DedicatedServer:
    def __init__(self):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = LOCAL_SERVER_IP
        self.port = PORT
        self.conn = None
        self.address = None

        self.clients = 0  # total number of clients on the server
        self.server_players = {}  # table of players
        self.player_positions = {}

        self.server_ip = socket.gethostbyname(self.server)

    def bind_socket(self):
        try:
            self.sock.bind((self.server, self.port))
        except socket.error as err:
            print(str(err))

    def start(self):
        self.bind_socket()
        self.sock.listen(MAX_PLAYERS)

        print(f"Waiting for connection on server [{LOCAL_SERVER_IP}:{PORT}]..")

    def assign_player_id(self, conn) -> 'HelloMsg':
        """player gets unique id after connecting to the server"""
        tmp = HelloMsg()
        pid = tmp.pid
        if not self.server_players:
            pid = str(self.clients)
            self.server_players[pid] = ServerPlayerDataStruct(conn, player_id=pid)
        else:
            if str(self.clients) not in self.server_players:
                pid = str(self.clients)
                self.server_players[pid] = ServerPlayerDataStruct(conn, player_id=pid)
            else:
                for player_id in range(1, self.clients + 1):
                    if str(player_id) not in self.server_players:
                        pid = str(player_id)
                        self.server_players[pid] = ServerPlayerDataStruct(conn, player_id=pid)
        tmp.set_client_id(pid)
        pid = tmp
        return pid

    def delete_player_from_server(self, pid: str) -> str:
        """if player quits"""

        del self.server_players[pid]
        print(f'deleted player with id {pid}')
        return pid

    def new_prep_data(self, data: 'ClientPlayerDataStruct') -> tuple:
        if data:
            x, y, angle, health, sin, cos, walk = data.get_player_data()
            shot_state, damage, hit = data.get_shot_state()
            raycast_val: dict = data.get_ray_cast_result()
            alive = data.get_alive_status()
            player_id = data.get_player_id()
            return (float(x), float(y), float(angle), float(sin), float(cos), bool(walk), raycast_val,
                    bool(shot_state), int(damage), int(health), hit, bool(alive),
                    str(player_id))
        return tuple()

    def update_player_data(self, player_struct: tuple, pid: str):
        x_pos, y_pos, angle, sin, cos, walk, rc_val, shot, dmg, hp, hit, alive, _ = player_struct
        self.server_players[pid].set_params(pos=(x_pos, y_pos), angle=angle, polars=(sin, cos), walk=walk, health=hp)
        self.server_players[pid].set_shot_state(shot, dmg, hit.copy())
        self.server_players[pid].set_ray_cast_result(rc_val.copy())
        self.server_players[pid].set_alive_status(alive)

    def new_get_player_data(self, pid: str):
        all_data = {}

        for player_id, player_instance in self.server_players.items():  # player_instance: ServerPlayerDataStruct
            other_player_id = player_instance.get_player_id()
            if pid != other_player_id:
                all_data[other_player_id] = player_instance
        return all_data

    def threaded_client(self, conn, pid):
        conn.send(pickle.dumps(pid, protocol=pickle.HIGHEST_PROTOCOL))
        pid = pid.pid  # get str from class HelloMsg()

        reply = ''
        while True:
            if self.clients > MAX_PLAYERS:
                print("too much players")
                raise Exception('Too much players')
            try:
                data = conn.recv(DATA_RECV_CHUNK)

                if not data:
                    print("Disconnected")
                    break
                else:
                    reply: ClientPlayerDataStruct = pickle.loads(data)
                    #print(f"Received: {reply}\n")

                    # pack data into tuple if we use pickle class data transfer
                    player_struct = self.new_prep_data(reply)

                    if player_struct:
                        self.update_player_data(player_struct, pid)  # <---- update data of the player which send info

                    if reply == CLOSE:
                        self.close_connection(conn)
                        break

                    all_data = self.new_get_player_data(pid)
                    #print(f"Sending {all_data}\n")

                    # pickle.dumps(all_data) if we use pickle structs
                    reply: bytes = pickle.dumps(all_data, protocol=pickle.HIGHEST_PROTOCOL)

                conn.sendall(reply)  # reply.encode() if we use json
                #print(f'self.clients = {self.clients}')
            except Exception as err:
                print('Server Exception arose ', err)
                break

        print("Lost connection\n")
        self.delete_player_from_server(pid)
        self.clients -= 1

    def run(self):

        while True:
            self.conn, self.address = self.sock.accept()
            self.clients += 1
            pid = self.assign_player_id(self.conn)
            thread_id = _thread.start_new_thread(self.threaded_client, (self.conn, pid))
            print(f"connected to {self.address}")

    def close_connection(self, conn):
        conn.close()
        self.sock.close()


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


def main():
    server_host = DedicatedServer()
    server_host.start()
    server_host.run()


if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        print("error: ", err)
        time.sleep(3)
        print("wait for reloading 3 sec...")
        main()

