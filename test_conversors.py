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
