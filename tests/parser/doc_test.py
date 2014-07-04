
import exceptions
import unittest

from spidy.document.txt_transform import TxtTransform
from spidy.document.xml_transform import XmlTransform
from spidy.document.html_transform import HtmlTransform
from spidy.document.html_form import HtmlForm
from spidy.document.json_transform import JsonTransform

class DocTest(unittest.TestCase):    
    
    def test_parse_html1(self):
        ''' parse plain HTML, close open tags '''
        
        html_string = '''
            <html>
                <head>
                    <meta>
                    <link href="test/url">
                    <link href="test/url">
                    <script>alert('hello!')</script>
                    <link href="test/url">                    
                </head>
                <body>
                    <div id="main">
                        <span>this </span>
                        <span>is </span>
                        <span>plain </span>
                        <br>
                        <div>
                            <img src="empty">
                        </div>
                        <span>HTML!</span>
                        <br>
                    </div>
                    <div id="footer">
                        <table/>
                    </div>
                </body>
            </html>
        '''
        ht = HtmlTransform()
        doc = ht.perform(html_string)
        
        hf = HtmlForm()
        hf.refactor(doc)
        
        doc_string = ''
        for r in doc:
            doc_string += str(r)
        
        self.assertEqual(doc_string, '''html[1]\n-head[1]\n++meta[1]\n++link[1]\n++link[2]\n--script[1]\n++link[3]\n-body[1]\n--div[1]\n---span[1]\n---span[2]\n---span[3]\n+++br[1]\n---div[1]\n++++img[1]\n---span[4]\n+++br[2]\n--div[2]\n---table[1]\n----tbody[1]\n''')
        
    def test_parse_html2(self):
        ''' parse plain HTML, close open tr/td tags '''
        
        html_string = '''
            <html>
                <body>
                    <div>Hello broken table</div>
                    <table>
                        <tr>
                            <td>
                                <span>open cell</span>
                                <span>same open cell</span>
                        <tr>
                            <td>
                                <span>normal cell 1</span>
                            </td>
                            <tr>empty</tr>
                            <span>missed</span>
                        </tr>
                </body>
            </html>
        '''
        ht = HtmlTransform()
        doc = ht.perform(html_string)
        
        hf = HtmlForm()
        hf.refactor(doc)
        
        doc_string = ''
        for r in doc:
            doc_string += str(r)
        
        self.assertEqual(doc_string, '''html[1]\n-body[1]\n--div[1]\n--span[1]\n++table[1]\n---tbody[1]\n++++tr[1]\n+++++td[1]\n------span[1]\n------span[2]\n----tr[2]\n-----td[1]\n------span[1]\n----tr[3]\n''')
        
    def test_parse_html3(self):
        ''' parse plain HTML, rename tr/td tags w/o table to span '''
        
        html_string = '''
            <html>    
                <tr>
                    <td>
                      <span id="row">content</span>
                    </td>
                </tr>
            </html>
            '''
        ht = HtmlTransform()
        doc = ht.perform(html_string)
        
        hf = HtmlForm()
        hf.refactor(doc)
        
        doc_string = ''
        for r in doc:
            doc_string += str(r)
        
        self.assertEqual(doc_string, '''html[1]\n-span[1]\n--span[1]\n---span[1]\n''')
        
    def test_parse_json1(self):
        ''' parse plain JSON to multi-root document '''
        
        json_string = '''
        [
            [
                "plain_string",
                4234,
                [2423,432423]
            ],
            {
                "id":10132,
                "name": "dummy",
                "child": [
                    {
                        "id":13642,
                        "name": "dummy_child1"
                    },
                    {
                        "id":1343242,
                        "name": "dummy_child2"
                    }                
                ]
            },
            {
                "key": "a key",
                "value": 1
            }
        ]
        '''
        jt = JsonTransform()
        doc = jt.perform(json_string)
        
        doc_string = ''
        for r in doc:
            doc_string += str(r)
        
        self.assertEqual(doc_string,
'''tag[1]
-tag[1]
-tag[2]
-tag[3]
--tag[1]
--tag[2]
tag[2]
-child[1]
-child[2]
tag[3]
''')