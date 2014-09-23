
import unittest
import spidy as SS

from spidy.common import *

class XPathTest(unittest.TestCase):

    def test_path1(self):
        ''' & get value '''
        out = SS.do('''
                    get 'tests/files/doc1.xml'
                    x = &'/root/div/span[1]/'
                    return x
                    ''')
        self.assertEqual(out, 'apple')
        
    def test_path2(self):
        ''' & get value wrong path '''
        out = SS.do('''
                    get 'tests/files/doc1.xml'
                    x = &'/root/div/h[1]/'
                    return x
                    ''')
        self.assertEqual(out, '')
        
    def test_path3(self):
        ''' & get attribute '''
        out = SS.do('''
                    get 'tests/files/doc1.xml'
                    x = &'/root/div/span@name[1]'
                    return x
                    ''')
        self.assertEqual(out, 'first')
        
    def test_path4(self):
        ''' & get attribute, wrong name '''
        out = SS.do('''
                    get 'tests/files/doc1.xml'
                    x = &'/root/div/span[1]@wrong'
                    return x
                    ''')
        self.assertEqual(out, '')
        
    def test_path5(self):
        ''' & get attribute, attribute not on last item '''
        self.assertRaises(ParsingException, SS.do,
                    '''
                    get 'tests/files/doc1.xml'
                    x = &'/root/div@missplaced/span[1]@wrong'
                    return x
                    ''')
        
    def test_path6(self):
        ''' & get value, no document '''
        self.assertRaises(EvaluationException, SS.do,
                    '''
                    x = &'/root/div'
                    return x
                    ''')
        
    def test_path7(self):
        ''' & get whole document '''
        out = SS.do('''
                    get 'tests/files/doc1.xml'                    
                    return &
                    ''')
        self.assertEqual(out,
'''<root>
    <p>fruits</p>
    <div>
        <span name="first">apple</span>
        <span name="second" mark="xxx">orange</span>
        <span name="third" class="c@stom">mango</span>
    </div>
</root>''')
        
    def test_path8(self):
        ''' & get current path pointer value '''
        out = SS.do('''
                    get 'tests/files/doc1.xml'
                    skip &'/root/div/span[1]'
                    return &'.'
                    ''')
        self.assertEqual(out, 'apple')
        
    def test_path9(self):
        ''' & get current path pointer attribute value '''
        out = SS.do('''
                    get 'tests/files/doc1.xml'
                    skip &'/root/div/span'
                    return &'.@name'
                    ''')
        self.assertEqual(out, 'first')
        
    def test_path10(self):
        ''' & get current path pointer attribute value, wrong name '''
        out = SS.do('''
                    get 'tests/files/doc1.xml'
                    skip &'/root/div/span[1]'
                    return &'.@wrong'
                    ''')
        self.assertEqual(out, '')
        
    def test_path11(self):
        ''' & get attribute value after index selector '''
        out = SS.do('''
                    get 'tests/files/doc1.xml'
                    return &'/root/div[1]/span[2]@name'
                    ''')
        self.assertEqual(out, 'second')
        
    def test_path12(self):
        ''' & simple attribute selector '''
        out = SS.do('''
                    get 'tests/files/doc1.xml'
                    return &'/root/div[1]/span[@mark][1]'
                    ''')
        self.assertEqual(out, 'orange')
        
    def test_path13(self):
        ''' & simple attribute selector w/ attr value'''
        out = SS.do('''
                    get 'tests/files/doc1.xml'
                    return &'/root/div[1]/span[@mark=xxx][1]'
                    ''')
        self.assertEqual(out, 'orange')
        
    def test_path14(self):
        ''' & simple attribute selector w/ empty attr value'''
        out = SS.do('''
                    get 'tests/files/doc1.xml'
                    return &'/root/div[1]/span[@mark=][1]'
                    ''')
        self.assertEqual(out, '')
    
    def test_path15(self):
        ''' & attribute selector w/ index selector '''
        out = SS.do('''
                    get 'tests/files/doc1.xml'
                    return &'/root/div[1]/span[@mark][1]'
                    ''')
        self.assertEqual(out, 'orange')
        
    def test_path16(self):
        ''' & attribute selector w/ two index selector, fails '''
        self.assertRaises(ParsingException, SS.do,
                    '''
                    get 'tests/files/doc1.xml'
                    return &'/root/div[1]/span[@mark][1][2]'
                    ''')
    
    def test_path17(self):
        ''' & two attribute selector, fails '''
        self.assertRaises(ParsingException, SS.do,
                    '''
                    get 'tests/files/doc1.xml'
                    return &'/root/div[1]/span[@mark][@tick]'
                    ''')
        
    def test_path18(self):
        ''' & attribute selector w/ double @, fails '''
        self.assertRaises(ParsingException, SS.do,
                    '''
                    get 'tests/files/doc1.xml'
                    return &'/root/div[1]/span[@@mark]'
                    ''')
        
    def test_path19(self):
        ''' & get attribute value after index selector w/ attribute selector '''
        out = SS.do('''
                    get 'tests/files/doc1.xml'
                    return &'/root/div[1]/span[2]@name[@mark]'
                    ''')
        self.assertEqual(out, 'second')
        
    def test_path20(self):
        ''' & get value, attribute selector in the mid of the path '''
        out = SS.do('''
                    get 'tests/files/doc2.xml'
                    return &'/root/div/table/span[@class=label]/div[2]'
                    ''')
        self.assertEqual(out, '2')
        
    def test_path21(self):
        ''' & search for first p tag '''
        out = SS.do('''
                    get 'tests/files/doc1.xml'
                    return &'//p[1]'
                    ''')
        self.assertEqual(out, 'fruits')
        
    def test_path22(self):
        ''' & search by attr value '''
        out = SS.do('''
                    get 'tests/files/doc1.xml'
                    return &'//*[@mark=xxx][1]'
                    ''')
        self.assertEqual(out, 'orange')
        
    def test_path23(self):
        ''' & combined search, skip then search for second span '''
        out = SS.do('''
                    get 'tests/files/doc1.xml'
                    return &'/root//span[2]'
                    ''')
        self.assertEqual(out, 'orange')
        
    def test_path24(self):
        ''' & sequential search, search for first div, then for any tag with attribute'''
        out = SS.do('''
                    get 'tests/files/doc1.xml'
                    return &'//div//*[@mark][1]'
                    ''')
        self.assertEqual(out, 'orange')
        
    def test_path25(self):
        ''' & . in search, fails '''
        self.assertRaises(ParsingException, SS.do,
                    '''
                    get 'tests/files/doc1.xml'
                    return &'//.[@mark]'
                    ''')
        
    def test_path26(self):
        ''' & double * in search, fails '''
        self.assertRaises(ParsingException, SS.do,
                    '''
                    get 'tests/files/doc1.xml'
                    return &'//**[@mark]'
                    ''')
        
    def test_path27(self):
        ''' & search p tag which has at least one attribute, returns empty '''
        out = SS.do('''
                    get 'tests/files/doc1.xml'
                    return &'//p[@*][1]'
                    ''')
        self.assertEqual(out, '')
        
    def test_path28(self):
        ''' & get tag value w/ special symbol in attribute '''
        out = SS.do('''
                    get 'tests/files/doc1.xml'
                    return &'//span[@class="c@stom"][1]'
                    ''')
        self.assertEqual(out, 'mango')
        
    def test_path29(self):
        ''' & search span whith any attribute equals "third" '''
        out = SS.do('''
                    get 'tests/files/doc1.xml'
                    return &'//span[@*=third][1]'
                    ''')
        self.assertEqual(out, 'mango')
        
    def test_path30(self):
        ''' & missing name selector, fails '''
        self.assertRaises(ParsingException, SS.do,
                    '''
                    get 'tests/files/doc1.xml'
                    return &'@missing'
                    ''')
        
    def test_path31(self):
        ''' missplaced alternate path (|), fails '''
        self.assertRaises(ParsingException, SS.do,
                    '''
                    get 'tests/files/doc1.xml'
                    return &'|/root/div/span[1]'
                    ''')
        self.assertRaises(ParsingException, SS.do,
                    '''
                    get 'tests/files/doc1.xml'
                    return &'/root/div/span|'
                    ''')
        self.assertRaises(ParsingException, SS.do,
                    '''
                    get 'tests/files/doc1.xml'
                    return &'/root/div[@name=|]/span[1]'
                    ''')
        
        self.assertRaises(ParsingException, SS.do,
                    '''
                    get 'tests/files/doc1.xml'
                    return &'/root/div[|@name]/span'
                    ''')
        
    def test_path32(self):
        ''' & get value using alternate path, second works  '''
        out = SS.do('''
                    get 'tests/files/doc1.xml'
                    return &'/root/div/p[1]|root/div/span[1]'
                    ''')
        self.assertEqual(out, 'apple')
        
    def test_path33(self):
        ''' & get value using alternate path, both work, returns first  '''
        out = SS.do('''
                    get 'tests/files/doc1.xml'
                    return &'/root/div/span[@name][1]|root/p[1]'
                    ''')
        self.assertEqual(out, 'apple')
        
    def test_path34(self):
        ''' & skip to and get value using alternate path, third works '''
        out = SS.do('''
                    get 'tests/files/doc1.xml'
                    skip &'//table|/div/span[@name]|/root/div/span[2]'
                    return &'.'                    
                    ''')
        self.assertEqual(out, 'orange')
        
    def test_path35(self):
        ''' & select all names with one expression '''
        out = SS.do('''
                    get 'tests/files/doc1.xml'
                    return &'/root/div/span'       
                    ''')
        self.assertEqual(out, ['apple', 'orange', 'mango'])
        
    def test_path36(self):
        ''' & select all attribute values with one expression '''
        out = SS.do('''
                    get 'tests/files/doc1.xml'
                    return &'/root/div/span@name'
                    ''')
        self.assertEqual(out, ['first', 'second', 'third'])
                
    def test_path37(self):
        ''' & enumerate selected name values '''
        out = SS.do('''
                    get 'tests/files/doc1.xml'
                    r = ''
                    for v in &'/root/div/span':
                        r = r + v + '\n'
                    return r
                    ''')
        self.assertEqual(out, 'apple\norange\nmango\n')
        
    def test_path38(self):
        ''' & empty results returns as empty list '''
        out = SS.do('''
                    get 'tests/files/doc1.xml'
                    return &'/root/div/meta'                    
                    ''')
        self.assertEqual(out, [])
        
    def test_path39(self):
        ''' document is searched for the tag name, if path starts from word char (not slash)'''
        out = SS.do('''
                    get 'tests/files/doc1.xml'
                    return &'span/'
                    ''')
        self.assertEqual(out, ['apple', 'orange', 'mango'])
        
    def test_path40(self):
        ''' get children tags after implicit search '''
        out = SS.do('''
                    get 'tests/files/doc1.xml'
                    return &'div/span[2]'
                    ''')
        self.assertEqual(out, 'orange')