
''' Header and headers block statement parsing and evaluation. '''

import syntax
import exp_parser

from spidy.common import *
from nodes import ValueNode
from script_node import ScriptNode

# ident: string
class HeaderNode(ValueNode):
    ''' Header data statement node. Works together with *get* command. ''' 
    
    _name = None
    
    def __str__(self):
        return self._name + syntax.COLON + syntax.WHITESPACE + str(self._value)
        
    def get_name(self):
        return self._name
    
    def set_name(self, name):
        self._name = name
    
    def parse(self, line_num):
        log.debug(self._id, 'HeaderNode: parsing')
        self._sline = self._context.get_script()[line_num]
        line = self._sline.string.lstrip()
        ident_idx = line.index(syntax.COLON)
        self._name = line[:ident_idx]        
        validate(self._id, self._sline, syntax.is_header_name(self._name), 'HeaderNode: invalid header name')
        value_exp = line[ident_idx+1:].strip()
        self._value = exp_parser.parse_expression(self._context, line_num, value_exp)
        
    def evaluate(self):
        log.debug(self._id, 'HeaderNode: evaluating')
        value = self._value.evaluate()
        return value

# (headers_block)*
class HeadersNode(ScriptNode):
    ''' Speacial header statements container, returns headers dictionary on evaluate. '''
    
    def __str__(self):
        string = ''
        for s in self.get_statements():
            string += str(s) + syntax.LINEFEED
        return string

    def evaluate(self):
        log.debug(self._id, 'HeadersNode: evaluating headers')
        
        headers = {}
        for h in self._statements:
            v = h.evaluate()
            validate_eval(self._id, self._sline, v != None, 'HeadersNode: header value should be specified')
            headers[h.get_name()] = v
            
        log.debug(self._id, 'HeadersNode: finished evaluating headers')
        return headers