import unittest
from nose.tools import *



################################################################################
import mock
from greap import compose

class test_compose(unittest.TestCase):
    def setUp(self):
        self.d = {"a":11,"b":"c"}

    @mock.patch('greap.output')
    def test_mock_returns(self,mock):
        mock.return_value="fooreturn"
        compose("a,b",{"a":11,"b":"c"})
        eq_(False,mock.called)

    @nottest  # missing loglevel TODO
    @mock.patch('greap.output')
    def test_empty_query_str_calls_output(self,mock):
        mock.return_value="fooreturn"
        compose("",self.d)
        eq_(True,mock.called)

    @nottest  # Dont enable this until we change logging
    @mock.patch('greap.output')
    def test_none_query_calls_output(self,mock):
        mock.return_value="fooreturn"
        compose(None,{"a":11,"b":"c"})
        print dir(mock)
        eq_(True,mock.called)

    def test_returns_a_field(self):
        res = compose("a,b",self.d)
        eq_(" 11 c ", res)
