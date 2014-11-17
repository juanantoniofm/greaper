# logcoroutine.py
#
# using co-routines to define consumers for the Apache log data
# http://www.dabeaz.com/generators/logcoroutine.py

from apachelogparser import *
from helpers import apache_log, field_map, consumer
from broadcast import *

stats = {
        "200" : { "count" : 0},
        }

def add_entry(r=None,totalstatus=None):
    """adds an entry to the results dictionary"""
    assert r is not None
    assert totalstatus is not None
    try:
        totalstatus[str(r['status'])]['count'] += 1
        # add the request that caused the code
        try:
            totalstatus[str(r['status'])][r['request']] += 1
        except KeyError:
            totalstatus[str(r['status'])][r['request']] = 1
        # add the IP count
        try:
            totalstatus[str(r['status'])][r['host']] += 1
        except KeyError:
            totalstatus[str(r['status'])][r['host']] = 1

    except KeyError as e:
        totalstatus[str(r['status'])] = { "count":1}
        totalstatus[str(r['status'])][r['request']] = 1



@consumer
def find_404():
    global stats
    while True:
        r = (yield)
        add_entry(r, stats)
        #print  stats


## 
## @consumer
## def bytes_transferred():
##     total = 0
##     while True:
##         r = (yield)
##         total += r['bytes']
##         print "Total bytes", total
##
##
##broadcast(log, [find_404(),bytes_transferred()]) # using more than one consumer


logfile = "access-vpn.fidelio.log"
lines = open(logfile,"r").readlines()
log   = apache_log(lines)

broadcast(log, [find_404()])
print stats
