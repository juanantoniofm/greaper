
""" Module to host some helper function, mainly related to logging and printing"""


from __future__ import print_function
import sys
import logging

# configure logging
logging.basicConfig(
        stream=sys.stderr,
        level=logging.DEBUG,
        format="GREAP %(levelname)s %(message)s")
#TODO:configure it from settings and command line


def normal_output(msg=None):
    """
    prints normal output of the program, that is, the results of the query 
    performed, results, etc. 
    Not the information related to the inner workings of the application
    """
    #raise TypeError("when called")
    if msg == None:
        print("")
        return ""
    print(msg)
    return(msg)


def output(msg, loglevel="OUTPUT", deprecated_param = None):
    """
    New output function. 
    It uses the logging module to control everything
    :msg: the actuall message to print 
    :loglevel: the loglevel to which the msg belongs
    :deprecated_param: just that. a deprecated param that will be removed soon from the callers
    """
    # to imitate a switch/case behaviour, we use a hashmap:
    levels = {
            "DEBUG":logging.debug,
            "WARNING": logging.warning,
            "ERROR": logging.error,
            "INFO": logging.debug,
            "EXC": logging.exception,
            "OUTPUT":normal_output
            #"OUTPUT":logging.info
            }
    levels[loglevel](msg)
    return "GREAP {0} {1}".format(loglevel,msg)
    try:
        pass
    except KeyError:
        logging.error("Log level not found: {0}".format(loglevel))
        logging.error("logging: ",msg)

################################################################################

def line_matches_greps(line, greplist=None):
    """
    check if the line matches the strings we are looking for in the greps
    :line: just the line
    :greplist: list of grep parameters
    """
    assert greplist is not None
    # if the list is empty is because we are not actually searching nothing
    print(line)
    if greplist ==  [] or line is None:
        return line

    nomatch = False
    for grep in greplist:
        if grep not in line:
            nomatch = True

    if nomatch:
        return None
    else:
        return line


def line_no_matches_ngreps(line, ngreplist=None):
    """
    check if the line doesn't match the strings in the neg greps
    :line:  the line to match
    :ngreplist: a list with the expresions to discard
    """
    assert ngreplist is not None
    # if the list is empty is because we are not actually searching anything
    if ngreplist == [] or line is None:
        return line

    match = False
    for grep in ngreplist:
        if grep in line:
            match = True

    if match:
        return None
    else:
        return line

def grepit(line, regex=[], nregex = []):
    """
    only returns a line if it matches the rexex, and doesn't match the ngrep regex
    :line: line of the log to process
    :regex: expresion to validate the line
    :nregex: expresion to discard the line
    """
    #TODO: it can be simplified with the new line_matches_greps method
    if regex is None:
        regex = []
    if nregex is None:
        nregex  = []

    if type(nregex) is not type([]) or type(regex) is not type([]):
        raise TypeError("You have not passed a list to grepit")

    return line_matches_greps(
            line_no_matches_ngreps(
                line,
                nregex),
            regex)


