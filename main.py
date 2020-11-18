import argparse
from recorder import Recorder
from server import Server
from processor import Processor

def main():
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('--target', help='the url the generated osc messages should be published to', dest='targeturl', required=True)

    server = arg_parser.add_argument_group('mode')
    server.add_argument('--server', help='run the application as web server', action='store_true')
    server.add_argument('--name', help="the server's name or ip address", default='', dest='servername')
    server.add_argument('--port', type=int, help='the port the server will listen to', default=5050)

    arg_parser.add_argument('--samplerate', type=int, help='the samplerate of the audio stream', default=44100)
    arg_parser.add_argument('--channels', type=int, help='the number of channels of the audio stream', default=2)
    arg_parser.add_argument('--chunklength', type=float, help='the chunk length in seconds', default=2.0)

    args = arg_parser.parse_args()

    processor = Processor(args.targeturl, args.channels, args.samplerate, args.chunklength)

    if args.server:
        Server(args.servername, args.port) \
            .with_handle(processor.process) \
            .run()
    else:
        Recorder(args.channels, args.samplerate, args.chunklength) \
            .with_handle(processor.process) \
            .run()

if __name__ == '__main__':
    main()