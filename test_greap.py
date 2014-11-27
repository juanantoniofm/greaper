import unittest
from nose.tools import *

################################################################################
from greap import grepit
import imp
imp.load_source("greap", "./greap")

class test_grepit(unittest.TestCase):
    def test_matches_an_expresion(self):
        """simple matching"""
        eq_("foobar", grepit("foobar","ob"))

    def test_doesnt_match_foreign_expr(self):
        """if the positive expresion dont match and no neg, dont show"""
        eq_("", grepit("naranja", "ob"))

    def test_doesnt_return_negrep(self):
        """simple negative matching"""
        eq_("", grepit("foobar", "",nregex="ob"))

    def test_matches_both_no_print(self):
        """ if matches both dont show """
        eq_("",grepit("foobar","oo","fo"))

    @nottest
    def test_(self):
        """ t """
        eq_("",grepit("",))
