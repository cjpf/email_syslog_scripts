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


# SETUP
    """Returns the next line in the file"""
logpath = process_args()
positionfile = '/tmp/mcpos'

# Create and init temp file if DNE
if not os.path.isfile(positionfile):
    write_position(positionfile, 0)

# Get position from temp file
position = get_position(positionfile)

# MAIN LOOP
while 1:
    # Parsing Interval
    # time.sleep(0.1)
    # Open the log
    log = open(logpath, 'r')
    # Seek to position
    log.seek(position)
    # Get new line
    line = log.readline()
    # Get new position
    position = log.tell()
    log.close()
    if not line:
        time.sleep(3)
    # If there is a line of data, parse out the JSON and decode it for storage.
    else:
        data = re.findall(r'\{.*\}', line)
        data = json.loads(data[0])
        print(json.dumps(data, indent=2))
        # Update the position in temp file
        write_position(positionfile, position)
