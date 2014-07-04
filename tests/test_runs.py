
import unittest
import logging

from spidy.language import scripter
from parser.expressions_test import ExpressionsTest
from parser.script_test import ScriptTest
from parser.doc_test import DocTest
from shell.shell_test import ShellTest
from shell.xpath_test import XPathTest

def run_expressions_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(ExpressionsTest)
    unittest.TextTestRunner(verbosity=1).run(suite)
    
def run_script_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(ScriptTest)    
    unittest.TextTestRunner(verbosity=1).run(suite)
    
def run_doc_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(DocTest)    
    unittest.TextTestRunner(verbosity=1).run(suite)
    
def run_shell_tests():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(ShellTest))
    suite.addTests(unittest.makeSuite(XPathTest))
    unittest.TextTestRunner(verbosity=1).run(suite)
    
def run_all_tests():
    logging.disable(100)
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(ExpressionsTest))
    suite.addTests(unittest.makeSuite(ScriptTest))
    suite.addTests(unittest.makeSuite(DocTest))    
    suite.addTests(unittest.makeSuite(ShellTest))
    suite.addTests(unittest.makeSuite(XPathTest))
    unittest.TextTestRunner(verbosity=1).run(suite)
    
def parse_test1_script():
    sn = scripter.parse_script('scripts/script1.sp')
    print str(sn)
    
def parse_test2_script():
    sn = scripter.parse_script('scripts/script2.sp')
    print str(sn)