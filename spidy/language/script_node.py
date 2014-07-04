
''' Script block parsing and evaluation. '''

import syntax

from spidy.common import *
from nodes import Node
from return_node import ReturnNode

# (script_block)*
class ScriptNode(Node):
    ''' Statements container node. Evaluates statements one by one. '''
    
    _statements = None
    
    def __init__(self, context):
        super(ScriptNode, self).__init__(context)
        self._statements = []
    
    def get_statements(self):
        return self._statements
    
    def set_statements(self, statements):
        self._statements = statements
        
    def evaluate(self):
        log.debug(self._id, 'ScriptNode: starting script frame')
        self._context.frame_start()
        
        for s in self._statements:
            s.evaluate()
            
            # check flags
            flags = self._context.get_flags()            
            if (flags & ExecutionFlags.HALT
               |flags & ExecutionFlags.BREAK
               |flags & ExecutionFlags.CONTINUE):
                break
        
        log.debug(self._id, 'ScriptNode: ending script frame')
        self._context.frame_end()
        
    def __str__(self):
        string = ''
        for s in self.get_statements():
            string += str(s) + syntax.LINEFEED
        return string