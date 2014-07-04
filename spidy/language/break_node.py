
''' 'break' statement parsing and evaluation. '''

import syntax

from spidy.common import *
from nodes import Node

class BreakNode(Node):
    '''
    Typical *break loop* statement.
    Breaks ``for``, ``while`` and ``traverse`` statements.
    '''

    def evaluate(self):        
        log.debug(self._id, 'BreakNode: evaluating')
        flags = self._context.get_flags()
        self._context.set_flags(flags | ExecutionFlags.BREAK)

    def parse(self, line_num):
        log.debug(self._id, 'BreakNode: parsing')
        self._sline = self._context.get_script()[line_num]
        line = self._sline.string
        idx = line.index(syntax.OP_BREAK) + len(syntax.OP_BREAK)        
        validate(self._id, self._sline, line[idx:].strip() == '', 'BreakNode: invalid syntax')
        
    def __str__(self):
        return syntax.OP_BREAK