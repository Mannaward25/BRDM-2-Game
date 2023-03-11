import socket
from game_settings import *
import _thread
import time
import json
import pickle

# server side logic


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

        print("Waiting for connection..")

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
        tmp.client_id = pid
        pid = tmp
        return pid

    def delete_player_from_server(self, pid: str) -> str:
        """if player quits"""

        del self.server_players[pid]
        print(f'deleted player with id {pid}')
        return pid

    def test_prep_data(self, data: str) -> tuple:  # will be replaced
        """test function to cook raw data from string to tuple
            format: float(x), float(y), float(angle), int(id)
        """
        data = data.split(',')
        if len(data) == 4:  # check if struct has 4 variables
            x, y, angle, player_id = data

            return float(x), float(y), float(angle), str(player_id)
        else:
            print('no data prepared!')

    def new_prep_data(self, data: 'ClientPlayerDataStruct'):  # YET TODO
        data = None
        if isinstance(data, ClientPlayerDataStruct):
            pass
        #return float(x), float(y), float(angle), str(player_id)  # YET TODO


    def update_player_data(self, player_struct: tuple, pid: str):
        x_pos, y_pos, angle, player_id = player_struct
        for _ in self.server_players.values():
            self.server_players[pid].set_pos(x_pos, y_pos)
            self.server_players[pid].set_angle(angle)

    def get_player_data(self, pid: str):
        all_data = {}

        for player_id, player_instance in self.server_players.items():
            if pid != player_instance.get_player_id():
                other_player_id, data = player_instance.get_all_data()
                all_data[other_player_id] = data
        return all_data

    def new_get_player_data(self, pid: str):
        all_data = {}

        for player_id, player_instance in self.server_players.items():  # player_instance: ServerPlayerDataStruct
            other_player_id = player_instance.get_player_id()
            if pid != other_player_id:
                all_data[other_player_id] = player_instance
        return all_data

    def threaded_client(self, conn, pid: 'HelloMsg'):
        conn.send(pickle.dumps(pid))
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
                    #reply = data.decode('utf-8')  # <--- get data from clients if we use string data transfer
                    reply: ClientPlayerDataStruct = pickle.loads(data)
                    print(f"Received: {reply}\n")
                    # player_struct = self.test_prep_data(reply)  # if we use string data transfer
                    player_struct = self.new_prep_data(reply)  # if we use pickle class data transfer  # YET TODO

                    if player_struct:
                        self.update_player_data(player_struct, pid)  # <---- update data of the player which send info

                    if reply == CLOSE:
                        self.close_connection(conn)
                        break

                    all_data = self.new_get_player_data(pid)
                    print(f"Sending {all_data}\n")

                    reply: bytes = pickle.dumps(all_data)  # json.dumps(all_data) if we use json structs

                conn.sendall(reply)  # reply.encode() if we use json
                print(f'self.clients = {self.clients}')
            except Exception:
                break

        print("Lost connection\n")
        self.delete_player_from_server(pid)
        self.conn.close()
        self.clients -= 1

    def run(self):

        while True:
            self.conn, self.address = self.sock.accept()
            self.clients += 1
            pid = self.assign_player_id(self.conn)
            print('ok')
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

        self.server = server
        self.port = port

        self.address = (self.server, self.port)

        self.client_pos = {
            '0': PLAYER_POS,
            '1': PLAYER_POS,
            '2': (2.5, 6.5)
        }

    def connect(self) -> str:

        try:
            self.client.connect(self.address)
            data = self.client.recv(DATA_RECV_CHUNK).decode()

            return data
        except:
            pass

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


class HelloMsg:

    def __init__(self, msg='', client_id='0'):

        self.client_id = client_id
        self.msg = f'Player {self.client_id} connected'

    @property
    def pid(self):
        return self.client_id


class ClientPlayerDataStruct:
    """struct we will pack into binary with pickle module
        and send to the server
    """
    def __init__(self, player_id='0'):
        self.player_id = player_id
        self.x = 0
        self.y = 0
        self.angle = 0
        self.health = 0

    def set_params(self, pos: tuple, angle, health):
        self.x, self.y = pos
        self.angle = angle
        self.health = health

    def set_player_id(self, player_id):
        self.player_id = player_id


class ServerPlayerDataStruct:
    """what we will store in server memory"""
    def __init__(self, conn, player_id="0"):
        self.player_id = player_id
        self.connection_instance = conn
        self.x = 0
        self.y = 0
        self.angle = 0
        self.health = 0

    def set_pos(self, x, y):
        self.x, self.y = x, y

    def get_pos(self):
        return self.x, self.y

    def set_angle(self, angle):
        self.angle = angle

    def get_angle(self):
        return self.angle

    def get_all_data(self):
        return self.player_id, f'{self.x},{self.y},{self.angle}'

    def get_player_id(self):
        return self.player_id

    def set_player_id(self, player_id):
        self.player_id = player_id


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

