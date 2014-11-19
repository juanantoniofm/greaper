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
command_parser.add_argument("-v","--verbose", action="store_true", help="enable debug output", required=False)
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

import time

def filter_time(strtime, out_format = "%H:%M", in_format = "%d/%b/%Y:%H:%M:%S +0000"):
    """convert a string to a proper datetime timestamp"""
    stamp =  time.strptime(strtime, in_format)
    return time.strftime(out_format, stamp)


@consumer
def neilfilter():
    while True:
        r=(yield)
        # Check if the uri is on the interests list
        interesting = ["/integration-opera/services",
                      "/ws/fidelio"]
        if r['request'] in interesting:
            if args["verbose"]:
                #print r["host"], r["request"]
                print filter_time(r['datetime']),r["host"] , r["request"]

lines = read_in_lines(open(settings.logfile,"r"))
log   = apache_log(lines)

broadcast(log, [neilfilter()])



