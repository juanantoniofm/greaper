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

    def test_empty_content_is_ok(self):
        eq_("",convert_xml(self.basic_logdata))
