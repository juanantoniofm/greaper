import unittest
from nose.tools import *

################################################################################
from greap import grepit
import imp
imp.load_source("greap", "./greap")

class test_grepit(unittest.TestCase):
    def test_matches_an_expresion(self):
        """simple matching"""
        eq_("foobar", grepit("foobar","ob"))

    def test_only_pos_that_not_match(self):
        """if the positive expresion dont match and no neg, dont show"""
        eq_("", grepit("naranja", "ob"))

    def test_only_neg_that_match(self):
        """simple negative matching"""
        eq_("", grepit("foobar", "",nregex="ob"))

    def test_matches_both_exist_and_match(self):
        """ if matches both dont show """
        eq_("",grepit("foobar","oo","fo"))

    def test_nothing_to_grep_about(self):
        """ nothing to greap about """
        eq_("foobar",grepit("foobar","",""))

    def test_both_exist_pos_match_neg_no_match(self):
        """ both exist pos match neg no match """
        eq_("foobar",grepit("foobar","foo","nomatch"))

    @nottest
    def test_(self):
        """ t """
        eq_("",grepit("",))

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
