import socket
import threading
import time


class Client:
    def __init__(self, ip, port, reconnect=True):
        self.socket = None
        self.ip = ip
        self.port = port
        self.connected = False
        self.reconnect = reconnect

    def connect(self):
        print("connect()")
        try:
            threading.Thread(target=self._connect, name="c1").start()
        except Exception as e:
            print(f"connect() >error> {e}")

    def try_reconnect(self):
        if self.reconnect:
            print("try_reconnect()")
            self.connect()

    def _connect(self):
        print("_connect()")
        while self.connected is False:
            time.sleep(3)
            try:
                self.socket = socket.socket()
                self.socket.connect((self.ip, self.port))
                self.connected = True
                self.run_thread_receive()
            except (socket.error, Exception) as e:
                self.connected = False
                print("_connect() >err> ", e)

    def run_thread_receive(self):
        try:
            threading.Thread(target=self.receive, name="r1").start()
        except Exception as e:
            print(f"run_thread_receive() >error> {e}")

    def receive(self):
        print("receive()")
        while self.connected:
            try:
                msg = self.socket.recv(1024).decode("UTF-8")
                print(f"receive() >msg> {msg}")
            except (socket.error, Exception) as e:
                self.connected = False
                self.try_reconnect()
                print("receive() >err> ", e)

    def send(self, message):
        if self.connected:
            print("send()")
            try:
                self.socket.send(bytes(message, "UTF-8"))
            except (socket.error, Exception) as e:
                print("send() >err> ", e)
                self.connected = False

    def disconnect(self):
        print("disconnect()")
        try:
            self.socket.close()
            self.connected = False
            self.try_reconnect()
        except (socket.error, Exception) as e:
            print("disconnect() >err> ", e)
