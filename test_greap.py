import unittest
from nose.tools import *

################################################################################
from greap import grepit
import imp
imp.load_source("greap", "./greap")

class test_grepit(unittest.TestCase):
    def test_matches_an_expresion(self):
        eq_("foobar", grepit("foobar","ob"))

    def test_doesnt_match_wrong_expr(self):
        eq_("", grepit("naranja", "ob"))

    def test_doesnt_return_negrep(self):
        eq_("", grepit("foobar", nregex="ob"))
