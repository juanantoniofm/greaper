import unittest
from nose.tools import *
import mock
from filters import parse_filters


class test_parse_filters(unittest.TestCase):
    def test_none_input_is_peaceful(self):
        parse_filters(None)

    @mock.patch("filters.mm")
    def test_a_normal_dic(self):
        mm = mock.MagicMock()
        expected = {"datetime":mm}
        result = parse_filters("""{"datetime":mm}""")
        eq_(expected, result)

    @mock.patch("filters.mm")
    def test_more_than_a_value(self):
        mm = mock.MagicMock()
        result = parse_filters(""" {"datetime":mm,"action":xml_stats} """)
        expected = {"datetime":mm,"action":xml_stats}
        eq_(expected, result)

    #@raises(SyntaxError)  # It actually doesn't raise, just logs as exception
    @mock.patch("filters.output")
    def test_invalid_dic(self,outmock):
        mm = mock.MagicMock()
        result = parse_filters(""" {"datetime":mm,pieceofbadcode} """)
        print outmock
        print outmock.called
