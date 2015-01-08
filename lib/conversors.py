
import datetime
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
    if strtime == "" or strtime == None or in_format == "" or out_format == "":
        raise TypeError("no proper input given to convert time. time: {0};in_fmt: {1}; out_fmt:{2}".format(
                        strtime,in_format,out_format))
    stamp =  datetime.datetime.strptime(strtime, in_format)
    return stamp.strftime(out_format)


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
        return beautify_xml(cleaned,root)
    except (TypeError,expatbuilder.expat.ExpatError) as e:
        #output("Couldnt parse XML, {0}".format(e.__str__()), "DEBUG") #DEBUGGING too verbose
        return content

def beautify_xml(content, root="root"):
    """beautify some xml mate!"""
    #TODO: work in progress
    #xml = mdom.parseString('<root>'+cleaned+'</root>')
    xml = mdom.parseString('<{0}>{1}</{0}>'.format(root,content))
    return xml.toprettyxml()


def xml_stats(content=None, root="root"):
    """
    extract stats from an xml request/response
    """
    if content is None or content is "" or type(content) is not type(""):
        raise TypeError("No XML input specified")
    #result_template = "{kind}; size={size} chars;"
    result_template = ";{kind}; {size};"  #csv ready
    try:
        #- detect if we are talking about request, response, or other shit
        if "REQUEST" in content[1:10]:
            pattern = r"\[(RE\S+)\] \[(.*)\]"
        elif "RESPONSE" in content[1:10]:
            pattern = r"\[(RE\S+) in (\d+) ms\] \[(.*)\]"
        else:
            raise TypeError("this is not request nor response")
        reg = re.compile(pattern)
        #- try to match the thing against a request or response regex
        fields=reg.match(content).groups()
        if fields[0] == "REQUEST":
            return result_template.format(kind=fields[0],size=len(fields[1]))
        else:
            #output(beautify_xml(fields[2],"response"), "OUTPUT") #TODO: this is just a temp check
            #return result_template.format(                      # normal mode
            #            kind=fields[0],size=len(fields[2]))
            #            + " rtt:{0};".format(fields[1])
            return result_template.format(                         #CSV ready
                        kind=fields[0],size=len(fields[2])) + " {0}".format(fields[1])
    except (TypeError,expatbuilder.expat.ExpatError) as e:
        output("couldn't get stats from XML,  {0}".format(e.__str__()), "DEBUG") #DEBUGGING too verbose
        return content
    return content


def trim_token(content=None, trim=40):
    """
    trim the trace token however we want. Example:
    integration-juniper-DES-inventoryJob-1: traceToken=vk4Ox7ctD5QA stamp=1417695841922,hotelier=9070,membership=79734
    so, to trim the beggining, is column 41; trimming until the = is column52
    """
    return content[trim:]


def trim_token_inventoryjobs(content=None, template = "\thotel {hotelier};\tmember {membership};"):
    """
    trim the trace token however we want. Example:
    integration-juniper-DES-inventoryJob-1: traceToken=vk4Ox7ctD5QA stamp=1417695841922,hotelier=9070,membership=79734
    integration-ctrip-inventoryJob-3: traceToken=IZ0Ei8qZzGIN timestamp=1420686240458,hotelier=5603,membership=85056
    so, to trim the beggining, is column 41; trimming until the = is column52
    """
    try:
        pattern = ".*traceToken=(\S+).*stamp=(\d+),hotelier=(\d+),membership=(\d+).*"
        reg =re.compile(pattern)
        groups = reg.match(content).groups()
        output("regex result: {0}".format([ x for x in groups]), "DEBUG")
        result = template.format(hotelier=groups[2], membership=groups[3], token=groups[0], timestamp=groups[1])
    except AttributeError as e:
        output("regex did not match on trim token: {0}".format(e), "DEBUG")
        result = content
    return result
