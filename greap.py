#!/usr/bin/python

# logcoroutine.py
#
# using co-routines to define consumers for the Apache log data
# http://www.dabeaz.com/generators/logcoroutine.py

import argparse

from lib.helpers import apache_log, field_map, consumer, read_in_lines
from myfilters import add_entry
from lib.broadcast import *
import settings


command_parser = argparse.ArgumentParser(description="get some cool stats from apache logs")
command_parser.add_argument("-v","--verbose", help="enable debug output", required=False)
args = vars(command_parser.parse_args()) 



stats = {
        "200" : { "count" : 0},
        }

@consumer
def get_stats():
    global stats
    while True:
        r = (yield)
        add_entry(r, stats)
        print("DEBUG:", stats)

@consumer
def neilfilter():
    while True:
        r=(yield)
        # Check if the uri is on the interests list
        interesting = ["/integration-opera/services",
                      "/ws/fidelio"]
        if r['status'] != 200:
            if args["verbose"]:
                print r

lines = read_in_lines(open(settings.logfile,"r"))
log   = apache_log(lines)

broadcast(log, [neilfilter()])


