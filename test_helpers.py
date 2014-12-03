import unittest
from nose.tools import *
import mock

class BaseTest(unittest.TestCase):
    def setUp(self):
        pass


################################################################################
from helpers import  output

### class test_output(BaseTest):
###     def setUp(self):
###         self.msg = "a message"
### 
###     def test_debug_output(self):
###         """a debug message goes printed in debug level"""
###         assert output(self.msg) is not None
### 
###     @raises(TypeError)
###     def test_void_msg(self):
###         """nothing breaks in null message"""
###         assert output(None) is None
###         assert output() is None
### 
###     def test_common_case(self):
###         """this would be the most common case in code"""
###         loglevel_from_command_line = "WARNING"
###         assert output(self.msg, "INFO", loglevel_from_command_line)
### 
###     def test_normal_goes_normal(self):
###         """if no params, means normal msg"""
###         eq_(self.msg, output(self.msg,"OUTPUT"))
###  
###     def test_no_level_goes_normal(self):
###         """if no params, means normal msg"""
###         eq_(self.msg, output(self.msg))
###  
###     @mock.patch("helpers.enabled_level")
###     def test_exceptions(self,mymock):
###         """we log exceptions as trace"""
###         mymock.side_effect = Exception("kabooom!")
###         res = output("msg", "ERROR")
###         eq_(type(""),res)
###         eq_(True,mymock.called)
###             
### 
###     def test_exceptions(self):
###         """we log exceptions as trace"""
###         try:
###             raise Exception("faki faki faki")
###         except Exception as e:
###             #TODO: write a proper test to verify exception logging
###             res = output(e, "ERROR")
###             eq_(type(""),type(res))
###             eq_("GREAP ERROR faki faki faki",res)
###             eq_(True,mymock.called)
###             
### 
###     def test_none_input(self):
###         """none input returns none"""
###         eq_(None, output())

################################################################################
from helpers import  line_no_matches_ngreps


class test_line_no_matches_ngreps(BaseTest):
    def setUp(self):
        self.line = "foobarbaz"

    @raises(AssertionError)
    def test_no_greplist_raises(self):
        """if we dont pass greplist, raise"""
        line_no_matches_ngreps(self.line)

    def test_empty_greplist_returns_line(self):
        """for a empty list of ngreaps, return the line"""
        # as it might mean we are not actually searching
        eq_(self.line,line_no_matches_ngreps(self.line,[]))


    def test_single_match_returns_none(self):
        """
        for a simple ngrep expr, match it and return none
        """
        eq_(None,line_no_matches_ngreps(self.line,["foo"]))

    def test_single_not_match_returns_line(self):
        """for a single expr that not match, return line"""
        eq_(self.line,line_no_matches_ngreps(self.line,["nomatch"]))


    def test_multi_match_return_expr(self):
        """for a multiple expr that match, return none"""
        eq_(None,line_no_matches_ngreps(self.line,["foo","bar"]))


    def test_multi_no_match_return_expr(self):
        """for a multiple expr where 1 does't and 1 does match, return nothing"""
        eq_(None,line_no_matches_ngreps(self.line,["foo","idontmatch"]))


################################################################################
from helpers import  line_matches_greps


class test_line_matches_greps(BaseTest):
    def setUp(self):
        self.line = "foobarbaz"

    @raises(AssertionError)
    def test_no_greplist_raises(self):
        """if we dont pass greplist, raise"""
        line_matches_greps(self.line)


    def test_empty_greplist_returns_line(self):
        """for a empty list of greaps, return the line"""
        # as it might mean we are not actually searching
        eq_(self.line,line_matches_greps(self.line,[]))


    def test_single_match_returns_line(self):
        """
        for a simple grep expr, match it and return
        """
        eq_(self.line,line_matches_greps(self.line,["foo"]))

    def test_single_not_match_returns_none(self):
        """for a single expr that not match, return nothing"""
        eq_(None,line_matches_greps(self.line,["nomatch"]))


    def test_multi_match_return_expr(self):
        """for a multiple expr that match, return line"""
        eq_(self.line,line_matches_greps(self.line,["foo","bar"]))


    def test_multi_no_match_return_expr(self):
        """for a multiple expr where 1 dont match, return nothing"""
        eq_(None,line_matches_greps(self.line,["foo","idontmatch"]))


################################################################################
from greap import grepit
import imp
imp.load_source("greap", "./greap")

class test_grepit(unittest.TestCase):
    def test_matches_an_expresion(self):
        """simple matching"""
        eq_("foobar", grepit("foobar",["ob"]))

    def test_only_pos_that_not_match(self):
        """if the positive expresion dont match and no neg, dont show"""
        eq_(None, grepit("naranja", ["ob"]))

    def test_only_neg_that_match(self):
        """simple negative matching"""
        eq_(None,grepit("foobar",[ ""],nregex=["ob"]))

    def test_matches_both_exist_and_match(self):
        """ if matches both dont show """
        eq_(None,grepit("foobar",["oo"],["fo"]))

    def test_nothing_to_grep_about(self):
        """ nothing to greap about """
        eq_("foobar",grepit("foobar",[],[]))

    def test_both_exist_pos_match_neg_no_match(self):
        """ both exist pos match neg no match """
        eq_("foobar",grepit("foobar",["foo"],["nomatch"]))

    @raises(TypeError)
    def test_typeerror_in_case_of_string(self):
        """ if we make a mistake a pass a string for expresion, fail """
        eq_(None,grepit("","",""))


    @nottest
    def test_(self):
        """ t """
        eq_(None,grepit("",))

