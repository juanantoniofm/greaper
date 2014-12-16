#!/usr/bin/python

"""
# GREAP

A tool to ease the burden of navigating an querying your logs
"""

import argparse
import sys
from time import sleep

from lib.parsmap import consumer
from lib.parsmap import list_fields, broadcast, get_producer, producers
#from lib.parsmap import field_map, convert_time  # by now unused. kept as reference
#from mappings import mpt  # by now unused. kept as reference
from lib.helpers import configure_logging, output, grepit
#from lib.helpers import line_matches_greps  # by now unused. kept as reference
import myfilters

command_parser = argparse.ArgumentParser(
        description="""
        Get some better detail from logs. You can specify different
        kinds of logs (check the -k param), query different fields (check -q) and
        use advanced filters (with -f).
        Example:

        greap -i <input file> -q <some fields queried> -k channel_manager

        OR

        greap -i <input file -q <query fields> -f <advance filter>

        You can edit/create your own filters in the myfilters folder, and the tool
        will pick them up automaticlly.

        Check out the README.md for more info.
        """,
        formatter_class=argparse.RawTextHelpFormatter)
        # see /System/Library/Frameworks/Python.framework/Versions/Current/lib/python2.7/argparse.py
        # this formatter takes the raw input. see the source code for more formatters.

command_parser.add_argument("-v", "--verbose", action="store_true",
        help="enable debug output", required=False, default=False)

command_parser.add_argument("-q", "--query", dest="query",
        help="select this fields from the log line.\n available:\n {0}".format(
            list_fields()),
        required=False)

command_parser.add_argument("-ff", "--follow", action="store_true",
        help="Follow, like `tail -f` or F inside less",
        required=False, default=False)

command_parser.add_argument("-f", "--filter", dest="filters",
        help="use custom built filters (available: {0})".format(
                ", ".join([f for f in dir(myfilters) if not f.startswith("__")])),
        required=False)

command_parser.add_argument("-i", "--input", dest="input_file",
        help="Filename to read input from", required=True)

command_parser.add_argument("-k", "--kind", dest="log_format",
        help="Define which kind of log to parse (available: {0})".format(
            ", ".join(producers.iterkeys())),
        required=False)

command_parser.add_argument("-g", "--grep", dest="grep_regex", default=[], action='append',
        help="Use the expresion t filter the input", required=False)

command_parser.add_argument("-ng", "--ngrep", dest="ngrep_regex",
        help="negative grep. Filter the lines that NOT match the expresion (like grep -v regex)",
        required=False)


################################################################################

#### # we dont need the follow if we put all of it in readinlines
####def follow(thefile):
####    """
####    Follow a file like tail -f.
####    """
####    thefile.seek(0,2)
####    output("reached the end of the file","DEBUG")
####    while True:
####        line = thefile.readline()
####        if not line:
####            time.sleep(0.1)
####            continue
####        else:
####            if not grepit(line, args["grep_regex"], args["ngrep_regex"]):
####                #- check that the line matches with the pre-regex and if not, break
####                yield ""
####            else:
####                #output("readinlines {0}".format(line), "DEBUG") # print debug info
####                yield line


def read_in_lines(fh=None, follow=False):
    """read a file line by line
    In a lazy way
    """
    if follow:
        #- we go to the end of the file first
        fh.seek(0,2) # it will work unless the 1st param is x>fh.tell() 
        #- and then go back a bit but never more that tell()
        backsteps = 100  # value to go back once in the EOF
        end = fh.tell()
        if backsteps < end:
            fh.seek(backsteps,2)
        else:
            #- if backsteps are higher, just go back to the beggining, as is a tiny file
            fh.seek(0,0)
        print "WTDF"
        output("reached the end of file", "INFO")

    while True:
        line = fh.readline()
        if not line:
            if follow:
                sleep(0.1)
                continue
            else:
                break
        else:
            if not grepit(line, args["grep_regex"], args["ngrep_regex"]):
                #- check that the line matches with the pre-regex and if not, break
                yield ""
            else:
                #output("readinlines {0}".format(line), "DEBUG") # print debug info
                yield line


################################################################################


##  @consumer
##  def get_stats():
##      """
##      a special consumer to get stats about a specifiq logkind.
##      DEPRECATED
##      """
##      while True:
##          r = (yield)
##          add_entry(r, stats)
##          output(stats, "DEBUG")


@consumer
def plain_print():
    """ just print the line received."""
    while True:
        r = (yield)
        print r


def compose(query, data=None):
    """
    compose the resulting line of the query ready for output.
    :query: list of params to print from the log line parsed.
    :data:  the dictionary with the parsed line.
    :return: the line to print with the fields in the order specified in query.
    """
    #TODO: change the behaviour, so compose will print the line in the same
    #      order of the original line, when no query specified
    resul_line = ""
    #- first figure out which fields to print. either all of just queried ones.
    if query is None:
        queried_fields = [x for x in data.iterkeys()]
        output("DEFQUERY {0}".format(queried_fields.__str__()), "DEBUG")
    else:
        queried_fields = query.split(",")
    #- then go and create the line
    if data is None:
        output("Nothing passed to compose", "DEBUG")
        return ""
    for f in queried_fields:
        resul_line += data[f].__str__() + " "
    return resul_line


@consumer
def query_print():
    """
    the regular consumer used with the query parameter
    """
    while True:
        r = (yield)
        output(compose(args["query"], r), "OUTPUT")


################################################################################

debug_mode = False


if __name__ == "__main__":
    args = vars(command_parser.parse_args())
    configure_logging(args["verbose"])
    try:
        #- show the params for debug purposes
        output("parameters: {0}".format(args.__str__()), "DEBUG")

        lines = read_in_lines(open(args["input_file"], "r"), args["follow"])

        producer = get_producer(args["log_format"])
        log = producer(lines)

        broadcast(log, [query_print()])

    except ValueError as e:
        output("Are you sure you have choosen the proper logformat?", "ERROR")
        output(e, "EXC")
        sys.exit(1)

    except Exception as e:
        # pokemon exception
        output(e, "EXC")
        output("We are dead", "ERROR")
        sys.exit(1)
