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

################################################################################
from helpers import convert_time
from datetime import datetime

class test_convert_time(BaseTest):
    def setUp(self):
        self.valid_inputs = [
                "17/Nov/2014:06:44:08 +0000",
                "2014-11-25 00:02:00,180",
                "Nov 25 00:02:05"
                ]
        self.invalid_inputs = [
                "OMG is 00:00:00",
                "023-12-89 88:88:88,777",
                "oh no, this is not a time"
                ]

    @nottest
    def test_empty_time(self):
        convert_time("")

    def test_syslog_format(self):
        result =  convert_time(self.valid_inputs[0])
        eq_("06:44", result)

    def test_java_format(self):
        result = convert_time(self.valid_inputs[1],"%Y-%m-%d %H:%M:%S,%f")
        eq_("00:02", result)

    def test_inetmsg_format(self):
        result = convert_time(self.valid_inputs[2],"%b %d %H:%M:%S")
        eq_("00:02", result)

    def test_weird_input(self):
        for inp in self.invalid_inputs:
            assert_raises(ValueError,convert_time,inp)


################################################################################
from helpers import  validate_logkind

class test_validate_logkind(BaseTest):
    def setUp(self):
        self.logkinds = ["apache", "whatever"]

    @raises(LookupError)
    def test_empty_list(self):
        """If we pass empty logkind list, break"""
        validate_logkind("apache", [])

    @raises( LookupError )
    def test_empty_logkind(self):
        """If we pass empty logkind, wat?"""
        validate_logkind("",[])

    @raises( LookupError )
    def test_none_logkind(self):
        validate_logkind(None,[])

    def test_normal_logking(self):
        """all works normal"""
        eq_(True, validate_logkind("apache",self.logkinds))

    @raises( LookupError )
    def test_not_in_list(self):
        """If the logkind is not in the list, break"""
        eq_(True, validate_logkind("apache",["foo"]))


################################################################################
from helpers import app_log

class test_app_log(BaseTest):
    def setUp(self):
        pass

    def test_empty_lines(self):
        input_line = []
        assert_raises(ValueError,app_log, input_line)   

    def test_wrong_line(self):
        input_line = "bau asetao euas uabsoeutaneusan uasoe tu asoeuta "
        assert_raises(ValueError,app_log, input_line)   
        assert type(app_log(input_line)) is type(dict())

    def test_wtf(self):
        input_line = "wtf"
        eq_([],[ f for f in  app_log(input_line)])

################################################################################
from helpers import apache_log

class test_apache_log(BaseTest):
    def setUp(self):
        pass

    def test_empty_lines(self):
        input_line = []
        assert_raises(ValueError,apache_log, input_line)   

    def test_wrong_line(self):
        input_line = "bau asetao euas uabsoeutaneusan uasoe tu asoeuta "
        assert_raises(ValueError,apache_log, input_line)   
        assert type(apache_log(input_line)) is type(dict())

    def test_wtf(self):
        input_line = "wtf"
        eq_([],[ f for f in  apache_log(input_line)])

################################################################################
from helpers import define_logkind

args = {"log_format": ""}

class test_define_logkind(BaseTest):
    def setUp(self):
        global args
        args = {}

    def test_no_format_defined_fall_to_apache(self):
        global args
        args["log_format"] = ""
        eq_("apache", define_logkind())

    def test_normal_format_recognised(self):
        global args
        args["log_format"] = "channel_manager"
        eq_("channel_manager", define_logkind())

    def test_unknown_format_not_recognised(self):
        global args
        args["log_format"] = "NOTVALID"
        eq_("apache", define_logkind())
