import unittest
from nose.tools import *
import mock

class BaseTest(unittest.TestCase):
    def setUp(self):
        pass


################################################################################
from helpers import  output

class test_output(BaseTest):
    def setUp(self):
        self.msg = "a message"

    def test_debug_output(self):
        """a debug message goes printed in debug level"""
        assert output(self.msg) is not None

    @raises(TypeEror)
    def test_void_msg(self):
        """nothing breaks in null message"""
        assert output(None) is None
        assert output() is None

    def test_common_case(self):
        """this would be the most common case in code"""
        loglevel_from_command_line = "WARNING"
        assert output(self.msg, "INFO", loglevel_from_command_line)

    def test_normal_goes_normal(self):
        """if no params, means normal msg"""
        eq_(self.msg, output(self.msg,"OUTPUT"))
 
    def test_no_level_goes_normal(self):
        """if no params, means normal msg"""
        eq_(self.msg, output(self.msg))
 
    @mock.patch("helpers.enabled_level")
    def test_exceptions(self,mymock):
        """we log exceptions as trace"""
        mymock.side_effect = Exception("kabooom!")
        res = output("msg", "ERROR")
        eq_(type(""),res)
        eq_(True,mymock.called)
            

    def test_exceptions(self):
        """we log exceptions as trace"""
        try:
            raise Exception("faki faki faki")
        except Exception as e:
            #TODO: write a proper test to verify exception logging
            res = output(e, "ERROR")
            eq_(type(""),type(res))
            eq_("GREAP ERROR faki faki faki",res)
            eq_(True,mymock.called)
            

    def test_none_input(self):
        """none input returns none"""
        eq_(None, output())

