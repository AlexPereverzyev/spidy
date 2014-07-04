
''' Set ``=`` operator evaluation. '''

import collections
import syntax

from spidy.common import *
from nodes import BinaryNode
from nodes import VarNode

class SetNode(BinaryNode):
    '''
    Typical assignment operator, sets value to variable or list item.
    
    Example::
    
        a = 10
    
    Set list item::
    
        lst[0] = 10    
    '''
        
    def set_left(self, left):
        validate(self._id, self._sline, isinstance(left, VarNode) or
                 isinstance(left, BinaryNode) and left.get_op() == syntax.OP_INDEXER,
            'SetNode: only assignment to variable or indexer is allowed')
        
        super(SetNode, self).set_left(left)
        
    def evaluate(self):
        log.debug(self._id, 'SetNode: evaluating')
        value = self._right.evaluate()
        
        if isinstance(self._left, VarNode):
            varname = self._left.get_value()
            self._context.make_var(varname, value)
            
        else: # indexer            
            lst = self._left.get_left().evaluate()
            index = self._left.get_right().evaluate()
            
            validate_eval(self._id, self._sline, isinstance(lst, collections.Iterable),
                'SetNode: only lists can be indexed')
                
            lst[index] = value

        return value
    
    def __str__(self):        
        return str(self._left) + syntax.WHITESPACE + syntax.OP_SET + syntax.WHITESPACE + str(self._right)