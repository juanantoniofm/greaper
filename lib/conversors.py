
import time
import xml.dom.minidom as mdom
import xml.dom.expatbuilder as expatbuilder
import re

from helpers import output

def convert_time(strtime, in_format = "%d/%b/%Y:%H:%M:%S +0000", out_format = "%H:%M"):
    """convert a string to a proper datetime timestamp
        Common timestamp formats are:
            Internet msg: "%b %d %H:%M:%S"
                "Nov 25 00:02:05",
            ISO whatever: "%d/%b/%Y:%H:%M:%S +0000"
                "17/Nov/2014:06:44:08 +0000",
            log4j style : "%Y-%m-%d %H:%M:%S,%f"
                "2014-11-25 00:02:00,180",
    """
    stamp =  time.strptime(strtime, in_format)
    return time.strftime(out_format, stamp)


def clean_action_to_xml(action):
    """
    takes the string corresponding to an "action" in a channel manager 
    log, and extracts the XML and the kind of message (request or response).
    In case of error, it should raise an exception and the caller will
    return the original action then
    """
    expresion = r"\[(.*)\] \[(.*)\]"
    reg = re.compile(expresion)
    try:
        fields = reg.match(action).groups()
    except:
        raise TypeError("This doesn't look like a request/response","DEBUG")
    return fields


def convert_xml(content=None, root = "root"):
    """
    tries to clean and convert an action in a channel manager app log
    and if it can't, just failback to plain string
    """
    if content is None or content is "" or type(content) is not type(""):
        raise TypeError("No XML input specified")

    try:
        (cleaned,root) = clean_action_to_xml(content)
        #xml = mdom.parseString('<root>'+cleaned+'</root>')
        xml = mdom.parseString('<{0}>{1}</{0}>'.format(root,cleaned))
        return xml.toprettyxml()
    except (TypeError,expatbuilder.expat.ExpatError) as e:
        output("Couldnt parse XML, {0}".format(e.__str__()), "DEBUG")
        return content

