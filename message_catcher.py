#!/usr/bin/python3
# CJ Pfenninger
# January 2020
# This script will read an ESS syslog file and parse each new line of the file.  It writes the position of the log each time a message is recorded to keep it's place so that
# it does not parse entries more than once.
import sys, getopt, re, json, time

# Process Arguments
def processArgs():
    if(len(sys.argv) == 1):
        usage(2)
    logfile = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hl:')
    except getopt.GetoptError:
        usage(2)
    for opt, arg in opts:
        if opt in ("-h"):
            usage(0)
        elif opt in ("-l"):
            logfile = arg
        else:
            usage(0)
    return logfile

# Prints a usage helper and exits
def usage(code):
    if type(code) != type(1):
        code = 2
    print('message_catcher.py -l <logfile>')
    sys.exit(code)

# Writes the position of the log file 
def writePosition(posfile, pos):
    with open(posfile, 'w') as file:
        file.write(str(pos))

# Reads the previous position of the log file
def getPosition(posfile):
    with open(posfile, 'r') as file:
        return int(file.read())


# MAIN
log = open(processArgs(), "r")


data = log.readlines()

# this is junk
while 1:
    time.sleep(5)
    pointer = log.tell()
    line = log.readline()
    if not line:
        log.seek(pointer)
    else:
        data = re.findall('\{.*\}', line)
        data = json.loads(data[0])
        print(data)

