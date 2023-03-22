import socket
from game_settings import *
import _thread
import time
import json
import pickle
import re
from network_game import *


class DedicatedServer:
    def __init__(self, ip_address=''):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if ip_address:
            self.server = ip_address
        else:
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

        print(f"Waiting for connection on server [{self.server}:{PORT}]..")

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


def validate_ip(text):
    pattern = r'^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$'
    res = re.search(pattern, text)
    if res:
        return True
    else:
        print(f'Enter valid ip address!\n')
        return False


def main():
    ip_address = ''
    while not validate_ip(ip_address):
        ip_address = input(':>| ')

    print(ip_address)
    server_host = DedicatedServer(ip_address=ip_address)
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
