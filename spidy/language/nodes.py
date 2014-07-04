
''' Contains primitive syntax nodes used to build Spidy syntax trees. '''

from syntax import *
from spidy.common import *

class Node(object):
    ''' Syntax tree node base class. '''
    
    _context = None
    _id = None
    _sline = None
    _parent = None
    
    def __init__(self, context):
        self._context = context
        self._id = self._context.get_id()
        
    def get_context(self):
        return self._context
    
    def get_script_line(self):
        return self._sline
    
    def set_script_line(self, sline):
        self._sline = sline
    
    def parse(self, line_num):
        self._sline = self._context.get_script()[line_num]
    
    def get_parent(self):
        return self._parent
    
    def set_parent(self, parent):
        self._parent = parent
        
    def evaluate(self):
        pass
    
    def to_metrics(self):
        pass
    
class ListNode(Node):
    ''' Syntax tree list node, contains list of item nodes. '''
    
    _items = None
    
    def __init__(self, context):
        super(ListNode, self).__init__(context)
        self._items = []
        
    def get_items(self):
        return self._items
    
    def set_items(self, items):
        self._items = items
        
    def evaluate(self):
        result = []
        for item in self._items:
            r = item.evaluate()
            result.append(r)
        return result
    
    def __str__(self):
        result = LEFT_SQUARE
        l = len(self._items)
        for i in range(l):
            item = self._items[i]
            s = str(item)
            result += s
            if i != l - 1:
                result += COMMA + WHITESPACE 
        result += RIGHT_SQUARE
        return result

class UnaryNode(Node):
    ''' Syntax tree node which represents unary operator, contains one operand. '''
    
    _op = None
    _right = None
    
    def get_op(self):
        return self._op
    
    def set_op(self, op):
        self._op = op
        
    def get_right(self):
        return self._right
    
    def set_right(self, right):
        self._right = right
        if self._right != None:
            self._right.set_parent(self)

    def evaluate(self):
        r = self._right.evaluate()        
        try:
            if self._op == OP_UNARY_MINUS:
                return -r
            elif self._op == OP_UNARY_PLUS:
                return r
            elif self._op == OP_NOT:
                return not r
            elif self._op == OP_PATH:
                return r
            elif self._op == OP_CONVERT_TO_STR:
                if isinstance(r, basestring):
                    return r                
                return str(r)
            elif self._op == OP_CONVERT_TO_NUM:
                if isinstance(r, int) or isinstance(r, float):
                    return r
                if DOT in r:
                    return float(r)
                return int(r)        
            else:
                raise_eval(self._id, self._sline, 'UnaryNode: unknown operator')
                
        except EvaluationException as ee:
            raise ee
        except Exception as e:
            raise_eval(self._id, self._sline, 'UnaryNode: evaluation failed')
        
    def __str__(self):
        op = self._op.replace(MARK_UNARY, EMPTY)
        return LEFT_PAREN + op + WHITESPACE + str(self._right) + RIGHT_PAREN

class BinaryNode(UnaryNode):
    ''' Syntax tree node which represents binary operator, contains two operands. '''
    
    _left = None
    
    def get_left(self):
        return self._left
    
    def set_left(self, left):
        self._left = left
        if self._left != None:
            self._left.set_parent(self)

    def evaluate(self):
        l = self._left.evaluate()
        if self._op == OP_AND and not l or self._op == OP_OR and l:
            return l
        r = self._right.evaluate()
        try:
            if self._op == OP_DIVIDE:
                return l / r
            elif self._op == OP_MULT:
                return l * r
            elif self._op == OP_PLUS:
                return l + r
            elif self._op == OP_MINUS:
                return l - r
            elif self._op == OP_AND:
                return l and r        
            elif self._op == OP_OR:
                return l or r
            elif self._op == OP_IN:
                # always compare strings in lowercase
                if isinstance(l, basestring) and isinstance(r, basestring):
                    l = l.lower()
                    r = r.lower()
                return l in r
            elif self._op == OP_EQUALS:
                return l == r
            elif self._op == OP_NOT_EQUALS:
                return l != r
            elif self._op == OP_LESS:
                return l < r
            elif self._op == OP_LESS_OR_EQUALS:
                return l <= r
            elif self._op == OP_GREATER:
                return l > r
            elif self._op == OP_GREATER_OR_EQUALS:
                return l >= r
            elif self._op == OP_INDEXER:
                return l[r]
            else:
                raise_eval(self._id, self._sline, 'BinaryNode: unknown operator')
                
        except EvaluationException as ee:
            raise ee
        except Exception as e:
            raise_eval(self._id, self._sline, 'BinaryNode: evaluation failed')
        
    def __str__(self):
        if self._op != OP_INDEXER:
            return LEFT_PAREN + str(self._left) + WHITESPACE + self._op + WHITESPACE + str(self._right) + RIGHT_PAREN
        else:
            return str(self._left) + LEFT_SQUARE + str(self._right) + RIGHT_SQUARE
    
class ValueNode(Node):
    ''' Syntax tree node which holds primitive value. '''
    
    _value = None
    
    def get_value(self):
        return self._value
    
    def set_value(self, value):
        self._value = value
        
    def evaluate(self):
        pass
    
    def __str__(self):
        return self._value
        
class NoneNode(ValueNode):
    ''' Syntax tree node representing None. '''
    pass
                
class VarNode(ValueNode):
    ''' Syntax tree node which represents variable. '''
    
    def evaluate(self):        
        validate_eval(self._id, self._sline, self._context.is_bound(self._value),
            'VarNode: variable "{0}" is not defined'.format(self._value))
        return self._context.get_var(self._value)

class BoolNode(ValueNode):
    ''' Syntax tree node which represents boolean value. '''
    
    def evaluate(self):
        return self._value == 'True'
        
class NumberNode(ValueNode):
    ''' Syntax tree node which represents number (int or float) value. '''
    
    def evaluate(self):
        if DOT in self._value:
            return float(self._value)
        return int(self._value)
    
class StringNode(ValueNode):
    ''' Syntax tree node which represents string value. '''
        
    def evaluate(self):
        return self._value[1:-1]