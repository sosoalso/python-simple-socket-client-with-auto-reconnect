import socket
import threading
import time


class Client:
    def __init__(self, ip, port, reconnect=True, name=None):
        self.socket = None
        self.ip = ip
        self.port = port
        self.connected = False
        self.reconnect = reconnect
        self.time_reconnect = 3.0
        self.thread_receive = None
        self.thread_connect = None
        self.receive_callback = None
        self.name = f"{self.ip}:{self.port}" if name is None else name

    def set_reconnect_time(self, t):
        self.time_reconnect = t

    def set_receive_callback(self, callback):
        self.receive_callback = callback

    def connect(self):
        if not self.connected:
            print(f"{self.name} -- connect()")
            self.thread_connect = threading.Thread(
                target=self._connect, name=f"Thread-Connect--{self.name}", daemon=True)
            self.thread_connect.start()

    def _connect(self):
        while not self.connected:
            try:
                self.socket = socket.create_connection((self.ip, self.port))
                self.connected = True
                print(f"{self.name} -- _connect() >connected>")
                self._run_thread_receive()
            except Exception as e:
                self.connected = False
                print(f"{self.name} -- _connect() >error> {e}")
                time.sleep(self.time_reconnect)
                if self.reconnect:
                    self.connect()
                else:
                    break

    def _run_thread_receive(self):
        self.thread_receive = threading.Thread(
            target=self._receive, name=f"Thread-Receive--{self.name}", daemon=True)
        self.thread_receive.start()

    def _receive(self):
        while self.connected:
            try:
                msg = self.socket.recv(1024).decode("UTF-8")
                print(f"{self.name} -- _receive() >len(msg)={len(msg)}>")
                if msg and self.receive_callback:
                    self.receive_callback(msg)
            except Exception as e:
                self.connected = False
                print(f"{self.name} -- _receive() >error> {e}")
                if self.reconnect:
                    self.connect()
                break

    def send(self, message):
        if self.connected and self.socket:
            try:
                self.socket.sendall(bytes(message, "UTF-8"))
            except Exception as e:
                self.connected = False
                print(f"{self.name} -- send() >error> {e}")
                if self.reconnect:
                    self.connect()

    def disconnect(self):
        if self.connected:
            try:
                self.socket.close()
            except Exception as e:
                print(f"{self.name} -- disconnect() >error> {e}")
            finally:
                self.socket = None
                self.connected = False
                print(f"{self.name} -- disconnect() >disconnected>")
