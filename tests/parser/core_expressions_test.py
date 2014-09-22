
from spidy.common import *

from expressions_test_base import ExpressionsTestBase

class CoreExpressionsTest(ExpressionsTestBase):
    
    def test_assignment1(self):
        self.assertEqual(self.evaluate('x = 1'), 1)
        
    def test_assignment2(self):        
        self.assertEqual(self.evaluate('x = y = 1'), 1)
        
    def test_assignment3(self):
        self.assertRaises(ParsingException, self.evaluate, 'x = 1 = 2')
        
    def test_assignment4(self):
        self.assertEqual(self.evaluate('[0][0] = 1'), 1)
        
    def test_assignment5(self):
        self.assertEqual(self.evaluate('(y) = z = [0][0] = 1'), 1)
    
    def test_assignment6(self):    
        self.assertEqual(self.evaluate('(y) = (z) = 1'), 1)
    
    def test_arithmetics1(self):        
        self.assertEqual(self.evaluate('2-3/ 3+ 1'), 2)
        
    def test_arithmetics2(self):         
        self.assertEqual(self.evaluate('2* (3 *2)+1/1'), 13)
        
    def test_arithmetics3(self):
        self.assertEqual(self.evaluate('3*(2-3/(2+1))'), 3)        
    
    def test_arithmetics4(self):
        self.assertRaises(ParsingException, self.evaluate, '1 1 + 2')
        
    def test_arithmetics5(self):
        self.assertRaises(ParsingException, self.evaluate, '(a or b)(c + 1)')
        
    def test_arithmetics6(self):
        self.assertEqual(self.evaluate('(1 or 2)+(2 + 1)'), 4)
        
    def test_arithmetics7(self):
        self.assertRaises(ParsingException, self.evaluate, '(x+1) y')
            
    def test_brackets1(self):
        self.assertEqual(self.evaluate(''), None)
        
    def test_brackets1(self):
        self.assertEqual(self.evaluate('()'), None)
        
    def test_brackets2(self):
        self.assertEqual(self.evaluate('10'), 10)
        
    def test_brackets3(self):
        self.assertEqual(self.evaluate('( 8)'), 8)
        
    def test_brackets4(self):
        self.assertEqual(self.evaluate('(((7)))'), 7)
        
    def test_brackets5(self):
        self.assertEqual(self.evaluate('(1+1)'), 2)
        
    def test_brackets6(self):
        self.assertEqual(self.evaluate('((3*3))'), 9)
        
    def test_brackets7(self):
        self.assertRaises(ParsingException, self.evaluate, '(0))')
        
    def test_brackets8(self):
        self.assertRaises(ParsingException, self.evaluate, '((100)')
        
    def test_brackets9(self):
        self.assertRaises(ParsingException, self.evaluate, '3(1+5)')
        
    def test_brackets10(self):
        self.assertRaises(ParsingException, self.evaluate, '(3())')
    
    def test_unary1(self):
        self.assertRaises(ParsingException, self.evaluate, '**2')
        
    def test_unary2(self):
        self.assertRaises(ParsingException, self.evaluate, '*1')
        
    def test_unary3(self):
        self.assertRaises(ParsingException, self.evaluate, '--1++')
        
    def test_unary4(self):
        self.assertEqual(self.evaluate('-(1)'), -1)
        
    def test_unary5(self):
        self.assertEqual(self.evaluate('(-1)'), -1)
        
    def test_unary6(self):
        self.assertEqual(self.evaluate('+-+1+2'), 1)

    def test_logical1(self):
        self.assertEqual(self.evaluate('1 or 0'), True)
        
    def test_logical2(self):
        self.assertEqual(self.evaluate('1 and (5 - 5)'), False)
        
    def test_logical3(self):
        self.assertEqual(self.evaluate('not not 1'), True)
        
    def test_comparison1(self):
        self.assertEqual(self.evaluate('3 >= 2'), True)
        
    def test_comparison2(self):
        self.assertEqual(self.evaluate('2 == 2'), True)
    
    def test_logical_arithmetics_mix1(self):
        self.assertRaises(ParsingException, self.evaluate, '2 + not 0')
        
    def test_logical_arithmetics_mix2(self):
        self.assertEqual(self.evaluate('2 > (not 1/5 + 1)'), True)
        
    def test_logical_arithmetics_mix3(self):
        self.assertEqual(self.evaluate('not 1 - 1'), True)
        
    def test_logical_arithmetics_mix4(self):
        self.assertEqual(self.evaluate('1 + (True and 0)'), 1)
        
    def test_logical_arithmetics_mix5(self):
        self.assertEqual(self.evaluate('1 + True and 0'), 0)
        
    def test_logical_arithmetics_mix6(self):
        self.assertEqual(self.evaluate('(not True)and(1-1)'), False)
        
    def test_logical_arithmetics_mix7(self):
        self.assertEqual(self.evaluate('not 0 and not(2/2-1)'), 1)
        
    def test_logical_arithmetics_mix8(self):
        self.assertEqual(self.evaluate('2 + (not 0)'), 3)
        
    def test_logical_arithmetics_mix9(self):
        self.assertEqual(self.evaluate('1 and 2*0'), False)
        
    def test_logical_arithmetics_mix10(self):
        self.assertEqual(self.evaluate('1 + 3 or 4 and 0'), 4)
        
    def test_logical_arithmetics_mix11(self):
        self.assertEqual(self.evaluate('True and False'), False)
        
    def test_logical_arithmetics_mix12(self):
        self.assertEqual(self.evaluate('45*(7 and (2/2 - 1))'), 0)
    
    def test_strings1(self):
        self.assertEqual(self.evaluate('not"!!!"or 0'), 0)
        
    def test_strings2(self):
        self.assertEqual(self.evaluate('"!!!"or 0'), '!!!')
        
    def test_strings3(self):
        self.assertEqual(self.evaluate('2*"x+1"'), 'x+1x+1')
        
    def test_strings4(self):
        self.assertEqual(self.evaluate('"x" + "y"'), 'xy')
        
    def test_strings5(self):
        self.assertRaises(ParsingException, self.evaluate, '"x + y')
    
    def test_strings6(self):
        self.assertEqual(self.evaluate('("hey")'), 'hey')
        
    def test_strings7(self):
        self.assertEqual(self.evaluate('"(-)"'), '(-)')

    def test_path1(self):
        self.assertEqual(self.evaluate('&"div/span[1]/span"'), '[items:3]')
        
    def test_path2(self):
        self.assertEqual(self.evaluate('&("div/span[1]/span" + "/span/")'), '[items:4]')
        
    def test_path3(self):
        self.assertRaises(EvaluationException, self.evaluate, '&div/span[1]')
        
    def test_path4(self):
        self.assertEqual(self.evaluate('&'), '[items:0]')
        
    def test_path5(self):
        self.assertEqual(self.evaluate('&"root/div/span(1)"'), '[items:3]')
        
    def test_path6(self):
        self.assertRaises(ParsingException, self.evaluate, '&"div@name/span[1]"')

    def test_list1(self):
        self.assertEqual(self.evaluate('[]'), [])
        
    def test_list2(self):
        self.assertEqual(self.evaluate('[1]'), [1])
    
    def test_list3(self):
        self.assertRaises(ParsingException, self.evaluate, '[,1]')
        
    def test_list4(self):
        self.assertEqual(self.evaluate('[1,2]+[3]'), [1,2,3])
        
    def test_list5(self):
        self.assertEqual(self.evaluate('([1] + [2])[0]'), 1)
        
    def test_list6(self):
        self.assertEqual(self.evaluate('[1,[-1,-2],2][1]'), [-1,-2])
        
    def test_list7(self):
        self.assertEqual(self.evaluate('[1]*3'), [1,1,1])
        
    def test_list8(self):
        self.assertEqual(self.evaluate('1 + ([1] + [2])[0]'), 2)
        
    def test_list9(self):
        self.assertEqual(self.evaluate('[[1,2], [-1,-2]][0][1]'), 2)
        
    def test_list10(self):
        self.assertRaises(ParsingException, self.evaluate, 'x[0]y')
        
    def test_list11(self):
        self.assertEqual(self.evaluate('[1]+[2]+[3]'), [1,2,3])
        
    def test_list12(self):
        self.assertRaises(Exception, self.evaluate, '[1]-[1]')
        
    def test_pop1(self):
        self.assertEqual(self.evaluate('[1,2] >>'), 2)
        
    def test_pop2(self):
        self.assertEqual(self.evaluate('[1,2][0] >>'), 1)
        
    def test_pop3(self):
        self.assertEqual(self.evaluate('[1,2][[1]>>]'), 2)
        
    def test_pop4(self):
        self.assertEqual(self.evaluate('1 == ([1])>>'), True)
        
    def test_pop5(self):
        self.assertEqual(self.evaluate('([0] + [1])>>'), 1)
        
    def test_pop6(self):
        self.assertEqual(self.evaluate('1 + ([0] + [1])>>'), 2)
        
    def test_pop7(self):
        self.assertRaises(Exception, self.evaluate, '2 >> 1')
        
    def test_push1(self):
        self.assertEqual(self.evaluate('[1] << 2'), 2)
        
    def test_push2(self):
        self.assertEqual(self.evaluate('[1][0] << 2'), 2)
        
    def test_push3(self):
        self.assertEqual(self.evaluate('[1]<<[1]<<2'), 2)
        
    def test_push4(self):
        self.assertEqual(self.evaluate('1 == [] << 2'), False)
        
    def test_push5(self):
        self.assertEqual(self.evaluate('[] << &"div:style"'), '[items:1]')
        
    def test_in1(self):
        self.assertEqual(self.evaluate('"a"in"Abc"'), True)
        
    def test_in2(self):
        self.assertEqual(self.evaluate('("a" + "B") in "xabc"'), True)
        
    def test_in3(self):
        self.assertEqual(self.evaluate('10 in [1,2,3]'), False)
        
    def test_in4(self):
        self.assertEqual(self.evaluate('1 in [1] and "hey" in "hello"'), False)