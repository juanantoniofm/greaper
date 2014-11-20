
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


