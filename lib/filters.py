"""
I want to test how to handle filter processing from the command line
"""

from lib.helpers import output

def parse_filters(string):
    """
    it converts a string with the filter definition in a 
    dictionary with the callables or the strings to call.
    TODO: currently work in progress
    """

    try:
        expr = eval(string)
        return expr
    except (TypeError,SyntaxError) as e:
        output("please review your filter syntax","ERROR")
        output(e,"EXC")
        return None
