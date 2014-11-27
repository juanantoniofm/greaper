#!/usr/bin/python


import argparse
import sys

from lib.parsmap import apache_log, field_map, consumer, convert_time, app_log
from lib.parsmap import mpt,list_fields,  broadcast, get_producer
from lib.helpers import output 
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
            ", ".join(mpt.iterkeys())),
        required=False)

command_parser.add_argument("-g","--grep", dest="grep_regex",
        help="Use the expresion t filter the input", required=False)

command_parser.add_argument("-ng","--ngrep", dest="ngrep_regex",
        help="negative grep. Filter the lines that NOT match the expresion (like grep -v regex)", required=False)




################################################################################

stats = {
        "200" : { "count" : 0},
        }


def define_loglevel():
    """sets a level of detail for the log."""
    global loglevel
    if args["verbose"]:
        loglevel = "DEBUG"

def grepit(line, regex="", nregex = ""):
    """
    only returns a line if it matches the rexex, and doesn't match the ngrep regex
    :line: line of the log to process
    :regex: expresion to validate the line
    :nregex: expresion to discard the line
    """
    if ((nregex is not "" ) and  (nregex in line)): 
        # if it matches neg regex, return nothing
        return ""
    else:
        # if not, check if matches positive
        if ((regex is not "" ) and (regex in line)) :
            # and if does, return the line
            return line
        else:
            return ""
    #if regex is None:
    #    return line
    #else:
    #    if (regex in line) == args["ngrep"]:
    #        return line


def read_in_lines(fh = None):
    """read a file line by line
    In a lazy way
    """
    while True:
        line = fh.readline()
        if not line:
            break
        else:
            if not grepit(line, args["grep_regex"], args["ngrep_regex"]):
                # check that the line matches with the pre-regex and if not, break
                yield ""
            else:
                output(line, "DEBUG:",loglevel) # print debug info
                yield line
 
################################################################################

@consumer
def get_stats():
    global stats
    while True:
        r = (yield)
        add_entry(r, stats)
        output(stats, "DEBUG:", loglevel)


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
    rl = " "
    #- first figure out which fields to print. either all of just queried ones.
    if query is None:
        queried_fields = [x for x in data.iterkeys()]
        output(queried_fields.__str__(),"DEBUG",loglevel)
    else:
        queried_fields = query.split(",")
    #- then go and create the line
    for f in queried_fields:
        rl += data[f].__str__() + " "
    return rl




@consumer
def query_print():
    while True:
        r=(yield)
        output(compose(args["query"], r))


################################################################################

if __name__ == "__main__":
    args = vars(command_parser.parse_args()) 
    loglevel = "ERROR"  # the default value is DEBUG untill further development
    import lib.helpers as helpers
    import lib.parsmap as parsmap
    helpers.loglevel = loglevel
    parsmap.loglevel = loglevel
    print "log level" + loglevel

    try:
        output(args.__str__(),"DEBUG",loglevel) # show the params for debug purposes
        define_loglevel()
        lines = read_in_lines(open(args["input_file"],"r"))

        log = get_producer(args["log_format"])(lines)

        broadcast(log, [query_print()])

    except ValueError as e:
        output("Are you sure you have choosen the proper logformat?", "ERROR")
        output(e,"ERROR")
        sys.exit(1)

    except Exception as e:
        output(e, "ERROR")
        sys.exit(1)

