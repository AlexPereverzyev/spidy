
''' 'continue' statement parsing and evaluation. '''

import syntax

from spidy.common import *
from nodes import Node

class ContinueNode(Node):
    '''
    Typical *continue loop* statement.
    Breaks ``for``, ``while`` and ``traverse`` statements.
    '''
    
    def evaluate(self):
        log.debug(self._id, 'ContinueNode: evaluating')
        flags = self._context.get_flags()
        self._context.set_flags(flags | ExecutionFlags.CONTINUE)
    
    def parse(self, line_num):
        log.debug(self._id, 'ContinueNode: parsing')
        self._sline = self._context.get_script()[line_num]
        line = self._sline.string
        idx = line.index(syntax.OP_CONTINUE) + len(syntax.OP_CONTINUE)
        validate(self._id, self._sline, line[idx:].strip() == '', 'ContinueNode: invalid syntax')
        
    def __str__(self):
        return syntax.OP_CONTINUE