#!/usr/bin/env python3

import argparse
import re
from configparser import ConfigParser

from pyaudio import PyAudio

from osc_sender import OscSender
from analyser import Analyser, get_analyser_config
from recorder import Recorder
from loader import Loader

def get_cmd_args():
    arg_parser = argparse.ArgumentParser()
    sub_parsers = arg_parser.add_subparsers()

    run_parser = sub_parsers.add_parser('detect')
    run_parser.add_argument('--run', help='run rhythm detector', dest='run_detector', action='store_true', default=True)
    mode_group = run_parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument('--record', type=int, help='record from audio input device', dest='device_number')
    mode_group.add_argument('--load', help='load from local file specified by absolute os filepath')
    run_parser.add_argument('--profile', help='name of analyser profile in analyser config', dest='analyser_profile', default=None)
    run_parser.add_argument('--target', help='the target generated osc messages should be published to in the format IPV4:PORT, e.g. 127.0.0.1:5050', required=True)

    deviceinfo_parser = sub_parsers.add_parser('deviceinfo')
    deviceinfo_parser.add_argument('--list', help='list all devices', dest='list_devices', action='store_true', default=True)

    return arg_parser.parse_args()

def validate_connection_info(target_string):
    match = re.match(r'(\d+\.\d+\.\d+\.\d+):(\d+)', target_string)
    if match != None:
        ip, port = match.groups()
        return (ip, int(port))
    else:
        raise ValueError("specification of target connection malformed; expected 'IPV4:PORT' but instead got %s" % target_string)

def make_handle(analyser, osc_sender):
    def handle(chunk):
        beats = analyser.analyse(chunk)
        osc_sender.send(beats)
    return handle

def run_recorder(device_number, analyser_config, osc_sender):
    recorder = Recorder(device_number, analyser_config['chunk_length'])
    sample_rate = recorder.get_sample_rate()
    analyser = Analyser(sample_rate=sample_rate, analyser_config=analyser_config)
    handle = make_handle(analyser, osc_sender)
    recorder.with_handle(handle).run()

def run_loader(load_path, analyser_config, osc_sender):
    loader = Loader(load_path, analyser_config['chunk_length'])
    sample_rate = loader.get_sample_rate()
    analyser = Analyser(sample_rate=sample_rate, analyser_config=analyser_config)
    handle = make_handle(analyser, osc_sender)
    loader.with_handle(handle).run()

def list_devices():
    pa = PyAudio()
    device_count = pa.get_device_count()
    for i in range(device_count):
        print()
        print(pa.get_device_info_by_index(i))
    print()
    pa.terminate()

def main():
    args = get_cmd_args()

    if hasattr(args, 'run_detector') and args.run_detector:

        analyser_config = get_analyser_config('analyser_config.ini', args.analyser_profile)
        target_connection = validate_connection_info(args.target)
        osc_sender = OscSender(target_connection)

        if hasattr(args, 'device_number') and args.device_number != None:
            run_recorder(args.device_number, analyser_config, osc_sender)

        elif hasattr(args, 'load') and args.load:
            run_loader(args.load, analyser_config, osc_sender)

        else:
            print('unknown error')
            exit(1)

    elif hasattr(args, 'list_devices') and args.list_devices:
        list_devices()

    else:
        print('unknown error')
        exit(1)

if __name__ == '__main__':
    main()