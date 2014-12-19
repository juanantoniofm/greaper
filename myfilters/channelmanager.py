
################################################################################
#   My Filters.
#   Though as a library of possible filters to be used weth the greap tools.
################################################################################
    

################################################################################
import xml.dom.minidom as mdom
import xml.dom.expatbuilder as expatbuilder

from helpers import output

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


def trim_token(content=None,trim=40):
    """
    trim the trace token however we want. Example:
    integration-juniper-DES-inventoryJob-1: traceToken=vk4Ox7ctD5QA timestamp=1417695841922,hotelier=9070,membership=79734
    so, to trim the beggining, is column 41; trimming until the = is column52
    """
    return content[trim:]


def trim_token_inventoryjobs(content=None,template = "\thotel {hotelier} member {membership}"):
    """
    trim the trace token however we want. Example:
    integration-juniper-DES-inventoryJob-1: traceToken=vk4Ox7ctD5QA timestamp=1417695841922,hotelier=9070,membership=79734
    so, to trim the beggining, is column 41; trimming until the = is column52
    """
    pattern = ".*traceToken=(\S+) timestamp=(\d+),hotelier=(\d+),membership=(\d+)"
    reg =re.compile(pattern)
    groups = reg.match(content).groups()
    output("regex result: {0}".format([ x for x in groups]),"DEBUG")

    return template.format(hotelier=groups[2],membership=groups[3],token=groups[0],timestamp=groups[1])
