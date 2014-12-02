import unittest
from nose.tools import *
import mock



class BaseTest(unittest.TestCase):
    def setUp(self):
        pass


################################################################################
from parsmap import convert_time
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
from parsmap import  validate_logkind

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
from parsmap import channel_manager_log

class test_app_log(BaseTest):
    """app_log need lines to be fed.
    just a list of  strings
    """
    def setUp(self):
        # open the file and load the sample
        self.applines=""
        with open("sample.app.log","r") as f:
            self.applines = f.readlines()

    @mock.patch('parsmap.conversors.convert_time')
    def test_convert_time_error(self,mymock):
        mymock.side_effect=ValueError("bazinga!")
        r = app_log(self.applines)
        calling = [l for l in r]
        eq_(True,mymock.called)

    @mock.patch('conversors.convert_xml')
    def test_xml_fail(self,mymock):
        mymock.side_effect=ValueError("bazinga!")
        mymock.return_value="bazinga!"
        r = app_log(["Nov 25 16:34:00 appukcm03 cm-dsync-client-app: 2014-11-25 16:34:00,132 INFO  [jobScheduler_Worker-2: ] SyncJob.vcl - Job winding down..."])
        calling = [l for l in r]
        eq_([{'loglevel': 'INFO', 'tracing': 'jobScheduler_Worker-2: ', 'datetime': '16:34', 'machine': 'appukcm03', 'logdate': '16:34', 'action': 'Job winding down...', 'logfile': 'cm-dsync-client-app', 'jobtype': 'SyncJob.vcl'}],calling)
        eq_(True,mymock.called)

    def test_empty_lines(self):
        input_line = []
        assert_raises(ValueError,app_log, input_line)   

    def test_wrong_line(self):
        input_line = "bau asetao euas uabsoeutaneusan uasoe tu asoeuta "
        assert_raises(ValueError,app_log, [input_line])   
        assert type(app_log(input_line)) is type(dict())

    def test_wtf(self):
        input_line = "wtf"
        eq_([],[ f for f in  app_log(input_line)])

    def test_sample_lines(self):
        input_lines = self.applines
        r = app_log(input_lines)
        res = [l for l in r]
        eq_(31,len(res))

################################################################################
from parsmap import apache_log

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
from parsmap import define_logkind

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


################################################################################
from parsmap import  field_map

class test_field_map(BaseTest):
    def setUp(self):
        self.columns = ('a','b','c')
        self.fields = ('11','22','33')
        self.d = dict(zip(self.columns,self.fields))
        def fake_func(param):
            return int(param)
        self.ff = fake_func


    def test_testing_test(self):
        """
        testing if we can actually test this thing
        NOTE:
            - we have to pass an iterator to field_map
            - it will return a generator
            - that we have to use to make the actual calls
        """
        # we call the function, passing a seq/list of dics, the field to map,
        # and the func to use
        self.d = field_map([self.d],'a',self.ff)
        # then we convert the generator to a dic to get the content,
        # and put it on another seq/list
        resd = [(f)  for f in self.d]
        # and then the assertion
        eq_({'a':11,'b':'22','c':'33'}, resd[0])

    @raises(Exception)
    def test_that_raises(self):
        """
        we break how we break
        """
        def breaker(ignored):
            print "Im not being called. why?"
            raise Exception("bazinga")

        d = field_map([self.d],'b',breaker)
        [f for f in r] # if we dont use the generator, no call will be done

    def test_field_map_passes_params(self):
        mymock = mock.MagicMock(return_value="relol")
        r = field_map([self.d],'b',mymock,"myparam")
        [f for f in r] # if we dont use the generator, no call will be done
        calls = [mock.call('22', 'myparam')]
        #print "calls:",mymock.call_args_list
        mymock.assert_has_calls(calls)
        eq_(True, mymock.called)


    @raises(Exception)
    def test_field_map_side_effect(self):
        """ testing what happends on side_effects"""
        mymock = mock.MagicMock(return_value="relol",side_effect = Exception("kaboom"))
        mymock.return_value="lol"
        r = field_map([self.d],'b',mymock)
        [f for f in r] # if we dont use the generator, no call will be done
        eq_(True, mymock.called)


################################################################################
from parsmap import generic_log

class test_generic_log(BaseTest):
    def setUp(self):
        pass

    def test_is_ok(self):
        eq_(None, generic_log([{"fake":"value"}],["fake"],{"fake":lambda x: x},{"fake":"param?"}))

    def test_empty_params(self):
        eq_(None, generic_log([{"fake":"value"}],["fake"],{"fake":lambda x: x}))

    def test_empty_funcs(self):
        eq_(None, generic_log([{"fake":"value"}],["fake"]))

    @raises(AssertionError)
    def test_empty_colnames_raises(self):
        eq_(None, generic_log([{"fake":"value"}]))

################################################################################
from parsmap import list_fields

class test_list_fields(BaseTest):
    def test_normal_input(self):
        d = {"kind":{"field1":"foo"}}
        res = list_fields(d)
        eq_(type(""),type(res))
