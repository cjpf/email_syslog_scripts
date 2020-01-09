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
import getopt
import re
import json
import time
import os


def process_args():
    """This function will process the arguments for the script"""
    if len(sys.argv) == 1:
        usage(2)
    path = ''
    try:
        opts, _ = getopt.getopt(sys.argv[1:], 'hl:')
    except getopt.GetoptError:
        usage(2)
    for opt, arg in opts:
        if opt in ("-h"):
            usage(0)
        elif opt in ("-l"):
            path = arg
        else:
            usage(0)
    return path


def usage(code):
    """Prints instructions for how to call this script"""
    if type(code) != type(1):
        code = 2
    print('Invalid arguments.')
    print('usage: message_catcher.py -l <logpath>')
    sys.exit(code)


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
    logpath = process_args()
    positionfile = '/tmp/mcpos'

    if not os.path.isfile(positionfile):
        write_position(positionfile, 0)

    position_proc = get_position(positionfile)

    while 1:
        data, position_proc = get_line(logpath, position_proc)
        if not data:
            time.sleep(3)
        else:
            data = re.findall(r'\{.*\}', data)
            data = json.loads(data[0])
            print(json.dumps(data, indent=2))
            write_position(positionfile, position_proc)


if __name__ == '__main__':
    main()
