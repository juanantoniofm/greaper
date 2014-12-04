import unittest
from nose.tools import *

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
        eq_("",xml_stats(self.basic_logdata))

    @raises(TypeError)
    def test_none(self):
        eq_("",xml_stats(None))

    @raises(TypeError)
    def test_wrong_input(self):
        eq_("",xml_stats(""))
 
    def test_dont_die_for_bad_xml(self):
        """ if we pass bad xml, dont break, return original string"""
        input = """<WRONG><XML>"""
        eq_(input,xml_stats(input))
 
    def test_detect_response(self):
        expected1 = """RESPONSE rtt=848 ms; size=64 bytes"""
        expected2 = """RESPONSE rtt=1036 ms; size=64 bytes"""
        eq_("",xml_stats(self.responses[0]))
        eq_("",xml_stats(self.responses[1]))
 
    def test_detect_request(self):
        expected1 = """REQUEST size=64 bytes"""
        expected2 = """REQUEST size=64 bytes"""
        eq_("",xml_stats(self.request[0]))
        eq_("",xml_stats(self.request[1]))
 
    def test_nice_xml(self):
        """ if we pass valid xml, return nice stats"""
        eq_("",xml_stats(""))
 
    @nottest
    def test_dont_die_for_bad_xml(self):
        """ if we pass valid xml, return it nicely formatted"""
        eq_("",xml_stats(""))
e
