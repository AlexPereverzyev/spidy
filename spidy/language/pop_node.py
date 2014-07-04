
''' Pop ``>>`` operator evaluation. '''

import collections
import syntax

from spidy.common import *
from nodes import BinaryNode
from nodes import VarNode
from set_node import SetNode

class PopNode(SetNode):
    '''
    Pops item for list. Optionally, pops item to specified variable. If list
    index is specified - removes item from list.
    
    Example, pop from list::
    
        lst >>
        
    Pop to variable::
    
        lst >> current
        
    Remove first item from list::
    
        lst[0] >> first    
    '''
    
    def set_left(self, left):
        self._left = left
        if self._left != None:
            self._left.set_parent(self)
    
    def set_right(self, right):
        validate(self._id, self._sline, right == None or
                 isinstance(right, VarNode) or
                 isinstance(right, BinaryNode) and right.get_op() == syntax.OP_INDEXER,
            'PopNode: only pop to list or indexer is allowed')
        
        super(PopNode, self).set_right(right)
    
    def evaluate(self):
        log.debug(self._id, 'PopNode: evaluating')        
        lst = None
        index = -1
        # pop item at index
        if isinstance(self._left, BinaryNode) and self._left.get_op() == syntax.OP_INDEXER:
            lst = self._left.get_left().evaluate()
            index = int(self._left.get_right().evaluate())
            
            validate_eval(self._id, self._sline, isinstance(lst, collections.Iterable) and not isinstance(lst, basestring),
                'PopNode: only pop from list or indexer is allowed')
            validate_eval(self._id, self._sline, index < len(lst),
                'PopNode: index out of range')

        # pop last item
        else:
            lst = self._left.evaluate()
            
            validate_eval(self._id, self._sline, isinstance(lst, collections.Iterable) and not isinstance(lst, basestring),
                'PopNode: only pop from list or indexer is allowed')
            validate_eval(self._id, self._sline, len(lst) > 0,
                'PopNode: pop from empty list')
            
        value = lst.pop(index)
            
        # now try to set the output variable
        if self._right != None:
            if isinstance(self._right, VarNode):
                varname = self._right.get_value()
                self._context.make_var(varname, value)
                
            else: # indexer 
                lst = self._right.get_left().evaluate()
                index = self._right.get_right().evaluate()
                
                validate_eval(self._id, self._sline, isinstance(lst, collections.Iterable) and not isinstance(lst, basestring),
                    'PopNode: only pop from list or indexer is allowed')
                validate_eval(self._id, self._sline, index < len(lst),
                    'PopNode: index out of range')
                
                lst[index] = value

        return value
    
    def __str__(self):        
        string = str(self._left) + syntax.WHITESPACE + syntax.OP_POP
        if self._right != None:
            string += syntax.WHITESPACE + str(self._right)
        return string