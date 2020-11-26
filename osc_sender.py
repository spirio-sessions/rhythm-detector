from pythonosc.udp_client import SimpleUDPClient

class OscSender:
    
    def __init__(self, target):
        ip, port = target
        self.osc_client = SimpleUDPClient(ip, port)

    def osc_message(self, beats):
        return ('/pulse/generate', beats)

    def send(self, beats):
        path, data = self.osc_message(beats)
        self.osc_client.send_message(path, data)