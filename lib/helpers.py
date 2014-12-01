
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
    #print("FFFFFFFFFFFFFFFFFFFFFFFFFFF" ,file=sys.stderr)
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
    #print ("FFFFFFXXXXXXXXXXXFFFFFFFFFF {0};; {1};; {2};;\n".format(loglevel, msg, deprecated_param))
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
