
''' Contains node factory routines to create plain value or unray/binary nodes. '''

__all__ = ['make_unary_node', 'make_binary_node', 'make_value_node']

from syntax import *
from spidy.common.sniff import *

from nodes import *
from set_node import SetNode
from pop_node import PopNode
from push_node import PushNode
from path_node import PathNode
from regex_node import RegexNode

def make_unary_node(operator, context, line_num):
    ''' Creates a unary node corresponding to specified operator and
        initializes it with specified execution context. '''
    node = None
    if operator == OP_PATH:
        node = PathNode(context)
    else:
        node = UnaryNode(context)
    node.set_op(
        to_unary(operator))
    node.parse(line_num)
    return node

def make_binary_node(operator, context, line_num):
    ''' Creates a binary node corresponding to specified operator and
        initializes it with specified execution context. '''
    if operator == OP_SET:
        node = SetNode(context)
    elif operator == OP_POP:
        node = PopNode(context)
    elif operator == OP_PUSH:
        node = PushNode(context)
    elif operator == OP_LIST:
        node = ListNode(context)
    elif operator == OP_REGEX:
        node = RegexNode(context)
    else:
        node = BinaryNode(context)
    if operator != OP_LIST:
        node.set_op(operator)
    node.parse(line_num)
    return node
    
def make_value_node(value, context, line_num):
    ''' Creates a plain value node from specified value and initializes it with
        specified execution context. '''
    node = None
    if is_none(value):
        node = NoneNode(context)
    elif is_bool_const(value):
        node = BoolNode(context)
    elif is_string_const(value):
        node = StringNode(context)
    elif is_number_const(value):
        node = NumberNode(context)        
    elif is_var_name(value):
        node = VarNode(context)     
    if node != None:
        node.set_value(value)
        node.parse(line_num)
    return node