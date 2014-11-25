
def add_entry(r=None,totalstatus=None):
    """adds an entry to the results dictionary"""
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



def uno():
    pass

def dos():
    pass

def tres():
    pass
