import argparse

from . import __version__


def get_parser():
    description = f'ATCommander v{__version__} - A simple AT Command tool'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-v', '--version', action='version', version=description)
    parser.add_argument('--loglevel', default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help='Set log level, Defaults to INFO')
    parser.add_argument('-f', '--config', required=True,
                        help='A local path or URL of AT Command script file. Required!')
    parser.add_argument('-i', '--interval', default=1.0, type=float,
                        help='The time interval in seconds between commands, Defaults to 1.0')
    parser.add_argument('-s', '--serial-port',
                        help='pyserial URL (or port name) for serial port')
    parser.add_argument('-b', '--baudrate', default=115200, type=int,
                        help='Baud rate for serial port. Defaults to 115200')
    parser.add_argument('-p', '--parity', default='N', choices=['N', 'O', 'E'],
                        help='Parity for serial port. Defaults to none')
    return parser
