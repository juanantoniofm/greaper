
import re

def field_map(dictseq, name, func):
    """ Take a sequence of dictionaries and remap one of the fields
    """
    for d in dictseq:
        d[name] = func(d[name])
        yield d


logpats  = r'(\S+) (\S+) (\S+) \[(.*?)\] ' \
           r'"(\S+) (\S+) (\S+)" (\S+) (\S+) (\S+) (\S* ?\S* ?\S*)'
           #r'"(\S+) (\S+) (\S+)" (\S+) (\S+) "(\S+)" "(\S* ?\S* ?\S*)"' # carefull, not compatible with other logs
           #r'"(\S+) (\S+) (\S+)" (\S+) (\S+) (\S+) (\S+)'

logpat   = re.compile(logpats)

def apache_log(lines):
    """Parse an apache log file into a sequence of dictionaries
    """
    groups = (logpat.match(line) for line in lines)
    tuples = (g.groups() for g in groups if g)
    
    colnames = ('host','referrer','user','datetime',
            'method', 'request','proto','status','bytes','from','useragent')

    log      = (dict(zip(colnames,t)) for t in tuples)
    log      = field_map(log,"status",int)
    log      = field_map(log,"bytes",
                         lambda s: int(s) if s != '-' else 0)

    return log


def consumer(func):
    """consumer decorator and co-routine """
    def start(*args,**kwargs):
        c = func(*args,**kwargs)
        c.next()
        return c
    return start


def output(msg = None, level=None,output_level="DEBUG" ):
    """shows or not a message, depending on the level of output selected.
    level > level of the current message to send
    output_level > level of the logging detail desired"""
    if msg == None:
        return None  # nothing to do here
    if level == None:
        # regular message then
        print msg
        return msg
    # If there is any kind of loglevel, means app message
    loglevels = "DEBUG WARNING INFO QUIET"
    if level in loglevels[loglevels.find(output_level):]:
        print level, msg
        return " ".join([level,msg])
    
import time

def filter_time(strtime, out_format = "%H:%M", in_format = "%d/%b/%Y:%H:%M:%S +0000"):
    """convert a string to a proper datetime timestamp"""
    stamp =  time.strptime(strtime, in_format)
    return time.strftime(out_format, stamp)


