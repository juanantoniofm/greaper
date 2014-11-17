# logcoroutine.py
#
# using co-routines to define consumers for the Apache log data
# http://www.dabeaz.com/generators/logcoroutine.py

from jinja2 import Template

from helpers import apache_log, field_map, consumer
from broadcast import *
import settings

stats = {
        "200" : { "count" : 0},
        }

def add_entry(r=None,totalstatus=None):
    """adds an entry to the results dictionary"""
    # TODO: this is not being GC properly, causing a memory leak.... sloppy...
    assert r is not None
    assert totalstatus is not None
    try:
        #if r["status"] == 405:
            #print r

        try:
            totalstatus[str(r['status'])]['count'] += 1
        except KeyError:
            totalstatus[str(r['status'])] = {}
            totalstatus[str(r['status'])]['count'] = 1


        # add the request that caused the code
        try:
            totalstatus[str(r['status'])]["URI"][r['request']] += 1
        except KeyError:
            # if it's not being found till now, create a new entry in stats
            totalstatus[str(r['status'])]["URI"] = {}
            totalstatus[str(r['status'])]["URI"][r['request']] = 1

##        # add the IP count
##        try:
##            totalstatus[str(r['status'])][r['host']] += 1
##        except KeyError:
##            totalstatus[str(r['status'])][r['host']] = 1

        # add the user agent
        try:
            totalstatus[str(r['status'])]["useragents"][r['useragent']] += 1
        except KeyError:
            # if it's not being found till now, create a new entry in stats
            totalstatus[str(r['status'])]["useragents"] = {}
            totalstatus[str(r['status'])]["useragents"][r['useragent']] = 1
            

    except KeyError as e:
        print("ERROR:", "some value appears to not have being registered in stats", e)



@consumer
def find_404():
    global stats
    while True:
        r = (yield)
        add_entry(r, stats)


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


lines = open(settings.logfile,"r").readlines()
log   = apache_log(lines)

broadcast(log, [find_404()])


def compose_email(data=None):
    """returns the HTML body of an email, with the data in the provided dic"""
    assert data is not None
    template_file = settings.template_file
    with open(template_file) as tf:
        t = Template(tf.read())
        return t.render(data)


#print compose_email(stats)
import pprint
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(stats)


