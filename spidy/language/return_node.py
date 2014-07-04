
''' ``return`` statement parsing and evaluation. '''

import syntax
import exp_parser

from spidy.common import *
from nodes import Node
from nodes import NoneNode

class ReturnNode(Node):
    '''
    Terminates script execution and returns immediately. If expression is specified,
    evaluates it and returns result.
    
    Example::
    
        return
        
    Or::
    
        return (2 + 2) == 4
    '''
    
    _return_exp = None
    
    def get_return_exp(self):
        return self._return_exp
    
    def set_return_exp(self, return_exp):
        self._return_exp = return_exp
        
    def evaluate(self):
        log.debug(self._id, 'PushNode: evaluating')
        out = self._return_exp.evaluate()                        
        self._context.set_return(out)
        self._context.set_flags(self._context.get_flags() | ExecutionFlags.HALT)

    def parse(self, line_num):
        log.debug(self._id, 'PushNode: parsing')
        self._sline = self._context.get_script()[line_num]
        line = self._sline.string
        idx = line.index(syntax.OP_RETURN) + len(syntax.OP_RETURN)
        exp = line[idx:].strip()        
        if exp != '':        
            self._return_exp = exp_parser.parse_expression(self._context, line_num, exp)
        else:
            self._return_exp = NoneNode()

    def __str__(self):
        string = syntax.OP_RETURN
        if self._return_exp != None:
            string += syntax.WHITESPACE + str(self._return_exp)
        return string 