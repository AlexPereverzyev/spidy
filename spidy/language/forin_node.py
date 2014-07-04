
''' 'for...in' statement parsing and evaluation. '''

import collections 
import syntax
import exp_parser

from spidy.common import *
from tokenizer import *
from nodes import Node

class ForInNode(Node):
    '''
    Typical *for...in* statement, iterates through collection of items.
    
    For example::
    
        for item in items:
            lst << item
    '''
    
    _ident = None
    _source = None
    _body = None
    
    def get_ident(self):
        return self._ident
    
    def set_ident(self, ident):
        self._ident = ident
    
    def get_source(self):
        return self._source
    
    def set_source(self, source):
        self._source = source
    
    def get_body(self):
        return self._body
    
    def set_body(self, body):
        self._body = body
    
    def evaluate(self):
        id = self._context.get_id()
        log.debug(self._id, 'ForInNode: parsing')
        validate_eval(self._id, self._sline, not self._context.is_bound(self._ident),
            'ForInNode: loop variable is already defined')

        lst = self._source.evaluate()
        validate_eval(self._id, self._sline, isinstance(lst, collections.Iterable) and not isinstance(lst, basestring),
            'ForInNode: for-in source should be a collection')
        
        self._context.bind_var(self._ident, None)
        
        for item in lst:
            self._context.set_var(self._ident, item)
            self._body.evaluate()
            
            # check flags
            flags = self._context.get_flags() & ~ExecutionFlags.CONTINUE
            self._context.set_flags(flags)
            if flags & ExecutionFlags.BREAK:
                self._context.set_flags(flags & ~ExecutionFlags.BREAK)
                break
            
        self._context.unbind_var(self._ident)

    def parse(self, line_num):        
        log.debug(self._id, 'ForInNode: parsing')        
        lines = self._context.get_script()       
        self._sline = lines[line_num]
        line = self._sline.string
        
        # check if we have indented 'for...in' block
        validate(self._id, self._sline, line_num + 1 < len(lines),
            'ForInNode: missing script block after ' + syntax.OP_FOR)
        validate(self._id, self._sline, syntax.is_indented_block(lines[line_num:line_num + 2]),
            'ForInNode: expected an indented block after ' + syntax.OP_FOR)
        validate(self._id, self._sline, line.rstrip().endswith(syntax.COLON),
            'ForInNode: expected ' + syntax.COLON + ' after ' + syntax.OP_FOR + ' source')
                
        # parse 'for...in' line
        idx = line.index(syntax.OP_FOR) + len(syntax.OP_FOR)
        l = line[idx:]
        idx = skip_space(l)
        l = l[idx:]
        ident_idx = skip_token(l)

        # set loop identity first
        ident = l[:ident_idx]
        validate(self._id, self._sline, syntax.is_var_name(ident), 'ForInNode: invalid loop variable name')            
        self._ident = ident
        
        # check 'in' operator
        l = l[ident_idx:]
        idx = skip_space(l)
        l = l[idx:]
        in_idx = skip_token(l)        
        validate(self._id, self._sline, l[:in_idx] == syntax.OP_IN, 'ForInNode: invalid syntax')

        # now parse source
        l = l[in_idx:]
        idx = skip_space(l)
        source = l[idx:].replace(syntax.COLON, '').strip()
        self._source = exp_parser.parse_expression(self._context, line_num, source)
        
    def __str__(self):
        string = (syntax.OP_FOR + syntax.WHITESPACE + self._ident + syntax.WHITESPACE +
                  syntax.OP_IN + syntax.WHITESPACE + str(self._source) + syntax.COLON + syntax.LINEFEED)
        
        body_lines = str(self._body).strip().split('\n')
        for i in range(len(body_lines)):
            body_lines[i] = '\t' + body_lines[i]            
        string += '\n'.join(body_lines)
        
        return string