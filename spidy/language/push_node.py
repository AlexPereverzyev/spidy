
''' Push ``<<`` operator evaluation. '''

import collections
import syntax

from spidy.common import *
from nodes import BinaryNode
from set_node import SetNode

class PushNode(SetNode):
    '''
    Appends item to list. Optionally, inserts item at specified position, if list
    index is specified.
    
    Example, push to list::
    
        lst << 5
        
    Insert at certain index::
    
        lst[5] << 5
    '''
    
    def set_left(self, left):        
        self._left = left
        if self._left != None:
            self._left.set_parent(self)
    
    def evaluate(self):        
        log.debug(self._id, 'PushNode: evaluating')        
        value = self._right.evaluate()
        
        # insert value to the list
        if isinstance(self._left, BinaryNode) and self._left.get_op() == syntax.OP_INDEXER:
            lst = self._left.get_left().evaluate()
            index = self._left.get_right().evaluate()

            validate_eval(self._id, self._sline, isinstance(lst, collections.Iterable) and not isinstance(lst, basestring),
                'PushNode: only pop from list or indexer is allowed')
            validate_eval(self._id, self._sline, index <= len(lst),
                'PushNode: index out of range')
            
            lst.insert(index, value)
            
        # append value to the list
        else:
            lst = self._left.evaluate()
            
            validate_eval(self._id, self._sline, isinstance(lst, collections.Iterable) and not isinstance(lst, basestring),
                'PushNode: only pop from list or indexer is allowed')
            
            lst.append(value)
                
        return value
    
    def __str__(self):        
        return str(self._left) + syntax.WHITESPACE + syntax.OP_PUSH + syntax.WHITESPACE + str(self._right)