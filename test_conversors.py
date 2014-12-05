import unittest
from nose.tools import *


################################################################################
from conversors import convert_time

class test_convert_time(unittest.TestCase):
    """basic integrity tests"""
    def test_valid_time_valid_output(self):
        """ valid time valid output """
        eq_("06:44",convert_time("17/Nov/2014:06:44:08 +0000"))

    def test_valid_time_alt_input_format(self):
        """ valid time in alt input format """
        eq_("00:02",convert_time("2014-11-25 00:02:00,180","%Y-%m-%d %H:%M:%S,%f"))

    def test_valid_time_alt_output_format(self):
        """ valid time valid output alt format"""
        eq_("06_44_08",convert_time("17/Nov/2014:06:44:08 +0000",out_format="%H_%M_%S"))

    def test_valid_converts_microseconds(self):
        """ valid time valid output alt format"""
        eq_("00_02_00_180000",convert_time("2014-11-25 00:02:00,180",
                            in_format="%Y-%m-%d %H:%M:%S,%f",
                            out_format="%H_%M_%S_%f"))


    @raises(TypeError)
    def test_none_values(self):
        """ None value raises TypeError """
        convert_time(None)

    @raises(TypeError)
    def test_empty_string_raises_TypeError(self):
        """ empty string raises TypeError """
        convert_time("")

    @raises(TypeError)
    def test_empty_format_raises_typeerror(self):
        """ empty_format_raises_typeerror"""
        convert_time("17/Nov/2014:06:44:08 +0000", "")

    @raises(TypeError)
    def test_empty_outformat_raises_typeerror(self):
        """ empty_format_raises_typeerror"""
        convert_time("17/Nov/2014:06:44:08 +0000", out_format="")

    @nottest
    def test_(self):
        """ XX """
        convert_time()


################################################################################
from conversors import clean_action_to_xml

class test_clean_action_to_xml(unittest.TestCase):
    @raises(TypeError)
    def test_empty_content(self):
        clean_action_to_xml("")

################################################################################
from conversors import convert_xml

class test_convert_xml(unittest.TestCase):
    def setUp(self):
        self.basic_logdata = {"action":""}

    @raises(TypeError)
    def test_a_dic_is_wrong(self):
        eq_("",convert_xml(self.basic_logdata))

    @raises(TypeError)
    def test_none(self):
        eq_("",convert_xml(None))

    @raises(TypeError)
    def test_wrong_input(self):
        eq_("",convert_xml(""))
    #TODO: add some better active tests for convert_xml like
    """ if we pass bad xml, dont break, return original string"""
    """ if we pass valid xml, return it nicely formatted"""

################################################################################
from conversors import xml_stats

class test_xml_stats(unittest.TestCase):
    def setUp(self):
        request1 = """[REQUEST] [<SOAP-ENV:Header xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"/>, <SOAP-ENV:Body xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"><ReadService xmlns="http://www.juniper.es/webservice/2010/"><ReadRQ Language="en" Version="1"><Login Email="MOLTON-NISANTASI" Password="Lots1234"/><Request><ModificationDateFrom>2014-12-01</ModificationDateFrom><ModificationDateTo>2014-12-05</ModificationDateTo></Request></ReadRQ></ReadService></SOAP-ENV:Body>]"""
        request2 = """[REQUEST] [<SOAP-ENV:Header xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"/>, <SOAP-ENV:Body xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"><ReadService xmlns="http://www.juniper.es/webservice/2010/"><ReadRQ Language="en" Version="1"><Login Email="testsiteminder" Password="Siteminder2014"/><Request><ModificationDateFrom>2014-12-01</ModificationDateFrom><ModificationDateTo>2014-12-05</ModificationDateTo></Request></ReadRQ></ReadService></SOAP-ENV:Body>]"""
        response2 = """[RESPONSE in 1036 ms] [, <soap:Body xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><ReadServiceResponse xmlns="http://www.juniper.es/webservice/2010/"><ReadRS><Reservations/></ReadRS></ReadServiceResponse></soap:Body>]"""
        response1 = """[RESPONSE in 848 ms] [, <soap:Body xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><ReadServiceResponse xmlns="http://www.juniper.es/webservice/2010/"><ReadRS><Reservations/></ReadRS></ReadServiceResponse></soap:Body>]"""
        self.responses = [response1,response2]
        self.requests = [request1,request2]

    @raises(TypeError)
    def test_a_dic_is_wrong(self):
        eq_("",xml_stats({}))

    @raises(TypeError)
    def test_none(self):
        eq_("",xml_stats(None))

    @raises(TypeError)
    def test_empty_string_raises(self):
        eq_("",xml_stats(""))
 
    def test_dont_die_for_bad_xml(self):
        """ if we pass bad xml, dont break, return original string"""
        input = """<WRONG><XML>"""
        eq_(input,xml_stats(input))
 
    def test_detect_response(self):
        """detect properly a response"""
        expected1 = """RESPONSE size=202 chars; rtt:848;"""
        expected2 = """RESPONSE size=202 chars; rtt:1036;"""
        eq_(expected1,xml_stats(self.responses[0]))
        eq_(expected2,xml_stats(self.responses[1]))
 
    def test_detect_request(self):
        """detect properly a request"""
        expected1 = """REQUEST size=464 chars;"""
        expected2 = """REQUEST size=468 chars;"""
        eq_(expected1,xml_stats(self.requests[0]))
        eq_(expected2,xml_stats(self.requests[1]))
 
    def test_nice_xml(self):
        """ if we pass valid xml, return nice stats"""
        inputxml = """[REQUEST] [<root></root>]"""
        expect = """REQUEST size=13 chars;"""
        eq_(expect,xml_stats(inputxml))
 
    @nottest
    def test_dont_die_for_bad_xml(self):
        """ if we pass valid xml, return it nicely formatted"""
        eq_("",xml_stats(""))


#TODO: add tests for trim_token and brother
