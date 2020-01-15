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
import argparse
import mail_store


def process_args():
    """This function will process the arguments for the script"""
    parser = argparse.ArgumentParser(
        prog='message_catcher',
        description='Process a Barracuda ESS Syslog file')
    parser.add_argument('-l', '--log', nargs=1, required=True,
                        help='log file containing syslog data from'
                        ' Barracuda ESS')
    return parser.parse_args(sys.argv[1:])


def main():
    """."""
    args = process_args()

    mail_store.build_store()

    with open(args.log[0], 'r') as log:
        while 1:
            data = log.readline()

            if not data:
                log.close()
                sys.exit(0)
            else:
                data = re.findall(r'\{.*\}', data)
                data = json.loads(data[0])
                mail_store.store(data)


if __name__ == '__main__':
    main()
