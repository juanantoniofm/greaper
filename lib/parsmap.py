from time import sleep
import re

from conversors import convert_time, convert_xml
from helpers import output


def follow(thefile):
    """
    Follow a file like tail -f.
    """
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line


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


### Example of usage for broadcast
##if __name__ == '__main__':
##
##    class Consumer(object):
##        def send(self,item):
##            print(self, "got", item:
##
##    c1 = Consumer()
##    c2 = Consumer()
##    c3 = Consumer()
##
##    from follow import *
##    lines = follow(open("run/foo/access-log"))
##    broadcast(lines,[c1,c2,c3])

################################################################################

def field_map(dictseq, name, func,*args):
    """ Take a sequence of dictionaries and remap one of the fields
    """
    for d in dictseq:
        d[name] = func(d[name],*args)
        yield d


mpt = { # a table to define differences among log formats
        "apache": {
            "regex":r'(\S+) (\S+) (\S+) \[(.*?)\] ' \
                       r'"(\S+) (\S+) (\S+)" (\S+) (\S+) (\S+) (\S* ?\S* ?\S*)',
                       # carefull, not compatible with other logs:
                       #r'"(\S+) (\S+) (\S+)" (\S+) (\S+) "(\S+)" "(\S* ?\S* ?\S*)"'
                       #r'"(\S+) (\S+) (\S+)" (\S+) (\S+) (\S+) (\S+)'
            "column_names":('host','referrer','user','datetime', 'method',
                            'request','proto','status','bytes','from','useragent'),
            "funcs":""},
        "channel_manager": {
            "regex": r'(\w{3} \d{2} \d{2}:\d{2}:\d{2}) ' \
                      r'(app\w{4}\d{2}) ([a-z\-]*): ' \
                      r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) ' \
                      r'(\w*) *\[(.*?)\] (.*?) - (.*)',
            "column_names": ('logdate','machine','logfile','datetime','loglevel','tracing',
                              'jobtype','action'),
            "funcs":""},
        "little_hotelier": { "regex":"",
            "column_names":"",
            "funcs":""}
        }


def list_fields():
    """make a nice list of the fields available for each kind of log"""
    help_line = ""
    for kind, v in mpt.iteritems():
        help_line += kind + ": " + mpt[kind]["column_names"].__str__() + ";"

    return help_line

#logpat   = re.compile(logpats)
logpat = re.compile(mpt["channel_manager"]["regex"])

################################################################################


def app_log(lines):
    """
    Parse an application log into a sequence of dicts
    """
    groups = (logpat.match(line) for line in lines)
    tuples = (g.groups() for g in groups if g)

    colnames = mpt["channel_manager"]["column_names"]

    log = (dict(zip(colnames,t)) for t in tuples)
    log      = field_map(log,"datetime",convert_time,"%Y-%m-%d %H:%M:%S,%f")
    log      = field_map(log,"logdate",convert_time,"%b %d %H:%M:%S")
    log      = field_map(log,"action",convert_xml)

    return log


def apache_log(lines):
    """Parse an apache log file into a sequence of dictionaries
    """
    groups = (logpat.match(line) for line in lines)
    tuples = (g.groups() for g in groups if g)
    
    colnames = mpt["apache"]["column_names"]

    log      = (dict(zip(colnames,t)) for t in tuples)
    log      = field_map(log,"status",int)
    log      = field_map(log,"bytes",
                         lambda s: int(s) if s != '-' else 0)

    return log


    
def guess_logkind(filename):
    """try to guess the kind of log from the filename"""
    raise Exception("Not f'in plemented")


def validate_logkind(log_format, supported_formats = [ k for k in mpt.iterkeys() ]):
    """validate the kind of log, or fail and exit with a list of supported formats"""
    if log_format not in supported_formats:
        raise LookupError("""I couldn't find your log kind in my list.
        see supported: {0}""".format([f for f in mpt.iterkeys()]))
    else:
        return True


def define_logkind():
    """basic logic to find out what kind of log are we parsing"""
    if args["log_format"] == False:
        #- not user-defined, so try fuzzy logic
        return validate_logkind(guess_logkind(args["input_file"]))
    else:
        # user defined, so check if is valid
        return validate_logkind(args["log_format"])
    output(logkind, "INFO",loglevel) #WAT? what the hell was i thinking with this?? TODO: delete it


def get_producer(logkind):
    producers = {
            "apache": apache_log,
            "channel_manager": app_log
            }
    lk = apache_log # by default
    try: 
        lk = producers[logkind]
    except:
        output("no producer found for: {0}".format(logkind), "DEBUG",loglevel)
    #return mpt[logkind]["producer"] #based on master dict. not working, circular dep
    return lk
