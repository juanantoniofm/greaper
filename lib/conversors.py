
import time
import xml.dom.minidom as mdom
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
    expresion = r"\[(.*)\] \[(.*)\]"
    reg = re.compile(expresion)
    return reg.match(action).groups()


def convert_xml(content=None):
    """
    tries to clean and convert an action in a channel manager app log
    and if it can't, just failback to plain string
    """
    assert content is not None

    if content == "":
        return ""

    try:
        cleaned = clean_action_to_xml(content)[1]
        #xml = xml.dom.minidom.parseString(cleaned)
        xml = mdom.parseString('<root>'+cleaned+'</root>')
        return xml.toprettyxml()
    except Exception as e:
        output("Couldnt parse XML, {0}".format(e.__str__()), "DEBUG")
        return content

