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
#from parsmap import channel_manager_log
import parsmap

class test_channel_manager_log(BaseTest):
    """channel_manager_log need lines to be fed.
    just a list of  strings
    """
    def setUp(self):
        # open the file and load the sample
        self.applines=""
        with open("../crap/samples/sample.app.log","r") as f:
            self.applines = f.readlines()

        self.ap2lines=""
        with open("../crap/samples/sample.ap2.log","r") as f:
            self.ap2lines= f.readlines()

    #@mock.patch('parsmap.conversors.convert_time') # no module conversors
    @nottest
    @mock.patch('conversors.convert_time')
    def test_convert_time_error(self,mymock):
        mymock.side_effect=ValueError("bazinga!")
        result = parsmap.channel_manager_log(self.applines)
        calling = [l for l in result]
        # print "calling,",calling #noisy!
        eq_(True,mymock.called)

    @mock.patch('conversors.convert_xml')
    # @raises(ValueError) # it shouldn't raise here, but inside the conversor
    def test_xml_fail(self,mymock):
        mymock.side_effect=ValueError("bazinga!")
        mymock.return_value="bazinga!"
        result = parsmap.channel_manager_log(["Nov 25 16:34:00 appukcm03 cm-dsync-client-app: 2014-11-25 16:34:00,132 INFO  [jobScheduler_Worker-2: ] SyncJob.vcl - Job winding down..."])
        calling = [l for l in result]
        eq_([{'loglevel': 'INFO', 'tracing': 'jobScheduler_Worker-2: ', 'datetime': '16:34', 'machine': 'appukcm03', 'logdate': '16:34', 'action': 'Job winding down...', 'logfile': 'cm-dsync-client-app', 'jobtype': 'SyncJob.vcl'}],calling)
        #eq_(True,mymock.called)

    def test_empty_lines_list(self):
        """on empty list, raise"""
        input_line = []
        assert_raises(ValueError,parsmap.channel_manager_log, input_line)   

    def test_empty_lines(self):
        """on empty lines, return nothing"""
        input_line = ["",""]
        result = parsmap.channel_manager_log( input_line)  
        eq_([],[x for x in result])

    def test_wrong_line(self):
        input_line = "bau 131312     euas uabsoeutaneusan uasoe tu asoeuta "
        eq_("foo",parsmap.channel_manager_log(input_line.split()))
        assert_raises(ValueError,parsmap.channel_manager_log, input_line.split())   

    #@raises(ValueError)  # is not raised anymore, it breaks nicely
    def test_wtf_returns_empty(self):
        """a weird line returns nothing"""
        input_line = "wtf"
        eq_([],[ f for f in  parsmap.channel_manager_log(input_line)])

    def test_sample_lines(self):
        input_lines = self.applines
        r = parsmap.channel_manager_log(input_lines)
        result = [l for l in r]
        eq_(31,len(result))

    def test_sample_lines2(self):
        input_lines = self.ap2lines
        r = parsmap.channel_manager_log(input_lines)
        result = [l for l in r]
        eq_(len(input_lines),len(result))

################################################################################
from parsmap import apache_log

class test_apache_log(BaseTest):
    def setUp(self):
        self.apachelines = ""
        with open("../crap/samples/sample.apache.log","r") as f:
            self.apachelines = f.readlines()

    def test_empty_lines_list(self):
        """on empty list of lines, raise"""
        input_line = []
        assert_raises(ValueError,apache_log, input_line)   

    def test_empty_lines(self):
        """on empty lines, don't raise"""
        input_lines = ["",""]
        result = apache_log(input_lines)
        eq_([], [x for x in result])

    @nottest
    def test_wrong_line(self):
        """TODO: define this behaviour"""
        input_line = "bau asetao euas uabsoeutaneusan uasoe tu asoeuta "
        #assert_raises(ValueError,apache_log, input_line.split(" "))   
        eq_([input_line], apache_log(input_line.split(" ")))

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
        """test that at least works ok"""
        input_string = """fooo
                            barrr
                        baazzzz"""
        result = generic_log(
                    input_string.split("\n"),
                    r" *(.*)", # regex
                    ["fake"],  # colnames
                    {"fake": lambda x: x},  # converters
                    {}  # parameters
                    )


        eq_([{"fake":"fooo"},{"fake":"barrr"},{"fake":"baazzzz"}], 
                [ x for x in result]
            )


    def test_one_fails_isolated(self):
        """test that if one conversor fails, not all do"""
        input_string = """fo 111 baz
foo 222 baazz
fooo 333 baaazzz"""
        lista = input_string.split("\n")
        result = generic_log(
                    input_string.split("\n"),
                    r"(.*) (.*) (.*)", # regex
                    ["fo","bar","baz"],  # colnames
                    {"fo":lambda x: x + "!!", "bar": lambda x: int(x)},  # converters
                    {"fake":"param?"}  # parameters
                    )

        expected = [
                {"fo":"fo!!","bar":111,"baz":"baz"},
                {"fo":"foo!!","bar":222,"baz":"baazz"},
                {"fo":"fooo!!","bar":333,"baz":"baaazzz"}
                ]

        eq_(expected, [ x for x in result])


    @nottest
    def test_empty_params(self):
        eq_(None, generic_log([{"fake":"value"}],["fake"],{"fake":lambda x: x}))

    @raises(AssertionError)
    def test_empty_funcs(self):
        eq_(None, generic_log([{"fake":"value"}],["fake"]))

    @raises(AssertionError)
    def test_empty_colnames_raises(self):
        eq_(None, generic_log([{"fake":"value"}]))

################################################################################
from parsmap import list_fields

class test_list_fields(BaseTest):
    def test_normal_input(self):
        d = {"kind":{"column_names":"foo"}}
        res = list_fields(d)
        eq_(type(""),type(res))


################################################################################
from  parsmap import consumer


class test_consumer_decorator(BaseTest):
    def test_it_runs_the_lines(self):
        """just run the lines for coverage"""
        mymock = mock.MagicMock(lambda x : x)
        decorator = consumer(mymock)
        decorated = decorator("mymock2")
        eq_(mymock.called, True)

################################################################################
from parsmap import broadcast


class test_broadcast(BaseTest):
    def test_for_coverage(self):
        """just runs the lines"""
        mymock = mock.MagicMock(lambda x : x )
        @consumer(mymock)
        def consumed(x):
            return x
        source = "foo\nbar\nbaz"
        broadcast(source,[consumed])
        eq_(mymock.called, True)


################################################################################
from parsmap import matchit
import re

