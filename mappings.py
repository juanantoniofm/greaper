
mpt = { # a table to define differences among log formats
"apache": {
    "regex":r'(\S+) (\S+) (\S+) \[(.*?)\] ' \
               r'"(\S+) (\S+) (\S+)" (\S+) (\S+) (\S+) (\S* ?\S* ?\S*)',
    "column_names":('host','referrer','user','datetime', 'method',
                    'request','proto','status','bytes','from','useragent'),
    "funcs":{"status":int,"bytes":lambda s: int(s) if s != '-' else 0},
    "params":{}
    },

"channel_manager": {
    "regex": r'(\w{3} {0,2}\d{1,2} \d{2}:\d{2}:\d{2}) ' \
              r'(app\w{4}\d{2}) ([a-z0-9\-]*): ' \
              r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) ' \
              r'(\w*) *\[(.*?)\] (.*?) - (.*)',
    "column_names": ('logdate','machine','logfile','datetime','loglevel','tracing',
                      'jobtype','action'),
    "funcs":{},
    "params":{}
    },

"cm_appserver":{
    "regex": r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) ' \
              r'(\w*) *\[(.*?)\] (.*?) - (.*)',
    "column_names": ('datetime','loglevel','tracing', 'jobtype','action'),
    "funcs":{},
    "params":{}
    },

"lh":{
    "regex": r'(\w{3} {0,2}\d{1,2} \d{2}:\d{2}:\d{2}) (app.*) (.*):' \
              r'*\[(.*?)\] *\[(.*?)\] (.*)',
    "column_names": ('logdate','machine','instance','tracing','jobtype','action'),
    "funcs":{},
    "params":{}
    },
}


