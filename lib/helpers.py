
from __future__ import print_function
import sys
import traceback

def enabled_level(output_level):
    loglevels = "DEBUG WARNING INFO ERROR QUIET"
    return loglevels[loglevels.find(output_level):]



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
    if level in enabled_level(output_level):
        output_msg = "GREAP [{0}] {1}"
        if type( msg) is not type(""):
            output_msg = output_msg.format(level,msg.__str__())
            if "DEBUG" in enabled_level(output_level):
                print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW") 
                traceback.print_exception(*sys.exc_info())
        else:
            output_msg = output_msg.format(level,msg.__str__())
        print(output_msg, file=sys.stderr)
        return output_msg

