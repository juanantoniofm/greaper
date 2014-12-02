from time import sleep
import re

from conversors import convert_time, convert_xml
from helpers import output


# disabled to avoid wrong coverage
##def follow(thefile):
##    """
##    Follow a file like tail -f.
##    """
##    thefile.seek(0,2)
##    while True:
##        line = thefile.readline()
##        if not line:
##            time.sleep(0.1)
##            continue
##        yield line


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


mpt = { # a table to define differences among log formats
        "apache": {
            "regex":r'(\S+) (\S+) (\S+) \[(.*?)\] ' \
                       r'"(\S+) (\S+) (\S+)" (\S+) (\S+) (\S+) (\S* ?\S* ?\S*)',
            "column_names":('host','referrer','user','datetime', 'method',
                            'request','proto','status','bytes','from','useragent'),
            "funcs":{"status":int,"bytes":lambda s: int(s) if s != '-' else 0},
            "params":{}},
        "channel_manager": {
            "regex": r'(\w{3} {0,2}\d{1,2} \d{2}:\d{2}:\d{2}) ' \
                      r'(app\w{4}\d{2}) ([a-z0-9\-]*): ' \
                      r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) ' \
                      r'(\w*) *\[(.*?)\] (.*?) - (.*)',
            "column_names": ('logdate','machine','logfile','datetime','loglevel','tracing',
                              'jobtype','action'),
            "funcs":""},
        "cm_appserver":{
            "regex": r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) ' \
                      r'(\w*) *\[(.*?)\] (.*?) - (.*)',
            "column_names": ('datetime','loglevel','tracing', 'jobtype','action'),
            "funcs":""}
        }


def list_fields(mpt = mpt):
    """make a nice list of the fields available for each kind of log"""
    help_line = ""
    for kind, v in mpt.iteritems():
        help_line += kind + ": " + mpt[kind]["column_names"].__str__() + ";"
    return help_line

################################################################################

def matchit(regob, line, validation_fields = None):
    """
    match and validate the matching of a line against a regex object
    :regob: regex pattern compiled
    :line:  just a line
    """
    matched =  regob.match(line)
    if validation_fields is not None:
        try:
            if len(matched.groups()) is not len(validation_fields):
                raise ValueError("number of regex matches not valid")
        except:
            output("regob: {0}".format(type(regob)), "DEBUG")
            output("pattern: {0}".format(regob.pattern), "DEBUG")
            output("line: {0}".format(line), "DEBUG")
            output("validation: {0}".format(len(validation_fields)), "DEBUG")
            output("matches: {0}".format(type(matched)), "DEBUG")
            raise ValueError("regex not matching properly")

    return matched


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
        raise ValueError("No lines provided")

    ####print "lines",repr(lines)
    ####print "regex",regex
    ####print "columns",colnames
    ####print "converts",converters
    ####print "params", parameters

    logpat = re.compile(regex)

    ### groups = (logpat.match(line) for line in lines if line != "")
    ### mygroups = [x for x in groups]
    ### if len(mygroups) < len(colnames):
    ###     raise ValueError("regex not matching well")

    groups = (matchit(logpat, line,colnames) for line in lines if line != "")
    mygroups = [x for x in groups]
    ####print "My Groups: ", mygroups  #DEBUGGING
    tuples = (g.groups() for g in mygroups if g)

    log = (dict(zip(colnames,t)) for t in tuples)
    try:
        for colname in converters:
            # try to convert each field
            try:
                # we have to pass the params as a pointer to the list
                # and check if there are params 
                if colname in parameters.keys():
                    log = field_map(log,colname,converters[colname],*parameters[colname])
                else:
                    log = field_map(log,colname,converters[colname])

            except TypeError:
                output("unparsed field {0}".format(colname),"DEBUG")
            #output([x for x in log],"DEBUG")
    except (TypeError) as e:
        #TODO: define what to do in case of massive failure
        #output("failure parsing lines {0}".format(lines),"DEBUG") # verborreic output
        output("failure parsing lines","DEBUG") # verborreic output
        output(e,"EXC")
        raise sys.exc_info[1], None, exc_info[2]
    return log

def apache_log(lines,mpt=mpt):
    """
    wrapper to call generic log with the proper params
    """
    kind = "apache"
    return generic_log( lines,
                        mpt[kind]["regex"],
                        mpt[kind]["column_names"],
                        mpt[kind]["funcs"],
                        mpt[kind]["params"]
                      )


def channel_manager_log(lines):
    return new_channel_manager_log(lines) # TODO: please delete this method

def new_channel_manager_log(lines):
    """
    wrapper to call app log with params accordingly.
    The idea behing this is being able to remove it in the near future
    """
    kind = "channel_manager"
    app_func = {"datetime":convert_time,
                    "logdate":convert_time,
                    "action":convert_xml
                    }
    # params have to be lists, so it can be properly referenced inside
    app_params = {"datetime":["%Y-%m-%d %H:%M:%S,%f"],
                    "logdate":["%b %d %H:%M:%S"],
                    "action":[]
                    }
    processed =  generic_log( lines,
                        mpt[kind]["regex"],
                        mpt[kind]["column_names"],
# this are the final lists we should be calling. this is just a test. TODO: finish it
#                          mpt[kind]["funcs"],
#                          mpt[kind]["params"]
                        app_func, app_params
                      )
    ####print ("PROCESSED: ", len([x for x in processed]))
    return processed


def old_channel_manager_log(lines):
    """
    Parse an application log into a sequence of dicts
    """
    logpat = re.compile(mpt["channel_manager"]["regex"])
    groups = (logpat.match(line) for line in lines)
    tuples = (g.groups() for g in groups if g)

    colnames = mpt["channel_manager"]["column_names"]

    try:
        log = (dict(zip(colnames,t)) for t in tuples)
        log      = field_map(log,"datetime",convert_time,"%Y-%m-%d %H:%M:%S,%f")
        log      = field_map(log,"logdate",convert_time,"%b %d %H:%M:%S")
        log      = field_map(log,"action",convert_xml)
    except TypeError as e:
        output("Are you sure you have chosen the application logformat?","INFO")
        raise sys.exc_info[1], None, exc_info[2]

    return log


def old_apache_log(lines):
    """
    Parse an apache log file into a sequence of dictionaries.
    Old fashioned method to be deprecated
    """
    logpat = re.compile(mpt["apache"]["regex"])
    groups = (logpat.match(line) for line in lines)
    tuples = (g.groups() for g in groups if g)
    
    colnames = mpt["apache"]["column_names"]

    try:
        log      = (dict(zip(colnames,t)) for t in tuples)
        log      = field_map(log,"status",int)
        log      = field_map(log,"bytes",
                             lambda s: int(s) if s != '-' else 0)
    except TypeError:
        print ("""barrrr""")
        output("Are you sure you have chosen the apache logformat?","INFO")
        raise sys.exc_info[1], None, exc_info[2]

    return log


producers = {
        "apache": apache_log,
        "channel_manager": channel_manager_log,
        "new_channel_manager": new_channel_manager_log
        }

def get_producer(logkind):
    """
    returns a callable to the proper log producer
    """
    try: 
        lk = producers[logkind]
    except:  # then we fallback to default
        output("no producer found for: {0}".format(logkind), "DEBUG")
        output("falling back to default log kind: {0}".format(channel_manager_log), "WARNING")
        lk = channel_manager_log # by default

    return lk
