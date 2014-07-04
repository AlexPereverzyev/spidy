
''' 'if...else' statement parsing and evaluation. '''

import syntax
import exp_parser

from spidy.common import *
from nodes import Node

class IfElseNode(Node):
    '''
    Typical *if...else* statement, implements execution flow control. *else* is
    optional.
    
    Example::
    
        if loaded:
            str = str + $count
            result = str
        else:
            result = 'failed :('            
    '''
        
    _condition = None 
    _if_script = None
    _else_script = None
        
    def get_if_script(self):
        return self._if_script
    
    def set_if_script(self, script):
        self._if_script = script
        
    def get_else_script(self):
        return self._else_script
    
    def set_else_script(self, script):
        self._else_script = script
        
    def get_condition(self):
        return self._condition
    
    def set_condition(self, condition):
        self._condition = condition
        
    def evaluate(self):
        log.debug(self._id, 'IfElseNode: evaluating')
        if self._condition.evaluate():
            self._if_script.evaluate()
        elif self._else_script != None:
            self._else_script.evaluate()
        
    def parse(self, line_num):
        log.debug(self._id, 'IfElseNode: parsing')        
        lines = self._context.get_script()
        self._sline = lines[line_num]
        if_line = self._sline.string
        
        # check if we have indented 'if' block
        validate(self._id, self._sline, line_num + 1 < len(lines),
            'IfElseNode: missing script block after ' + syntax.OP_IF)
        validate(self._id, self._sline, syntax.is_indented_block(lines[line_num:line_num + 2]),
            'IfElseNode: expected an indented block after '  + syntax.OP_IF)
        validate(self._id, self._sline, if_line.rstrip().endswith(syntax.COLON),
            'IfElseNode: expected ' + syntax.COLON + ' after ' + syntax.OP_IF + ' condition')
                
        # parse 'if' line
        idx = if_line.index(syntax.OP_IF) + len(syntax.OP_IF)
        condition = if_line[idx:].replace(syntax.COLON, '').strip()
                
        self._condition = exp_parser.parse_expression(self._context, line_num, condition)
    
    def parse_else(self, line_num):
        ''' Parses 'else' statement - pretty much validates formating. '''
        log.debug(self._id, 'IfElseNode: parsing else')
        lines = self._context.get_script()
        if_line = self._if_script.get_script_line()
        else_line = lines[line_num]
        if_indent = syntax.get_indent(if_line)
        else_indent = syntax.get_indent(else_line)
        
        if if_indent != else_indent:
            self._else_script = None
            return
    
        # check if we have indented 'else' block
        idx = else_line.string.index(syntax.OP_ELSE) + len(syntax.OP_ELSE)
        validate(self._id, self._sline, else_line[idx:].strip() == syntax.COLON,
            'IfElseNode: expected ' + syntax.COLON + ' after ' + syntax.OP_ELSE)
        validate(self._id, self._sline, line_num + 1 < len(lines),
            'IfElseNode: missing script block after ' + syntax.OP_ELSE)            
        validate(self._id, self._sline, syntax.is_indented_block(lines[line_num:line_num + 2]),
            'IfElseNode: expected an indented block after ' + syntax.OP_ELSE)

    def __str__(self):
        string = syntax.OP_IF + syntax.WHITESPACE + str(self._condition) + syntax.COLON + '\n'
    
        if_lines = str(self._if_script).strip().split('\n')
        for i in range(len(if_lines)):
            if_lines[i] = '\t' + if_lines[i]            
        string += '\n'.join(if_lines)
        
        if self._else_script != None:
            string += '\n' + syntax.OP_ELSE + syntax.COLON + '\n'
            
            else_lines = str(self._else_script).strip().split('\n')
            for i in range(len(else_lines)):
                else_lines[i] = syntax.TAB + else_lines[i]
            string += '\n'.join(else_lines)            
        return string