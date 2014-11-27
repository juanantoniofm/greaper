
from __future__ import print_function
import sys
import traceback

def output(msg = None, level=None,output_level="DEBUG" ):
    """shows or not a message, depending on the level of output selected.
    level > level of the current message to send
    output_level > level of the logging detail desired"""
    if msg == None:
        return None  # nothing to do here
    if level == None:
        # regular message then
        print (msg)
        return msg
    # If there is any kind of loglevel, means app message
    loglevels = "DEBUG WARNING INFO ERROR QUIET"
    if level in loglevels[loglevels.find(output_level):]:
        if level is "ERROR":
            print("GREAP {0} {1}".format(level,msg.__str__()), file=sys.stderr)
            traceback.print_exception(*sys.exc_info())
        else:
            print("GREAP", level, msg)
        return " ".join([level,msg])

