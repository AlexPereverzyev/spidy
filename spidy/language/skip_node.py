
''' ``skip`` statement parsing and evaluation. '''

import syntax
import exp_parser

from spidy.document import *
from spidy.common import *
from nodes import Node

class SkipNode(Node):
    '''
    Moves document path pointer to specified element in document tree.
    The element to move pointer to is specified using XPath expression.
    
    Optionally, *skip* direction can be specified:
    - forward (default)
    - reverse
    
    .. note:: All selectors are still applied when in *reverse* mode.
    
    .. note:: ``skip`` command's XPath expression always evaluates to single
        element even if index selector is not specified.
        
    Example::
    
        skip &'//div[@id=data_container]'
    '''
    
    _path = None
    _direction = syntax.SkipDirection.FORWARD    
    
    def get_path(self):
        return self._path
    
    def set_path(self, path):
        self._path = path

    def get_direction(self):
        return self._direction
    
    def set_direction(self, direction):
        self._direction = direction
        
    def evaluate(self):
        log.debug(self._id, 'SkipNode: evaluating')        
        
        # check document is loaded and of structured format
        doc_type   = self._context.get_doc_type()
        tried_load = (doc_type != None and doc_type != DocType.UNKNOWN)
        validate_eval(self._id, self._sline, tried_load,
            'SkipNode: document should be loaded using {0} command'.format(syntax.OP_GET))        
        validate_eval(self._id, self._sline, doc_type != DocType.TXT,
            'SkipNode: document should be of structured format')
        
        # try to parse path, if empty - exit
        xpath = None
        if self._path.get_right() != None:    
            exp_string = self._path.get_right().evaluate()
            xpath      = XPath(self._id, self._sline, exp_string)
            
        if xpath == None or xpath.is_empty():
            return
        
        # try to skip to specified tag
        doc        = self._context.get_doc()
        cursor     = self._context.get_doc_cursor()
        reverse    = self._direction == syntax.SkipDirection.REVERSE
        new_cursor = xpath.skip(doc, cursor, reverse)
        
        if new_cursor != None:
            self._context.set_doc_cursor(new_cursor)
        
    def parse(self, line_num):
        log.debug(self._id, 'SkipNode: parsing')
        self._sline = self._context.get_script()[line_num]
        line = self._sline.string
        idx = line.index(syntax.OP_SKIP) + len(syntax.OP_SKIP)
        exp = line[idx:].strip()
        
        # parse path
        ep = exp_parser.ExpressionParser(self._context, line_num)
        self._path = ep.parse(exp)
        
        # parse direction
        direction = ep.get_stop_word()
        if direction != '':
            validate(self._id, self._sline,
                     direction == syntax.SkipDirection.FORWARD
                  or direction == syntax.SkipDirection.REVERSE,
                'SkipNode: invalid skip direction')
            self._direction = direction
        
    def __str__(self):
        string = syntax.OP_SKIP + syntax.WHITESPACE + str(self._path) + syntax.WHITESPACE + self._direction
        return string 