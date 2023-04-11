import network
import socket
from time import sleep


class Connection(object):
    def __init__(self):
        self.connect()

    def connect(self):
        self.init_wlan()
        self.init_socket()

    def check(self):
        if not self.wlan.isconnected():
            self.socket.close()
            self.connect()

    def init_wlan(self):
        current = 0
        ssids = ["Bernd, 52 Jahre, 19 cm, Single",
                 "Samsung A71", "Tinis Hotter Spot"]
        passwords = ["Martini362", "apst6311", "xryu7807"]

        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)

        while True:
            print(f"Trying network configuration {current}")
            self.wlan.connect(ssids[current], passwords[current])
            current = (current + 1) % len(ssids)
            for i in range(1, 10):
                print("Waiting for connection...")
                sleep(1)
                if self.wlan.isconnected():
                    self.ip = self.wlan.ifconfig()[0]
                    print(f"Connected on {self.ip}")
                    return

    def init_socket(self):
        address = (self.ip, 80)
        self.socket = socket.socket()
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.settimeout(10)
        self.socket.bind(address)
        self.socket.listen()

    def get_request(self):
        self.client = self.socket.accept()[0]
        request = str(self.client.recv(1024))
        return request.split()[1].split("?")[0]

    def send_response(self, response):
        self.client.sendall(response)
        self.client.close()
