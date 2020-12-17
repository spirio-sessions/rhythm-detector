import argparse
import re
from pyaudio import PyAudio

from osc_sender import OscSender
from analyser import Analyser
from recorder import Recorder
from loader import Loader

def validate_connection_info(target_string):
    match = re.match(r'(\d+\.\d+\.\d+\.\d+):(\d+)', target_string)
    if match != None:
        ip, port = match.groups()
        return (ip, int(port))
    else:
        raise ValueError("specification of target connection malformed; expected 'IPV4:PORT' but instead got %s" % target_string)

def init_parameters(args):
    args.samplerate = 44100
    args.channels = 2
    args.chunklength = 5.0

def print_device_info():
    pa = PyAudio()
    device_count = pa.get_device_count()

    for i in range(device_count):
        print(pa.get_device_info_by_index(i))

    pa.terminate()

def main():
    arg_parser = argparse.ArgumentParser()
    sub_parsers = arg_parser.add_subparsers()

    run_parser = sub_parsers.add_parser('detect')
    run_parser.add_argument('--run', help='run bead detector', dest='run_detector', action='store_true', default=True)
    mode_group = run_parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument('--record', type=int, help='record from audio input device')
    mode_group.add_argument('--load', help='load from local file specified by absolute os filepath')
    run_parser.add_argument('--target', help='the target generated osc messages should be published to in the format IPV4:PORT, e.g. 127.0.0.1:5050', required=True)

    deviceinfo_parser = sub_parsers.add_parser('deviceinfo')
    deviceinfo_parser.add_argument('--list', help='list all devices', dest='list_devices', action='store_true', default=True)

    args = arg_parser.parse_args()
    init_parameters(args)

    if hasattr(args, 'run_detector') and args.run_detector:

        target_connection = validate_connection_info(args.target)
        osc_sender = OscSender(target_connection)
        analyser = Analyser(args.samplerate, args.chunklength)

        def handle(chunk):
                beats, _ = analyser.analyse(chunk)
                osc_sender.send(beats)

        if hasattr(args, 'record') and args.record:
            Recorder(args.channels, args.samplerate, args.chunklength) \
                .with_handle(handle) \
                .run()

        elif hasattr(args, 'load') and args.load:
            Loader(args.load, args.chunklength) \
                .with_handle(handle) \
                .run()

        else:
            print('unknown error')
            exit(1)

    elif hasattr(args, 'list_devices') and args.list_devices:
        print_device_info()

    else:
        print('unknown error')
        exit(1)

if __name__ == '__main__':
    main()