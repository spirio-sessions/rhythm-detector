from pythonosc.udp_client import SimpleUDPClient
from time import sleep

class OscSender:
    
    def __init__(self, target):
        ip, port = target
        self.osc_client = SimpleUDPClient(ip, port)

    def send(self, beats):
        path = '/pulse/beat'
        data = None
        last_timestamp = 0.0

        print(beats)

        for timestamp, _ in beats:
            delay = timestamp - last_timestamp
            sleep(delay)
            self.osc_client.send_message(path, data)
            last_timestamp = timestamp