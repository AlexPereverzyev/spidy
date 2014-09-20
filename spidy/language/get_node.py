
''' 'get' statement parsing and evaluation. '''

import syntax
import exp_parser

from spidy.common import *
from spidy.document import *
from nodes import Node

class GetNode(Node):
    '''
    Loads documnet specified by URL string either from Web or local file system.
    The document becomes main source of data for the whole execution context and
    ``&``, ``skip``, ``traverse`` operators and statements::
        
        get 'www.someresource.com/document.html'
    
    To specify expected document format use ``as`` operator::
    
        get 'www.someresource.com/index' as html
        
    To specify headers, end statement by ``:`` and add headers as indented block::
        
        get 'www.someresource.com/index' as html:
            User-agent: 'Firefox/25.0'
            
    When loading from Web resource, default headers are::
    
        Accept          : 'text/html,application/xhtml+xml,application/xml',
        Accept-Language : 'en-US,en;q=0.5',
        Connection      : 'keep-alive',
        Cache-Control   : 'max-age=0'
    '''
    
    _url = None
    _doc_type = DocType.UNKNOWN
    _headers = None

    def __str__(self):
        string = syntax.OP_GET + syntax.WHITESPACE + str(self._url)
        if self._doc_type != DocType.UNKNOWN:
            string += syntax.WHITESPACE + syntax.OP_AS + syntax.WHITESPACE + self._doc_type
            
        if self._headers != None:
            string += syntax.COLON + syntax.LINEFEED
            
            header_lines = str(self._headers).strip().split('\n')
            for i in range(len(header_lines)):
                header_lines[i] = '\t' + header_lines[i]            
            string += '\n'.join(header_lines)
            
        return string
    
    def has_headers(self, line_num):
        ''' Returns True if 'get' statement should iclude headers. '''
        return self._context.get_script()[line_num].string.rstrip().endswith(syntax.COLON)
    
    def get_url(self):
        return self._url
    
    def set_url(self, _url):
        self._url = _url
        
    def get_doc_type(self):
        return self._doc_type

    def set_doc_type(self, file_type):
        self._doc_type = doc_type

    def get_headers(self):
        return self._headers
    
    def set_headers(self, _headers):
        self._headers = _headers
        
    def evaluate(self):
        log.debug(self._id, 'GetNode: evaluating')
        url = self._url.evaluate()
        doc_loader = DocLoader()

        # prepare headers 
        headers = None
        if self._headers != None:
            headers = self._headers.evaluate()

        # never raise, unless doc format is unknown
        log.debug(self._id, 'GetNode: loading document {0}'.format(url))
        try:
            doc_loader.load(url, self._doc_type, headers)
            log.debug(self._id, 'GetNode: loaded document')
        except DocumentException as de:
            log.critical(self._id, str(de))
            raise de
        except Exception as e:
            log.error(self._id, 'GetNode: load document error: {0}'.format(str(e)))
        
        # set document context
        self._context.set_doc_type(doc_loader.get_doc_type())
        self._context.set_doc_raw(doc_loader.get_doc_raw())
        self._context.set_doc(doc_loader.get_doc())        
        self._context.set_doc_cursor(None)                       
        
    def parse(self, line_num):
        log.debug(self._id, 'GetNode: parsing')
        lines = self._context.get_script()
        self._sline = lines[line_num]
        line = self._sline.string
        idx = line.index(syntax.OP_GET) + len(syntax.OP_GET)
        url_exp = line[idx:].strip()
        
        # check if headers block present
        if url_exp.endswith(syntax.COLON):            
            url_exp = url_exp[:-1].rstrip()            
            
            validate(self._id, self._sline, line_num + 1 < len(lines),
                'GetNode: missing headers block after ' + syntax.COLON)
            validate(self._id, self._sline, syntax.is_indented_block(lines[line_num:line_num + 2]),
                'GetNode: expected an indented headers block after ' + syntax.COLON)
        
        # parse URL
        ep = exp_parser.ExpressionParser(self._context, line_num)
        self._url = ep.parse(url_exp)
        
        # try to parse doc type
        stop_word = ep.get_stop_word()        
        if stop_word != '':
            validate(self._id, self._sline, stop_word == syntax.OP_AS, 'GetNode: invalid syntax')
            
            doc_type_idx = ep.get_stop_idx() + len(stop_word)
            doc_type = url_exp[doc_type_idx:].strip().upper()
            
            if doc_type != '':
                validate(self._id, self._sline,
                         doc_type == DocType.TXT
                      or doc_type == DocType.XML
                      or doc_type == DocType.HTML
                      or doc_type == DocType.JSON,
                        'GetNode: invalid document type')
                self._doc_type = doc_type