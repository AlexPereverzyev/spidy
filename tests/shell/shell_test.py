
import unittest
import spidy as SS

from spidy.common import *

class ShellTest(unittest.TestCase):
    
    def test_return1(self):
        '''return nothing'''
        out = SS.do('''x = 2*2''')        
        self.assertEqual(out, None)
        
    def test_return2(self):
        '''return var from context'''
        out = SS.do('''
                    x = 2*2
                    y = 1
                    return y
                    ''')
        self.assertEqual(out, 1)
        
    def test_return3(self):
        '''return expression'''
        out = SS.do('''
                    y = 1
                    return 'hey'*3
                    ''')
        self.assertEqual(out, 'heyheyhey')
        
    def test_return4(self):
        '''return None'''
        out = SS.do('''
                    return None
                    ''')
        self.assertEqual(out, None)
        
    def test_return5(self):
        '''return undefined var, fail'''
        self.assertRaises(EvaluationException, SS.do,
                    '''
                    y = 1
                    return z
                    ''')
        
    def test_return6(self):
        ''' return terminates script '''
        out = SS.do('''
                    return True
                    return False
                    ''')
        self.assertEqual(out, True)
        
    def test_return7(self):
        ''' nested return terminates script '''
        out = SS.do('''
                    if True:
                        return True
                    return False
                    ''')
        self.assertEqual(out, True)
        
    def test_get1(self):
        '''get 'tests/files/doc1.xml' '''
        out = SS.do('''
                    get 'tests/files/doc1.xml' 
                    ''')
        self.assertEqual(out, None)
        
    def test_get2(self):
        ''' try get doc of unknown format - error'''
        self.assertRaises(DocumentException, SS.do,
                    '''
                    get 'tests/files/doc_no_ext'
                    return &
                    ''')
        
    def test_get3(self):
        ''' try get doc, doc is not loaded, error ignored '''
        out = SS.do('''
                    get 'tests/files/doc1.txt' as xml
                    return & == ''
                    ''')
        self.assertEqual(out, True)
        
    def test_get4(self):
        '''get 'files/doc_xml' as xml '''
        out = SS.do('''
                    get 'tests/files/doc_no_ext' as xml 
                    ''')
        self.assertEqual(out, None)

    def test_skip1(self):
        ''' skip, get value '''
        out = SS.do('''
                    get 'tests/files/doc1.xml'
                    skip &'root/div/span'
                    return &'/.@name'
                    ''')
        self.assertEqual(out, 'first')
        
    def test_skip2(self):
        ''' skip, skip reverse, get value '''
        out = SS.do('''
                    get 'tests/files/doc1.xml'
                    skip &'root/div/span'
                    skip &'span/div' reverse
                    return &'p[1]'
                    ''')
        self.assertEqual(out, 'fruits')
        
    def test_skip3(self):
        ''' skip wrong path, pointer is not updated '''
        out = SS.do('''
                    get 'tests/files/doc1.xml'
                    skip &'root/span/span'
                    return &'.@name'
                    ''')
        self.assertEqual(out, '')
        
    def test_skip4(self):
        ''' skip, skip reverse wrong path, pointer is not updated '''
        out = SS.do('''
                    get 'tests/files/doc1.xml'
                    skip &'root/div/span'
                    skip &'div' reverse
                    return &'.@name'
                    ''')
        self.assertEqual(out, 'first')
        
    def test_skip5(self):
        ''' skip, skip reverse beyond root, pointer is not updated '''
        out = SS.do('''
                    get 'tests/files/doc1.xml'
                    skip &'root/div/span'
                    skip &'span/div/root/beyond' reverse
                    return &'.@name'
                    ''')
        self.assertEqual(out, 'first')
        
    def test_push1(self):
        ''' define list, push to list '''
        out = SS.do('''
                    lst = []
                    lst << True
                    return lst[0]
                    ''')
        self.assertEqual(out, True)
        
    def test_push2(self):
        ''' define list, push to list, insert to list '''
        out = SS.do('''
                    lst = []
                    lst << True
                    lst[0] << False
                    return lst[0]
                    ''')
        self.assertEqual(out, False)
        
    def test_push3(self):
        ''' define list, push nothing to list '''
        self.assertRaises(ParsingException, SS.do,
                    '''
                    lst = []
                    lst <<
                    ''')
        
    def test_push4(self):
        ''' define list, push nothing to list '''
        self.assertRaises(EvaluationException, SS.do,
                    '''
                    lst = 'not list'
                    lst << True
                    ''')
        
    def test_push5(self):
        ''' define list, insert wrong index to list '''
        self.assertRaises(EvaluationException, SS.do,
                    '''
                    lst = []
                    lst[1] << True
                    ''')
        
    def test_pop1(self):
        ''' define list, push to list, pop from list '''
        out = SS.do('''
                    lst = []
                    lst << True
                    lst >>
                    return lst
                    ''')
        self.assertEqual(out, [])
        
    def test_pop2(self):
        ''' define list, pop from list '''
        self.assertRaises(EvaluationException, SS.do,
                    '''
                    lst = []
                    lst >>
                    ''')
        
    def test_pop3(self):
        ''' define list, pop at index from list '''
        self.assertRaises(EvaluationException, SS.do,
                    '''
                    lst = []
                    lst[0] >>
                    ''')
        
    def test_pop4(self):
        ''' define list, push to list, push to list, pop at index from list '''
        out = SS.do('''
                    lst = []
                    lst << True
                    lst << False
                    lst[0] >>
                    return lst
                    ''')
        self.assertEqual(out, [False])
            
    def test_pop5(self):
        ''' define list, push to list, pop at index from list to variable '''
        out = SS.do('''
                    lst = []
                    lst << True
                    lst[0] >> v
                    return v
                    ''')
        self.assertEqual(out, True)
        
    def test_pop6(self):
        ''' define list, push to list, pop at index from list to inexer '''
        out = SS.do('''
                        lst = [True]
                        lst2 = [False]
                        lst[0] >> lst2[0]
                        return lst2
                    ''')
        self.assertEqual(out, [True])
        
    def test_forin1(self):
        ''' enumerate list items '''
        out = SS.do('''
                    r = ''
                    src = [1,2,3]
                    for v in src:
                        r = r + $v
                    return r
                    ''')
        self.assertEqual(out, '123')
        
    def test_forin2(self):
        ''' enumerate expression '''
        out = SS.do('''
                    r = ''
                    for v in ([1,2] + [3]):
                        r = r + $v
                    return r
                    ''')
        self.assertEqual(out, '123')
        
    def test_forin3(self):
        ''' enumerate not list '''
        self.assertRaises(EvaluationException, SS.do,
                    '''
                    r = ''
                    src = 'not list'
                    for v in src:
                        r = r + $v
                    ''')
        
    def test_forin4(self):
        ''' enumerate list, loop var re-defined '''
        self.assertRaises(EvaluationException, SS.do,
                    '''
                    v = 1
                    r = ''
                    src = 'not list'
                    for v in src:
                        r = r + $v
                    ''')
        
    def test_traverse1(self):
        ''' traverse with default args, get first level elements '''
        out = SS.do('''
                    get 'tests/files/doc2.xml'
                    paths = ''
                    traverse p in &'root/div':
                        paths = paths + p + '\n'
                    return paths
                    ''')
        self.assertEqual(out, '''/div[1]\n/span[1]\n/table[1]\n''')
        
    def test_traverse2(self):
        ''' traverse 3 level breadth first '''
        out = SS.do('''
                    get 'tests/files/doc2.xml'
                    paths = ''
                    traverse p in &'root/div' breadthfirst 3:
                        paths = paths + p + '\n'
                    return paths
                    ''')
        self.assertEqual(out, '''/div[1]\n/span[1]\n/table[1]\n/div[1]/p[1]\n/div[1]/p[2]\n/div[1]/p[3]\n/span[1]/p[1]\n/span[1]/p[2]\n/span[1]/p[3]\n/table[1]/span[1]\n/table[1]/span[2]\n/table[1]/span[3]\n/span[1]/p[2]/span[1]\n/span[1]/p[2]/span[2]\n/span[1]/p[2]/span[3]\n/table[1]/span[2]/span[1]\n/table[1]/span[2]/div[1]\n/table[1]/span[2]/div[2]\n/table[1]/span[2]/div[3]\n''')
        
    def test_traverse3(self):
        ''' traverse 3 level depth first '''
        out = SS.do('''
                    get 'tests/files/doc2.xml'
                    paths = ''
                    traverse p in &'root/div' depthfirst 3:
                        paths = paths + p + '\n'
                    return paths
                    ''')
        self.assertEqual(out, '''/div[1]\n/div[1]/p[1]\n/div[1]/p[2]\n/div[1]/p[3]\n/span[1]\n/span[1]/p[1]\n/span[1]/p[2]\n/span[1]/p[2]/span[1]\n/span[1]/p[2]/span[2]\n/span[1]/p[2]/span[3]\n/span[1]/p[3]\n/table[1]\n/table[1]/span[1]\n/table[1]/span[2]\n/table[1]/span[2]/span[1]\n/table[1]/span[2]/div[1]\n/table[1]/span[2]/div[2]\n/table[1]/span[2]/div[3]\n/table[1]/span[3]\n''')
        
    def test_traverse4(self):
        ''' traverse -1 level depthfirst, exception is raised '''        
        self.assertRaises(EvaluationException, SS.do,'''
                    get 'tests/files/doc2.xml'
                    paths = ''
                    traverse p in &'root/div' depthfirst -1:
                        paths = paths + p + '\n'
                    return paths
                    ''')
        
    def test_traverse5(self):
        ''' traverse, check doc pointer is where is was before '''
        out = SS.do('''
                    get 'tests/files/doc2.xml'
                    traverse p in &'root/div':
                        x = True
                    return &'root/p[1]'
                    ''')
        self.assertEqual(out, 'fruits')
        
    def test_break1(self):
        ''' break a loop '''
        out = SS.do('''
                    v = 0
                    for i in [1,2,3,4,5]:
                        v = i
                        break
                    return v
                    ''')
        self.assertEqual(out, 1)
        
    def test_break2(self):
        ''' break inner loop '''
        out = SS.do('''
                    u = 0
                    v = 0                    
                    for i in [1,2,3]:
                        for j in [1,2,3]:
                            v = j
                            break
                        u = i
                    return $u + '-' + $v
                    ''')
        self.assertEqual(out, '3-1')
        
    def test_break3(self):
        ''' break inner loop, continue outer loop '''
        out = SS.do('''
                    u = 0
                    v = 0                    
                    for i in [1,2,3]:
                        for j in [1,2,3]:
                            v = j
                            break
                        continue
                        u = i
                    return $u + '-' + $v
                    ''')
        self.assertEqual(out, '0-1')
        
    def test_break4(self):
        ''' break traverse loop '''
        out = SS.do('''
                    get 'tests/files/doc2.xml' as xml
                    vs = ''
                    traverse p in &'root/div':
                        vs = vs + p + '\n'
                        break
                    return vs
                    ''')
        self.assertEqual(out, '/div[1]\n')
        
    def test_continue1(self):
        ''' continue a loop '''
        out = SS.do('''
                    v = 0
                    for i in [1,2,3,4,5]:                        
                        continue
                        v = i
                    return v
                    ''')
        self.assertEqual(out, 0)
        
    def test_continue2(self):
        ''' continue inner loop '''
        out = SS.do('''
                    u = 0
                    v = 0                    
                    for i in [1,2,3]:
                        for j in [1,2,3]:
                            continue
                            v = j
                        u = i
                    return $u + '-' + $v
                    ''')
        self.assertEqual(out, '3-0')
        
    def test_continue3(self):
        ''' continue traverse loop '''
        out = SS.do('''
                    get 'tests/files/doc2.xml' as xml
                    vs = ''
                    traverse p in &'root/div':
                        if p == '/span[1]':
                            continue                    
                        vs = vs + p + '\n'
                    return vs
                    ''')
        self.assertEqual(out, '/div[1]\n/table[1]\n')
        
    def test_while1(self):
        ''' loop N times '''
        out = SS.do('''
                    i = 3                    
                    while i >= 0:
                        i = i - 1
                    return i
                    ''')
        self.assertEqual(out, -1)
        
    def test_while2(self):
        ''' break infinitive loop '''
        out = SS.do('''
                    i = 0
                    while True:
                        if i == 3:
                            break
                        i = i + 1
                    return i
                    ''')
        self.assertEqual(out, 3)
        
    def test_while3(self):
        ''' pop list until its empty '''
        out = SS.do('''
                    r = 0
                    lst = [1,2,3]
                    while lst:
                        lst >> r
                    return r
                    ''')
        self.assertEqual(out, 1)
        
    def test_merge1(self):
        ''' merge ctx with template, return result '''
        out = SS.do('''
                    name = 'John'
                    age = 34
                    merge 'tests/files/template2.html' as row
                    return row
                    ''')
        self.assertEqual(out, '<tr><td>John</td><td>34</td></tr>')
        
    def test_merge2(self):
        ''' merge ctx with each list item, then merge result with master template '''
        out = SS.do('''
                    ppl = [['Joe', 18], ['Jack', 35]]
                    rows = ''
                    for p in ppl:
                        name = p[0]
                        age = p[1]
                        merge 'tests/files/template2.html' as row
                        rows = rows + row                
                    merge 'tests/files/template1.html' as r
                    return r
                    ''')
        self.assertEqual(out, '<html xmlns="http://www.w3.org/1999/xhtml"><head/><body><div><table><tbody><tr><th>Name</th><th>Age</th></tr><tr><td>Joe</td><td>18</td></tr><tr><td>Jack</td><td>35</td></tr></tbody></table></div></body></html>')