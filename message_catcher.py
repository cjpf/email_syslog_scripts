#!/usr/bin/python3
# CJ Pfenninger
# January 2020
# This script will read an ESS syslog file and parse each new line of the file.  It writes the position of the log each time a message is recorded to keep it's place so that
# it does not parse entries more than once.
import sys, getopt, re, json, time, os

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


# SETUP
# Process arguments to get the logfile 
logfile = processArgs()
# Open the logfile
log = open(logfile, "r")

# Get the previously read position of the logfile or start at the top
positionfile = '/tmp/message_catcher_position'

if os.stat(positionfile).st_size == 0:
    position = 0
else:
    position = getPosition(positionfile)

# Move log file to the position
log.seek(position)

# MAIN LOOP
while 1:
    # Parsing Interval
    time.sleep(0.1)
    # Update the previous position in system file
    writePosition(positionfile, position)
    # Get new position
    position = log.tell()
    # Get new line
    line = log.readline()
    # If line is empty, return to position and wait
    if not line:
        log.seek(position)
        time.sleep(3)
    # If there is a line of data, parse out the JSON and decode it for storage.
    else: 
        data = re.findall('\{.*\}', line)
        data = json.loads(data[0])
        print(json.dumps(data, indent=2))

