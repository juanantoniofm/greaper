#!/usr/bin/python


import argparse
import sys

from lib.parsmap import field_map, consumer, convert_time
from lib.parsmap import mpt,list_fields, broadcast, get_producer, producers
from mappings import mpt
from lib.helpers import configure_logging, output, line_matches_greps, grepit
import myfilters 

command_parser = argparse.ArgumentParser(
        description="get some cool stats from apache logs",
        formatter_class=argparse.RawTextHelpFormatter)
        # see /System/Library/Frameworks/Python.framework/Versions/Current/lib/python2.7/argparse.py
        # this formatter takes the raw input. see the source code for more formatters.

command_parser.add_argument("-v","--verbose", action="store_true",
        help="enable debug output", required=False, default=False)

command_parser.add_argument("-q","--query", dest="query",
        help="select this fields from the log line.\n available:\n {0}".format(list_fields()),
        required=False)

command_parser.add_argument("-f","--filter", dest="filters",
        help="use custom built filters (available: {0})".format(
                ", ".join([ f for f in dir(myfilters) if not f.startswith("__") ])),
        required=False)

command_parser.add_argument("-i","--input", dest="input_file",
        help="Filename to read input from", required=True)

command_parser.add_argument("-k","--kind", dest="log_format",
        help="Define which kind of log to parse (available: {0})".format(
            ", ".join(producers.iterkeys())),
        required=False)

command_parser.add_argument("-g","--grep", dest="grep_regex", default=[],action='append',
        help="Use the expresion t filter the input", required=False)

command_parser.add_argument("-ng","--ngrep", dest="ngrep_regex", default=[], action='append',
        help="negative grep. Filter the lines that NOT match the expresion (like grep -v regex)", required=False)




################################################################################

def read_in_lines(fh = None):
    """read a file line by line
    In a lazy way
    """
    try:
        while True:
            line = fh.readline()
            if not line:
                break
            else:
                if not grepit(line, args["grep_regex"], args["ngrep_regex"]):
                    #- check that the line matches with the pre-regex and if not, break
                    yield ""
                else:
                    #output("readinlines {0}".format(line), "DEBUG") # print debug info
                    yield line
    except IOError as e:
        output("No more output needed. {0}".format(e),"DEBUG")
 
################################################################################

@consumer
def get_stats():
    global stats
    while True:
        r = (yield)
        add_entry(r, stats)
        output(stats, "DEBUG")


@consumer
def plain_print():
    while True:
        r=(yield)
        print r

def compose(query, data=None):
    """compose the resulting line of the query ready for output.
    :query: list of params to print from the log line parsed.
    :data:  the dictionary with the parsed line.
    :return: the line to print with the fields in the order specified in query."""
    #TODO: change the behaviour, so compose will print the line in the same order of
    #      the original line, when no query specified
    rl = ""
    #- first figure out which fields to print. either all of just queried ones.
    if query is None:
        queried_fields = [x for x in data.iterkeys()]
        output("DEFQUERY {0}".format(queried_fields.__str__()), "DEBUG")
    else:
        queried_fields = query.split(",")
    #- then go and create the line
    if data is None:
        output("Nothing passed to compose","DEBUG")
        return ""
    for f in queried_fields:
        rl += data[f].__str__() + " "
    return rl




@consumer
def query_print():
    try:
        while True:
            r=(yield)
            output(compose(args["query"], r),"OUTPUT")
    except IOError as e:
        output("No more output needed. {0}".format(e),"DEBUG")


################################################################################

debug_mode = False

if __name__ == "__main__":
    args = vars(command_parser.parse_args()) 
    configure_logging(args["verbose"])
    try:
        output("parameters: {0}".format(args.__str__()),"DEBUG") # show the params for debug purposes

        lines = read_in_lines(open(args["input_file"],"r"))

        producer =  get_producer(args["log_format"])
        log = producer(lines)

        broadcast(log, [query_print()])

    except ValueError as e:
        output("Are you sure you have choosen the proper logformat?", "ERROR")
        output(e,"EXC")
        sys.exit(1)

    except Exception as e:
        output(e, "EXC")
        output("We are dead", "ERROR")
        sys.exit(1)
