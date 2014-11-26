
################################################################################
#   My Filters.
#   Though as a library of possible filters to be used weth the greap tools.
################################################################################
def add_entry(r=None,totalstatus=None):
    """
    adds an entry to the results dictionary. 
    Initially focused at apache logs
    """
    # TODO: this is not being GC properly, causing a memory leak.... sloppy...
    assert r is not None
    assert totalstatus is not None
    print "R:", r
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

        # add the user agent
        try:
            totalstatus[str(r['status'])]["useragents"][r['useragent']] += 1
        except KeyError:
            # if it's not being found till now, create a new entry in stats
            totalstatus[str(r['status'])]["useragents"] = {}
            totalstatus[str(r['status'])]["useragents"][r['useragent']] = 1

    except KeyError as e:
        print("ERROR:", "some value appears to not have being registered in stats", e)



################################################################################
#  Splitted methods to use with add entry
################################################################################

def get_total_count(r=None, totalstatus=None):
    """
    get the total count of hits that returned an error code
    """
    assert r is not None
    assert totalstatus is not None
    try:
        totalstatus[str(r['status'])]['count'] += 1
    except KeyError:

        totalstatus[str(r['status'])] = {}
        totalstatus[str(r['status'])]['count'] = 1
    return totalstatus


def get_uri(r=None, totalstatus=None):
    """add the request that caused the code"""
    assert r is not None
    assert totalstatus is not None
    try:
        totalstatus[str(r['status'])]["URI"][r['request']] += 1
    except KeyError:
        # if it's not being found till now, create a new entry in stats
        try:
            if totalstatus[str(r['status'])]["URI"]:
                totalstatus[str(r['status'])]["URI"][r['request']] = 1
        except:
            totalstatus[str(r['status'])]["URI"] = {}
            totalstatus[str(r['status'])]["URI"][r['request']] = 1
    return totalstatus


def get_ip(r=None, totalstatus=None):
    """ add the IP count"""
    assert r is not None
    assert totalstatus is not None
    try:
        totalstatus[str(r['status'])][r['host']] += 1
    except KeyError:
        totalstatus[str(r['status'])][r['host']] = 1


def get_useragent(r=None, totalstatus=None):
    """ add the user agent"""
    assert r is not None
    assert totalstatus is not None
    try:
        totalstatus[str(r['status'])]["useragents"][r['useragent']] += 1
    except KeyError:
        # if it's not being found till now, create a new entry in stats
        totalstatus[str(r['status'])]["useragents"] = {}
        totalstatus[str(r['status'])]["useragents"][r['useragent']] = 1
         


