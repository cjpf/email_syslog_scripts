#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script will read an ESS syslog file and parse each new line of the file.

CJ Pfenninger
January 2020

It writes the position of the log each time a message is recorded to keep it's
place so that it does not parse entries more than once.
"""
import sys
import re
import json
import time
import os
import argparse
import message_store


def process_args():
    """This function will process the arguments for the script"""
    parser = argparse.ArgumentParser(
        prog='message_catcher',
        description='Process a Barracuda ESS Syslog file')
    parser.add_argument('-l', '--log', nargs=1, required=True,
                        help='log file containing syslog data from'
                        ' Barracuda ESS')
    return parser.parse_args(sys.argv[1:])


def write_position(posfile, pos):
    """Writes the position of the log file"""
    with open(posfile, 'w') as file:
        file.write(str(pos))
        file.close()


def get_position(posfile):
    """Reads the previous position of the log file"""
    with open(posfile, 'r') as file:
        value = int(file.read())
        file.close()
        return value


def get_line(datafile, position):
    """Returns the next line in the file"""
    with open(datafile, 'r') as file:
        file.seek(position)
        line = file.readline()
        position = file.tell()
        file.close()
    return line, position


def main():
    """."""
    args = process_args()
    positionfile = '/tmp/mcpos'
    if not os.path.isfile(positionfile):
        write_position(positionfile, 0)

    position_proc = get_position(positionfile)

    while 1:
        data, position_proc = get_line(args.log[0], position_proc)
        if not data:
            time.sleep(3)
            print('Displaying ALL DB DATA...')
            i = 1
            for row in message_store.read_all():
                print(i, ': ', row)
                i += 1
        else:
            data = re.findall(r'\{.*\}', data)
            data = json.loads(data[0])
            # message_store.print_data(data)
            message_store.store(data)
            write_position(positionfile, position_proc)


if __name__ == '__main__':
    main()
