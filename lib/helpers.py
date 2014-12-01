
""" Module to host some helper function, mainly related to logging and printing"""


from __future__ import print_function
import sys
import logging

# configure logging
logging.basicConfig(
        stream=sys.stderr,
        level=logging.INFO,
        format="GREAP %(levelname)s %(message)s")
#TODO:configure it from settings and command line


def normal_output(msg=None):
    """
    prints normal output of the program, that is, the results of the query 
    performed, results, etc. 
    Not the information related to the inner workings of the application
    """
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
            "INFO": logging.info,
            "OUTPUT":normal_output
            }
    try:
        levels[loglevel](msg)
    except:
        logging.error("Log level not found: {0}".format(loglevel))
        logging.error("logging: ",msg)
