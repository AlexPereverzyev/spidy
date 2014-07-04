
''' Inline expression statement parsing and evaluation. '''

import exp_parser

from spidy.common import *
from nodes import Node

class InlineNode(Node):
    ''' Simply wraps inline expressions. '''
    
    _inline = None
        
    def get_inline(self):
        return self._inline
    
    def parse(self, line_num):
        log.debug(self._id, 'InlineNode: parsing')
        self._sline = self._context.get_script()[line_num]
        self._inline = exp_parser.parse_expression(self._context, line_num, self._sline.string)
        return self._inline
    
    def evaluate(self):
        log.debug(self._id, 'InlineNode: evaluating')
        return self._inline.evaluate()
    
    def __str__(self):
        return str(self._inline)