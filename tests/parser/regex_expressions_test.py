
from spidy.common import *

from expressions_test_base import ExpressionsTestBase

class RegexExpressionsTest(ExpressionsTestBase):

    def test_regex1(self):
        ''' input string, no capturing groups - returns whole match '''
        self.assertEqual(self.evaluate('"hello, John!" % "hello, [a-zA-Z]+!"'), 'hello, John!')
        
    def test_regex2(self):
        ''' input string, one capturing group - returns capture '''
        self.assertEqual(self.evaluate('"hello, John!" % "hello, ([a-zA-Z]+)!"'), 'John')
        
    def test_regex3(self):
        ''' input string, two capturing groups - returns list of captures '''
        self.assertEqual(self.evaluate('"hello, John!" % "(hello), ([a-zA-Z]+)!"'), ['hello', 'John'])
        
    def test_regex4(self):
        ''' input string, one capturing group, regex doesnt match - returns empty string '''
        self.assertEqual(self.evaluate('"hello, John!" % "hello, ([0-9]+)!"'), '')
        
    def test_regex5(self):
        ''' input not string, one capturing group - failed, evaluation exception is raised '''        
        self.assertRaises(EvaluationException, self.evaluate, '321321 % "hello, ([a-zA-Z]+)!"')
        
    def test_regex6(self):
        ''' input list of strings, no capturing groups - returns empty '''
        self.assertEqual(self.evaluate('["hello, John!", "hello, Kate!"] % "hello, [a-zA-Z]+!"'), ['hello, John!', 'hello, Kate!'])
        
    def test_regex7(self):
        ''' input list of strings, one capturing group - returns list of captures '''
        self.assertEqual(self.evaluate('["hello, John!", "hello, Kate!"] % "hello, ([a-zA-Z]+)!"'), ['John', 'Kate'])
                
    def test_regex8(self):
        ''' input list of strings, two capturing groups - returns list of lists of captures '''
        self.assertEqual(self.evaluate('["hello, John!", "hello, Kate!"] % "(hello), ([a-zA-Z]+)!"'), [['hello', 'John'], ['hello', 'Kate']])
        
    def test_regex9(self):
        ''' input list of strings, one capturing group, regex doesnt match - returns list of empty strings '''
        self.assertEqual(self.evaluate('["hello, John!", "hello, Kate!"] % "hello, ([0-9]+)!"'), ['', ''])
        
    def test_regex10(self):
        ''' input not string, one capturing group - failed, evaluation exception is raised '''        
        self.assertRaises(EvaluationException, self.evaluate, '["hello, John!", 3232]  % "hello, ([a-zA-Z]+)!"')
        
    def test_regex11(self):
        ''' input string, one capturing group, doesnt match - returns empty '''
        self.assertEqual(self.evaluate('"hello, John!" % "([0-9]+)"'), '')