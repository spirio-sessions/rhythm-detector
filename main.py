import argparse
import re

from osc_sender import OscSender
from analyser import Analyser
from recorder import Recorder
from server import Server

# make a ticking sound on the host machine

# def tick(t):
#     sleep(t)
#     print('\a')

# def ticks(ts):
#     ts = concatenate(([0.0], ts))
#     def do_ticks():
#         for i in range(len(ts) - 1):
#             tick(ts[i+1] - ts[i])
#     return do_ticks

def validate_connection_info(target_string):
    match = re.match(r'(\d+\.\d+\.\d+\.\d+):(\d+)', target_string)
    if match != None:
        ip, port = match.groups()
        return (ip, int(port))
    else:
        raise ValueError("specification of target connection malformed; expected 'IPV4:PORT' but instead got %s" % target_string)

def main():
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('--target', help='the target generated osc messages should be published to in the format IPV4:PORT, e.g. 127.0.0.1:5050', required=True)

    server = arg_parser.add_argument_group('mode')
    server.add_argument('--server', help='run the application as web server at IPV4:PORT, e.g. 127.0.0.1:5000', default=False)

    arg_parser.add_argument('--samplerate', type=int, help='the samplerate of the audio stream', default=44100)
    arg_parser.add_argument('--channels', type=int, help='the number of channels of the audio stream', default=2)
    arg_parser.add_argument('--chunklength', type=float, help='the chunk length in seconds', default=2.0)

    args = arg_parser.parse_args()
    
    target_connection = validate_connection_info(args.target)
    # osc_sender = OscSender(target_connection)
    analyser = Analyser(args.samplerate, args.chunklength)
    
    server_connection = False
    if args.server:
        server_connection = validate_connection_info(args.server)

    def handle(chunk):
            beats = analyser.analyse(chunk)
            print(beats)
            # osc_sender.send(beats)

    if server_connection:
        Server(server_connection) \
            .with_handle(handle) \
            .run()
    else:
        Recorder(args.channels, args.samplerate, args.chunklength) \
            .with_handle(handle) \
            .run()

if __name__ == '__main__':
    main()