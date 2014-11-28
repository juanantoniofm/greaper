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

    def test_debug_on_info(self):
        """ we dont print debug msgs on info level"""
        assert output(self.msg, "DEBUG","INFO") is None

    def test_info_on_debug(self):
        """ we print info mesg on debug lev"""
        assert output(self.msg,"INFO","DEBUG") is not None

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
            eq_(type(""),res)
            eq_(True,mymock.called)
            

    def test_none_input(self):
        """none input returns none"""
        eq_(None, output())

################################################################################
from helpers import enabled_level

class test_enabled_level(BaseTest):
    def test_debug(self):
        eq_("DEBUG WARNING INFO ERROR QUIET", enabled_level("DEBUG"))

    def test_warning(self):
        eq_("WARNING INFO ERROR QUIET", enabled_level("WARNING"))

    def test_info(self):
        eq_("INFO ERROR QUIET", enabled_level("INFO"))

    def test_error(self):
        eq_("ERROR QUIET", enabled_level("ERROR"))

    def test_quiet(self):
        eq_("QUIET", enabled_level("QUIET"))

    @raises(ValueError)
    def test_none_input(self):
        eq_(None, enabled_level(None))
