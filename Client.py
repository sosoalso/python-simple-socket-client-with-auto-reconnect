import socket
import time
import threading


class Client():
    def __init__(self, ip, port):
        self.socket = None
        self.ip = ip
        self.port = port
        self.connected = False
        self.thread_receive = threading.Thread(target=self.receive)

    def kill_thread_receive(self):
        print("kill?")

    def alive_thread_receive(self):
        if not self.thread_receive.is_alive():
            self.thread_receive.start()

    def receive(self):
        print("receive")
        while self.connected:
            try:
                message = self.socket.recv(1024).decode("UTF-8")
                self.socket.send(bytes("Client wave : " + message, "UTF-8"))
                print(message)

            except socket.error as e:
                print(e)
                self.connect()
                # time.sleep(2)

            except Exception as e:
                print(e)
                self.connect()
                # time.sleep(2)

    def send(self, message):
        try:
            self.socket.send(bytes(message), "UTF-8")
        except socket.error as e:
            print(e)
            # self.kill_thread_receive()

    def connect(self):
        try:
            self.socket = socket.socket()
            self.socket.connect((self.ip, self.port))
            self.connected = True
            print("connected")
            self.alive_thread_receive()
        except socket.error as e:
            print(e)
            self.connected = False
            # self.kill_thread_receive()
            print("connection lost... reconnecting")
            while not self.connected:
                try:
                    self.connect()
                except socket.error as e:
                    print(e)
                    # self.kill_thread_receive()
                    time.sleep(3)


def run():
    while True:
        print('run')
        time.sleep(2)


my_client = Client("localhost", 12345)
my_client.connect()

main = threading.Thread(target=run, daemon=True)
main.start()
