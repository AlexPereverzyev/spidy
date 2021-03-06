
import unittest
import exceptions

from spidy.language import *
from spidy.common import *

class ScriptTest(unittest.TestCase):
    
    def test_script1(self):
	context = Context()
	sn = parse_file('tests/scripts/script1.sp', context)
	script_text = str(sn)
	self.assertEqual(script_text,
'''l = []
if True:
	traverse t in & breadthfirst (10 / 2):
		l << &t
l >>
''')

    def test_script2(self):
	context = Context()
	sn = parse_file('tests/scripts/script2.sp', context)
	script_text = str(sn)
	self.assertEqual(script_text,
'''get ('http://www.google' + '.com') as XML
part = 'blabla'
skip &('/root/div[1]/span' + part) forward
x = 0
y = 1
if (x or y):
	i = 0
	for c in chars:
		i = (i + 1)
		if y:
			break
		else:
			continue
	if x:
		skip &'/div/' reverse
		x = 0
	else:
		skip &'/div/div/' forward
		x = 1
else:
	get 'www.something.com' as HTML:
		X-Name: 'test'
		X-Date: ('today' + '-tomorrow')
		X-State: x
return i
''')
	
    def test_script3(self):
	context = Context()
	sn = parse_inline(
'''
if (True):
    // standard header comment
    for c in [1,2,3]: // -- inline comments are OK
        x = 1
    
    lst = [1,
        //2, -- comments inside of multiline statements
	
        'parenthesis(in string[ are ignored',	
    3]
''', context)
	script_text = str(sn)
	self.assertEqual(script_text,
'''if True:
	for c in [1, 2, 3]:
		x = 1
	lst = [1, 'parenthesis(in string[ are ignored', 3]
''')