
''' 'log' statement parsing and evaluation. '''

import syntax
import exp_parser 

from spidy.common import *
from nodes import Node

class LogNode(Node):
    '''
    Logs string to file or *stdout*, ignores empty strings.
    
    Example::
    
        log 'loading next page'
        
    .. note:: The statement logs messages as *INFO*.
    '''

    _string = None
    
    def get_string(self):
        return self._string
    
    def set_string(self, string):
        self._string = string

    def evaluate(self):
        log.debug(self._id, 'LogNode: evaluating')
        s = self._string.evaluate()
        if s != None and isinstance(s, basestring) and len(s) > 0:
            log.info(self._id, s)
        else:
            log.warning(self._id, 'LogNode: attempt to write empty message to log, line {0}'.format(self._sline.number+1))

    def parse(self, line_num):
        log.debug(self._id, 'LogNode: parsing')
        self._sline = self._context.get_script()[line_num]
        line = self._sline.string
        idx = line.index(syntax.OP_LOG) + len(syntax.OP_LOG)        
        self._string = exp_parser.parse_expression(self._context, line_num, line[idx:])
        
    def __str__(self):
        return syntax.OP_LOG + syntax.WHITESPACE + str(self._string)