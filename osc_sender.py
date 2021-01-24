from pythonosc.udp_client import SimpleUDPClient
from time import sleep

class OscSender:
    
    def __init__(self, target):
        ip, port = target
        self.osc_client = SimpleUDPClient(ip, port)
        self.message_number = 0

    def send(self, beats):
        path = '/pulse/beat'
        last_timestamp = 0.0

        print(beats)

        for timestamp, amplitude in beats:
            delay = timestamp - last_timestamp
            sleep(delay)

            self.osc_client.send_message(path, (self.message_number, amplitude))

            last_timestamp = timestamp
            self.message_number += 1