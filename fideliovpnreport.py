# logcoroutine.py
#
# using co-routines to define consumers for the Apache log data
# http://www.dabeaz.com/generators/logcoroutine.py

from jinja2 import Template

from helpers import apache_log, field_map, consumer
from broadcast import *
from getstats import get_total_count, get_uri, get_useragent
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
        get_total_count(r,totalstatus)  # get the total count of hits with this code
        get_uri(r,totalstatus)  # add the request that caused the code
        get_useragent(r,totalstatus)  # add the user agent to the stats
    except KeyError as e:
        print("ERROR:", "some value appears to not have being registered in stats", e)
    return totalstatus



@consumer
def find_404():
    global stats
    while True:
        r = (yield)
        add_entry(r, stats)


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
