from time import sleep
import re

from conversors import convert_time, convert_xml
from helpers import output,matchit
from mappings import mpt


def consumer(func):
    """consumer decorator and co-routine """
    def start(*args,**kwargs):
        c = func(*args,**kwargs)
        c.next()
        return c
    return start


def broadcast(source, consumers):
    """
    Broadcast a generator source to a collection of consumers
    see
    http://www.dabeaz.com/generators/broadcast.py
    """
    for item in source:
        for c in consumers:
            c.send(item)

################################################################################

def field_map(dictseq, name, func,*args):
    """ Take a sequence of dictionaries and remap one of the fields
    """
    for d in dictseq:
        d[name] = func(d[name],*args)
        ####print "       field mapping      elem:{0}; name:{1}".format(d,name) #DEBUGGING
        yield d


def list_fields(mpt = mpt):
    """make a nice list of the fields available for each kind of log"""
    help_line = ""
    for kind, v in mpt.iteritems():
        help_line += kind + ": " + mpt[kind]["column_names"].__str__() + ";\n"
    return help_line

################################################################################

def generic_log(lines=None,regex = None, colnames = None, converters = None, parameters = None):
    """
    generic function to parse log lines, based on a dic of field:conversor
    :lines: 
    :regex: regular expression that will match each field
    :colnames: names in order for the fields
    :converters: functions that will process the different fields
    :parameters: extra data to pass to the converter functions
    """
    assert regex is not None
    assert colnames is not None
    if lines == []:
        raise ValueError("No lines provided") #TODO:COVER

    ##### DEBUGGING
    ####print "lines",repr(lines)
    ####print "regex",regex
    ####print "columns",colnames
    ####print "converts",converters
    ####print "params", parameters

    logpat = re.compile(regex)

    #####Debugging lines
    ####groups = (matchit(logpat, line,colnames) for line in lines if line != "")
    ####mygroups = [x for x in groups]
    ####tuples = (g.groups() for g in mygroups if g)

    #- using generator funcs
    groups = (matchit(logpat,line,colnames) for line in lines if line.strip() != "")
    tuples = (g.groups() for g in groups if g)

    log = (dict(zip(colnames,t)) for t in tuples)
    try:
        for colname in converters:
            #- try to convert each field
            try:
                #- we have to pass the params as a pointer to the list
                #- and check if there are params 
                if colname in parameters.keys():
                    log = field_map(log,colname,converters[colname],*parameters[colname]) #TODO:COVER
                else:
                    log = field_map(log,colname,converters[colname])

            except TypeError:  #TODO:COVER
                output("unparsed field {0}".format(colname),"DEBUG")
    except (TypeError) as e: #TODO:COVER
        #TODO: define what to do in case of massive failure
        output("failure parsing lines","DEBUG") # verborreic output
        output(e,"EXC")
        raise sys.exc_info[1], None, exc_info[2]
    return log


def agnostic_log(lines, kind=None):
    """
    takes the logkind and returns the generic log properly configured
    """
    if kind is None:
        raise TypeError("The kind of log {0} is not being recognised".format(kind))

    return generic_log(lines,
                        mpt[kind]["regex"],
                        mpt[kind]["column_names"],
                        mpt[kind]["funcs"],
                        mpt[kind]["params"]
                      )

def custom_log(lines, kind=None):
    """
    demo function to handle custom logs
    """
    if kind is None:
        raise TypeError("The kind of log {0} is not being recognised".format(kind))

    return generic_log(lines,
                        mpt[kind]["regex"],
                        mpt[kind]["column_names"],
                        mpt[kind]["funcs"],
                        mpt[kind]["params"]
                      )


producers = {
        "undocumented": custom_log,
        }

def get_producer(logkind):
    """
    returns a callable to the proper log producer
    """
    try: 
        if logkind in producers.iterkeys():
            lk = producers[logkind]
        else:
            output("Trying with agnostic provider","DEBUG")
            lk = agnostic_log
            output("found agnostic provider for {0} ".format(logkind),"DEBUG")


    except Exception as e:  # then we fallback to default
        output("no producer found for: {0}".format(logkind), "DEBUG")
        output("while looking for producer: {0}".format(e))
        output("falling back to default log kind: {0}".format(channel_manager_log), "WARNING")
        lk = channel_manager_log # by default

    return lk
