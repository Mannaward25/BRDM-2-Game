import socket
from game_settings import *
import _thread
import time

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

    def assign_player_id(self, conn) -> int:
        """player gets unique id after connecting to the server"""
        pid = 0
        if not self.server_players:
            self.server_players[self.clients] = PlayerDataStruct(conn, player_id=self.clients)
            pid = self.clients
        else:
            if self.clients not in self.server_players:
                self.server_players[self.clients] = PlayerDataStruct(conn, player_id=self.clients)
                pid = self.clients
            else:
                for player_id in range(1, self.clients + 1):
                    if player_id not in self.server_players:
                        self.server_players[player_id] = PlayerDataStruct(conn, player_id=player_id)
                        pid = player_id
        return pid

    def delete_player_from_server(self, conn) -> int:
        """if player quits"""
        pid = 0
        for player_id, player_instance in self.server_players.items():
            if player_instance.connection_instance == conn:
                pid = player_instance.player_id
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

            return float(x), float(y), float(angle), int(player_id)
        else:
            print('no data prepared!')

    def update_player_data(self, player_struct: tuple):
        x_pos, y_pos, angle, player_id = player_struct
        for instance in self.server_players.values():
            if player_id == instance.get_player_id:
                instance.set_pos(x_pos, y_pos)
                instance.set_angle(angle)

    def get_player_data(self, pid):
        all_data = {}

        for player_id, player_instance in self.server_players.items():
            if pid != player_instance.get_player_id():
                other_player_id, data = player_instance.get_all_data()
                all_data[other_player_id] = data
        return all_data

    def threaded_client(self, conn, pid):

        conn.send(f"Connected player_id {pid}".encode())

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
                    reply = data.decode('utf-8')  # <--- get data from clients
                    print(f"Received: {reply}\n")
                    player_struct = self.test_prep_data(reply)

                    if player_struct:
                        self.update_player_data(player_struct)  # <---- update data of the player which send info

                    if reply == CLOSE:
                        self.close_connection(conn)
                        break

                    all_data = self.get_player_data(pid)
                    reply = f'{all_data}'
                    print(f"Sending {reply}\n")

                conn.sendall(reply.encode())
                print(f'self.clients = {self.clients}')
            except Exception:
                break

        print("Lost connection\n")
        self.delete_player_from_server(self.conn)
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
        self.client_id = 0
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server = server
        self.port = port

        self.address = (self.server, self.port)

        self.client_pos = {
            0: PLAYER_POS,
            1: PLAYER_POS,
            2: (2.5, 6.5)
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
        self.client_id = int(num)

    def get_client_id(self):
        return int(self.client_id)

    def send_msg(self, msg: str):
        """for service use only"""
        self.client.send(msg.encode())

    def send_data(self, data):
        """for data exchanging"""
        self.client.send(data)

    def close(self):
        self.client.close()


class PlayerDataStruct:

    def __init__(self, conn, player_id=0):
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

