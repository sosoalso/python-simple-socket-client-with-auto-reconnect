import socket
import time
import threading


class Client:
    def __init__(self, ip, port):
        self.socket = None
        self.ip = ip
        self.port = port
        self.connected = False
        self.thread_receive = threading.Thread(target=self.receive)

    def receive(self):
        while self.connected:
            try:
                message = self.socket.recv(1024).decode("UTF-8")
                self.socket.send(
                    bytes("received message from server : " + message, "UTF-8"))
                print(message)
            except (socket.error, Exception) as e:
                print("receive() >err> ", e)
                self.connect()

    def send(self, message):
        if self.connected:
            try:
                self.socket.send(bytes(message, "UTF-8"))
            except socket.error as e:
                print("send() >err> ", e)

    def connect(self):
        try:
            self.socket = socket.socket()
            self.socket.connect((self.ip, self.port))
            self.connected = True
            print("connect() >msg> Connected")
            if not self.thread_receive.is_alive():
                self.thread_receive.start()
        except socket.error as e:
            print("connect() >err> ", e)
            self.connected = False
            print("Connection lost... reconnecting")
            while not self.connected:
                try:
                    self.connect()
                except socket.error as e:
                    print(e)
                    time.sleep(3)


def run():
    while True:
        my_client.send("hah")
        time.sleep(2)


my_client = Client("localhost", 12345)
my_client.connect()
main = threading.Thread(target=run, daemon=True)
main.start()
