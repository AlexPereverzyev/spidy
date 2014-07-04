
''' Spidy expressions prasing routines and classes. '''

__all__ = ['parse_expression', 'ExpressionParser']

import tokenizer

from syntax import *
from spidy.common import *
from spidy.common.sniff import *

from nodes import *
from set_node import SetNode
from pop_node import PopNode
from push_node import PushNode
from path_node import PathNode

def parse_expression(context, lnum, expression):
    ''' Parses Spidy expression from string and builds syntax tree ready for evaluation. '''
    ep = ExpressionParser(context, lnum)
    r = ep.parse(expression)
    return r

class ExpressionParser(object):
    ''' Spidy expressions parser. '''
    
    _context = None
    _id = None
    _lnum = -1
    _sline = None
    
    _stack = None          # needed for nested expressions parsing   
    _root = None           # syntax tree root
    _cur = None            # currnetly prased node    
    _token = ''            # being parsed expression string fragment
    _token_exp = ''        # being parsed expression string fragment w/o string content (quotes)
    _is_string = ''        # True when reading string  
    _is_subtree = True     # True when sub-tree after parsing (e.g. parenths) becomes the main tree
    _stop_word = ''        # the stop word which terminated parsing 
    _stop_idx = -1         # index at which parsing was stoped by stopword

    def __init__(self, context, line_num):
        self._context = context
        self._id = self._context.get_id()
        self._lnum = line_num
        self._sline = self._context.get_script()[line_num]
        self._stack = []

    def reset(self):
        ''' Resets parser's state so it's ready for parsing. '''
        self._stack = []
        self._root = None
        self._cur = None
        self._token = ''            
        self._token_exp = ''      
        self._is_string = ''
        self._is_subtree = True
        self._stop_word = ''
        self._stop_idx = -1

    def get_stop_word(self):
        ''' Returns stop word at which parsing has stopped. '''
        return self._stop_word

    def get_stop_idx(self):
        ''' Returns index at which parsing has stopped. '''
        return self._stop_idx

    def parse(self, exp):
        ''' Parses Spidy expression from string and builds syntax tree ready for evaluation. '''
        log.debug(self._id, 'ExpressionParser: starting parsing: {0}...'.format(exp[:10]))        
        i = -1
        length = len(exp)
        while i < length - 1:
            i += 1
            char = exp[i]
            self._token += char
            
            # look for string
            if char in STRING:
                self._pass_string(char)                    
                continue            
            elif self._is_string != EMPTY:
                continue
            
            # parse indexers and lists
            elif char == LEFT_SQUARE:            
                value = self._read_value(char)
                incomplete = _is_not_complete(self._cur)
                n = None
                
                # create list node
                if incomplete and value == '':                
                    n = self._make_node(value, OP_LIST)
                    if self._cur != None:
                        self._cur.set_right(n)
                    else:
                        self._root = n
                
                # create indexer node
                else:
                    validate(self._id, self._sline, incomplete or value == '', 'ExpressionParser: invalid square brackets syntax')
                    
                    n = self._make_node(value, OP_INDEXER)
                    if self._cur == None:
                        self._try_set_left(n, value)
                        self._root = n
                        
                    # set inexer's left and attach it to the current
                    elif incomplete:
                        self._try_set_left(n, value)
                        self._cur.set_right(n)
                        
                    # otherwise complete current's right or wrap current in indexer, if closing parenths or it's another indexer
                    else: 
                        replace = self._cur
                        if not _is_list(replace) and not self._is_subtree and replace.get_op() != OP_INDEXER:
                            replace = replace.get_right()
                        
                        p = replace.get_parent()
                        if p != None:   # attach to new parent 
                            p.set_right(n)
                        else:           # make new root
                            n.set_parent(None)
                            self._root = n
                            
                        n.set_left(replace)
                            
                # save the current tree, start building the new one
                self._cur = n            
                self._reset_tokens()
                self._stack.append(self._root)
                self._stack.append(self._cur)
                self._reset_tree()
                
            # parse next list item
            elif char == COMMA:
                validate(self._id, self._sline, len(self._stack) != 0, 'ExpressionParser: invalid syntax')
                l = self._stack[-1]
                validate(self._id, self._sline, _is_list(l), 'ExpressionParser: invalid syntax')
                
                # complete current node and add it to the parent list
                value = self._read_value(char)
                self._complete_cur(value)
                self._reset_tokens()
                    
                validate(self._id, self._sline, self._root != None, 'ExpressionParser: list item expected')
                l.get_items().append(self._root)
                self._reset_tree()
            
            elif char == RIGHT_SQUARE:
                validate(self._id, self._sline, len(self._stack) != 0, 'ExpressionParser: unmatched right square bracket')
                
                value = self._read_value(char)
                self._complete_cur(value)
                self._reset_tokens()
                    
                # try to attach new tree to old one
                c = self._stack.pop()
                r = self._stack.pop()            
                if c != None:
                    
                    # complete list node
                    if _is_list(c):
                        validate(self._id, self._sline, self._root != None or len(c.get_items()) == 0, 'ExpressionParser: list item expected')
                        if self._root != None:
                            c.get_items().append(self._root)
                        
                    # complete indexer
                    else:
                        c.set_right(self._root)
                        
                    self._cur = c
                    self._root = r
                else:
                    self._cur = self._root
    
            # look for parehthesis
            elif char == LEFT_PAREN:
                value = self._read_value(char)
                validate(self._id, self._sline, value == '', 'ExpressionParser: invalid parenthesis syntax')
                
                # save the current tree, start building the new one
                self._stack.append(self._root)
                self._stack.append(self._cur)
                self._reset_tree()
                self._reset_tokens()
            
            elif char == RIGHT_PAREN:
                validate(self._id, self._sline, len(self._stack) != 0, 'ExpressionParser: unmatched right parenthesis')
                
                value = self._read_value(char)
                self._complete_cur(value)
                self._reset_tokens()
    
                # try to attach new tree to old one
                self._is_subtree = False
                c = self._stack.pop()
                r = self._stack.pop()            
                if c != None:
                    validate(self._id, self._sline, c.get_right() == None, 'ExpressionParser: invalid parenthesis syntax')                
                    self._cur = c
                    self._cur.set_right(self._root)
                    self._root = r
                else:
                    self._cur = self._root
                    self._is_subtree = True
            
            # try parse operator, grow syntax tree
            else:
                self._token_exp += char
                
                # read ahead to catch stuff which should be separated
                next_char = WHITESPACE
                if i < length - 1:
                    next_char = exp[i + 1]
                
                # try to read operator    
                operator = tokenizer.read_operator(self._token_exp, next_char)
                if operator != '':
                    
                    # break on stopwords
                    if operator in PARSER_STOPWORDS:
                        self._stop_word = operator
                        break
                    
                    value = self._read_value(operator)
                    n = self._make_node(value, operator)
                
                    # initiate syntax tree
                    if self._cur == None:                
                        self._try_set_left(n, value)
                        self._root = n
                    
                    # if new op precedence higher than prev op's, add new one to the current as child
                    elif (_is_not_complete(self._cur) and OPS_PREC[self._cur.get_op()] <= OPS_PREC[n.get_op()]):
                        self._try_set_left(n, value)
                        self._cur.set_right(n)
                            
                    # otherwise find the first parent with same or lower precedence and replace it by the node
                    else:
                        p = self._cur
                        
                        # set and list ops should be parsed right after target value/node
                        if  (_is_value(p) or _is_list(p) or self._is_subtree or not is_assignment(operator)):
                            p = p.get_parent()
                            
                        # bubble up
                        while (p != None and OPS_PREC[p.get_op()] > OPS_PREC[n.get_op()]):
                            p = p.get_parent()
                            
                        if p != None:   # re-arrange
                            t = p.get_right()
                            p.set_right(n)
                            n.set_left(t)
                            
                        else:           # make new root
                            n.set_left(self._root)
                            self._root = n
                            
                        self._try_set_right(self._cur, value)
                            
                    self._cur = n            
                    self._reset_tokens()
    
        validate(self._id, self._sline,
                 self._is_string == '', 'ExpressionParser: unclosed string')
        validate(self._id, self._sline,
                 len(self._stack) == 0, 'ExpressionParser: unmatched left parenthesis')
        validate(self._id, self._sline,
                 not isinstance(self._cur, UnaryNode)
                 or _is_not_complete(self._cur)
                 or self._token.strip() == ''
                 or self._stop_word != '', 'ExpressionParser: invalid syntax')

        # cut off stop word
        if self._stop_word != '':
            stop_len = len(self._stop_word)
            self._stop_idx = i + 1 - (stop_len - 1)
            self._token = self._token[:-stop_len]

        # complete syntax tree
        value = tokenizer.strip_parenths(self._token)    
        self._complete_cur(value)
            
        if self._root == None:
            self._root = NoneNode(self._context)
            
        log.debug(self._id, 'ExpressionParser: finished parsing')
        return self._root
    
    def _reset_tokens(self):
        self._token = ''
        self._token_exp = ''
        self._is_subtree = False
        
    def _reset_tree(self):
        self._cur = None
        self._root = None
        
    def _read_value(self, operator):
        value = self._token[:-len(operator)].strip()
        return value
    
    def _pass_string(self, char):
        if self._is_string == '':
            self._is_string = char
            self._token_exp += char
            
        elif self._is_string == char and self._token[-2] != BACKSLASH:
            self._is_string = ''
            self._token_exp += char
    
    def _make_node(self, value, operator):            
        # if current node is not complete and value is empty - create unary node
        node = None
        if (is_unary(operator)
            or can_be_unary(operator)
            and _is_not_complete(self._cur)
            and value == ''):
            
            validate(self._id, self._sline,
                     self._cur == None
                     or operator != OP_NOT
                     or is_logical(self._cur.get_op()),
                'ExpressionParser: invalid \'' + operator + '\' operator syntax')
            
            node = None
            if operator == OP_PATH:
                node = PathNode(self._context)
            else:
                node = UnaryNode(self._context)
            node.set_op(
                to_unary(operator))
            
        else:        
            if operator == OP_SET:
                node = SetNode(self._context)
            elif operator == OP_POP:
                node = PopNode(self._context)
            elif operator == OP_PUSH:
                node = PushNode(self._context)
            elif operator == OP_LIST:
                node = ListNode(self._context)
            else:
                node = BinaryNode(self._context)
            if operator != OP_LIST:
                node.set_op(operator)
        node.parse(self._lnum)
        return node
    
    def _make_value_node(self, value):        
        validate(self._id, self._sline,
            WHITESPACE not in value or is_string_const(value),
            'ExpressionParser: invalid syntax or whitespace in value or name')
        
        node = None
        if is_none(value):
            node = NoneNode(self._context)
        elif is_bool_const(value):
            node = BoolNode(self._context)
        elif is_string_const(value):
            node = StringNode(self._context)
        elif is_number_const(value):
            node = NumberNode(self._context)        
        elif is_var_name(value):
            node = VarNode(self._context)     
        if node != None:
            node.set_value(value)
            node.parse(self._lnum)
        return node
    
    def _try_set_left(self, node, value):
        if isinstance(node, ListNode):
            validate(self._id, self._sline, value == '', 'ExpressionParser: invalid syntax')
        elif isinstance(node, BinaryNode):
            validate(self._id, self._sline, value != '', 'ExpressionParser: invalid syntax')
            vn = self._make_value_node(value)
            node.set_left(vn)
        
    def _try_set_right(self, node, value):
        if isinstance(node, ListNode):
            validate(self._id, self._sline, value == '', 'ExpressionParser: invalid syntax')
        elif isinstance(node, UnaryNode) and node.get_right() == None:
            validate(self._id, self._sline, value != '' or is_incomplete(node.get_op()), 'ExpressionParser: invalid syntax')
            vn = self._make_value_node(value)
            node.set_right(vn)
            
    def _complete_cur(self, value):        
        if self._cur != None:
            self._try_set_right(self._cur, value)
        else:
            self._cur = self._make_value_node(value)        
        if self._root == None:
            self._root = self._cur

def _is_list(node):
    return isinstance(node, ListNode)

def _is_value(node):
    return isinstance(node, ValueNode)

def _is_not_complete(node):
    result = (not isinstance(node, ListNode)
              and not isinstance(node, ValueNode)
              and (node == None or node.get_right() == None))
    return result