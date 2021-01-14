#!/usr/bin/env python3

import argparse
import re
from configparser import ConfigParser

from pyaudio import PyAudio

from osc_sender import OscSender
from analyser import Analyser
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

def get_analyser_config(config_path='analyser_config.ini', profile=None):
        cfg = ConfigParser(allow_no_value=True)
        cfg.read(config_path)

        if len(cfg.sections()) > 0:
            if profile == None:
                section = cfg[cfg.sections()[0]]
            elif cfg.sections().__contains__(profile): 
                section = cfg[profile]
            else:
                raise ValueError('analyser configuration could not be retrieved: no config profile named "%s"' % profile)
        else:
            raise ValueError('analyser configuration could not be retrieved: no configuration found in config file "%s"' % config_path)
        
        config = {
            'chunk_length': section.getfloat('ChunkLength'),
            'window_length': section.getfloat('WindowLength'),
            'hop_length': section.getfloat('HopLength'),
            'dominant_window_length': section.getfloat('DominantWindowLength'),
            'dominant_hop_length': section.getfloat('DominantHopLength'),
            'dominant_scale': section.getfloat('DominantScale')
        }

        return config

def make_handle(analyser, osc_sender):
    return lambda chunk: osc_sender.send(analyser.analyse(chunk))  

def main():
    args = get_cmd_args()

    if hasattr(args, 'run_detector') and args.run_detector:

        target_connection = validate_connection_info(args.target)
        osc_sender = OscSender(target_connection)
        analyser_config = get_analyser_config('analyser_config.ini', args.analyser_profile)

        if hasattr(args, 'device_number') and args.device_number != None:
            recorder = Recorder(args.device_number, analyser_config['chunk_length'])
            sample_rate = recorder.get_sample_rate()
            analyser = Analyser(sample_rate=sample_rate)            
            handle = make_handle(analyser, osc_sender)
            recorder.with_handle(handle).run()

        elif hasattr(args, 'load') and args.load:
            loader = Loader(args.load, analyser_config['chunk_length'])
            sample_rate = loader.get_sample_rate()
            analyser = Analyser(sample_rate=sample_rate)
            handle = make_handle(analyser, osc_sender)
            loader.with_handle(handle).run()

        else:
            print('unknown error')
            exit(1)

    elif hasattr(args, 'list_devices') and args.list_devices:
        pa = PyAudio()
        device_count = pa.get_device_count()

        for i in range(device_count):
            print(pa.get_device_info_by_index(i))

        pa.terminate()

    else:
        print('unknown error')
        exit(1)

if __name__ == '__main__':
    main()