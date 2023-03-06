import socket
from game_settings import *
import _thread

# server side logic


class DedicatedServer:
    def __init__(self):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = LOCAL_SERVER_IP
        self.port = PORT

        self.clients = 0

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

    def threaded_client(self, conn):
        self.clients += 1
        conn.send(f"Connected player_id {self.clients}".encode())
        reply = ''
        while True:
            if self.clients > MAX_PLAYERS:
                print("too much players")
                break
            try:
                data = conn.recv(DATA_RECV_CHUNK)
                reply = data.decode('utf-8')

                if not data:
                    print("Disconnected")
                    self.clients -= 1
                    break
                else:
                    print(f"Received: {reply}")
                    print(f"Sending {reply}")

                conn.sendall(reply.encode())
            except Exception:
                break

        print("Lost connection\n")
        conn.close()

    def run(self):

        while True:
            conn, address = self.sock.accept()
            print('ok')
            _thread.start_new_thread(self.threaded_client, (conn,))
            print(f"connected to {address}")


class Client:

    def __init__(self, game, server=LOCAL_SERVER_IP, port=PORT):
        self.game = game
        self.client_id = 0
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server = server
        self.port = port

        self.address = (self.server, self.port)

        msg = self.connect()
        self.client_id = msg.split(' ')[-1]
        print(msg, f'from Client_id{self.client_id} .__init__')

    def connect(self):

        try:
            self.client.connect(self.address)
            return self.client.recv(DATA_RECV_CHUNK).decode()
        except:
            pass


if __name__ == '__main__':
    try:
        server_host = DedicatedServer()
        server_host.start()
        server_host.run()
    except Exception as err:
        print("error: ", err)
