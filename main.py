import argparse
import re
from recorder import Recorder
from server import Server
from processor import Processor

def validate_connection_info(target_string):
    match = re.match(r'(\d+\.\d+\.\d+\.\d+):(\d+)', target_string)
    return match.groups() if match != None else False

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
    if not target_connection:
        raise ValueError("specification of target connection malformed; expected 'IPV4:PORT' but instead got %s" % args.target)
    
    server_connection = False
    if args.server:
        server_connection = validate_connection_info(args.server)
        if not server_connection:
            raise ValueError("specification of server connection malformed; expected 'IPV4:PORT' but instead got %s" % args.server)

    processor = Processor(target_connection, args.channels, args.samplerate, args.chunklength)

    if server_connection:
        Server(server_connection) \
            .with_handle(processor.process) \
            .run()
    else:
        Recorder(args.channels, args.samplerate, args.chunklength) \
            .with_handle(processor.process) \
            .run()

if __name__ == '__main__':
    main()