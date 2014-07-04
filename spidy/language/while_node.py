
''' ``while`` statement parsing and evaluation. '''

import collections
import syntax
import exp_parser

from spidy.common import *
from tokenizer import *
from nodes import Node

class WhileNode(Node):
    '''
    Typical *while* loop. Loops until expression is True. If expression evaluates
    to list, loops until it has items (like in Python)
    
    Example::
    
        host = 'www.cars.com/search'
        while lst:
            lst >> next
            get (host + next) as json                        
    '''

    _condition = None
    _body = None

    def get_condition(self):
        return self._condition
    
    def set_condition(self, cond):
        self._condition = cond
    
    def get_body(self):
        return self._body
    
    def set_body(self, body):
        self._body = body
    
    def evaluate(self):
        log.debug(self._id, 'WhileNode: evaluating')
                
        while self._condition.evaluate():                        
            self._body.evaluate()
            
            # check flags
            flags = self._context.get_flags() & ~ExecutionFlags.CONTINUE
            self._context.set_flags(flags)
            if flags & ExecutionFlags.BREAK:
                self._context.set_flags(flags & ~ExecutionFlags.BREAK)
                break
            
    def parse(self, line_num):
        log.debug(self._id, 'WhileNode: parsing')
        lines = self._context.get_script()
        self._sline = lines[line_num]
        line = self._sline.string
        
        # check if we have indented 'while' block
        validate(self._id, self._sline, line_num + 1 < len(lines),
            'WhileNode: missing script block after ' + syntax.OP_WHILE)
        validate(self._id, self._sline, syntax.is_indented_block(lines[line_num:line_num + 2]),
            'WhileNode: expected an indented block after ' + syntax.OP_WHILE)
        validate(self._id, self._sline, line.rstrip().endswith(syntax.COLON),
            'WhileNode: expected ' + syntax.COLON + ' after ' + syntax.OP_WHILE + ' condition')
                
        # parse 'while' line
        idx = line.index(syntax.OP_WHILE) + len(syntax.OP_WHILE)
        l = line[idx:]
        idx = skip_space(l)
        
        # set condition
        cond = l[idx:].replace(syntax.COLON, '').strip()
        self._condition = exp_parser.parse_expression(self._context, line_num, cond)
        
    def __str__(self):
        string = (syntax.OP_WHILE + syntax.WHITESPACE + str(self._condition) + syntax.COLON + '\n')
        
        body_lines = str(self._body).strip().split('\n')
        for i in range(len(body_lines)):
            body_lines[i] = '\t' + body_lines[i]            
        string += '\n'.join(body_lines)
        
        return string