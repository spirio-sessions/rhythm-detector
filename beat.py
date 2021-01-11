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
    run_parser.add_argument('--run', help='run beat detector', dest='run_detector', action='store_true', default=True)
    mode_group = run_parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument('--record', type=int, help='record from audio input device', dest='device_number')
    mode_group.add_argument('--load', help='load from local file specified by absolute os filepath')
    run_parser.add_argument('--profile', help='name of analyser profile in analyser config', dest='analyser_profile', default=None)
    run_parser.add_argument('--target', help='the target generated osc messages should be published to in the format IPV4:PORT, e.g. 127.0.0.1:5050', required=True)

    deviceinfo_parser = sub_parsers.add_parser('deviceinfo')
    deviceinfo_parser.add_argument('--list', help='list all devices', dest='list_devices', action='store_true', default=True)

    args = arg_parser.parse_args()

    if hasattr(args, 'run_detector') and args.run_detector:

        target_connection = validate_connection_info(args.target)
        osc_sender = OscSender(target_connection)
        analyser = Analyser().with_config('analyser_config.ini', args.analyser_profile)

        def handle(chunk):
            beats = analyser.analyse(chunk)
            osc_sender.send(beats)

        if hasattr(args, 'device_number') and args.device_number != None:
            Recorder(args.device_number, 2, analyser.sample_rate, analyser.chunk_length) \
                .with_handle(handle) \
                .run()

        elif hasattr(args, 'load') and args.load:
            Loader(args.load, args.chunk_length) \
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