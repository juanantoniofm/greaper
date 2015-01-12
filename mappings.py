from lib.conversors import convert_time,convert_xml,clean_action_to_xml
from lib.conversors import xml_stats,trim_token,trim_token_inventoryjobs, xml_error_text
#from myfilters.hbd import categorize_errors, get_hotel_and_room_name
import  myfilters 


apache= {
    "regex":r'(\S+) (\S+) (\S+) \[(.*?)\] ' \
               r'"(\S+) (\S+) (\S+)" (\S+) (\S+) (\S+) (\S* ?\S* ?\S*)',
    "column_names":('host','referrer','user','datetime', 'method',
                    'request','proto','status','bytes','from','useragent'),
    "funcs":{"status":int,"bytes":lambda s: int(s) if s != '-' else 0},
    "params":{}
    }

channel_manager= {
    "regex": r'(\w{3} {0,2}\d{1,2} \d{2}:\d{2}:\d{2}) ' \
              r'(app\w{4}\d{2}) ([a-z0-9\-]*): ' \
              r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) ' \
              r'(\w*) *\[(.*?)\] (.*?) - (.*)',
    "column_names": ('logdate','machine','logfile','datetime','loglevel','tracing',
                      'jobtype','action'),
    "funcs":{"datetime":convert_time, "logdate":convert_time, "action":convert_xml },
    "params": {"datetime":["%Y-%m-%d %H:%M:%S,%f"], "logdate":["%b %d %H:%M:%S"], "action":[] }
    }

cm_appserver={
    "regex": r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) ' \
              r'(\w*) *\[(.*?)\] (.*?) - (.*)',
    "column_names": ('datetime','loglevel','tracing', 'jobtype','action'),
    "funcs":{"action":xml_stats,"datetime":convert_time,"tracing":trim_token_inventoryjobs},
    "params":{"datetime":["%Y-%m-%d %H:%M:%S,%f","%H:%M:%S"],"tracing":["{timestamp}"]}
    }

lh={
    "regex": r'(\w{3} {0,2}\d{1,2} \d{2}:\d{2}:\d{2}) (app.*) (.*):' \
              r'*\[(.*?)\] *\[(.*?)\] (.*)',
    "column_names": ('logdate','machine','instance','tracing','jobtype','action'),
    "funcs":{},
    "params":{}
    }

temporary={
    "regex": channel_manager["regex"],
    "column_names": channel_manager["column_names"],
    "funcs":{"datetime":convert_time,"tracing":trim_token_inventoryjobs, "action":xml_error_text},
    "params":{"datetime":["%Y-%m-%d %H:%M:%S,%f","%H:%M"],"tracing":["{membership};{hotelier}"] }
    }




mpt = { # a table to define differences among log formats
"apache": apache ,
"channel_manager": channel_manager,
"temporary":temporary,
"cm_appserver": cm_appserver,
"lh": lh,
}


