import unittest
from nose.tools import *

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
        assert output(self.msg,"INFO") is not None

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
        eq_ (output(self.msg),self.msg)

    def test_exceptions(self):
        """we log exceptions as trace"""
        try:
            raise Exception("faki faki faki")
        except Exception as e:
            res = output(e, "ERROR")

        eq_("",res)

################################################################################
from helpers import enabled_level

class test_output(BaseTest):
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

