
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
    
    _direction = syntax.SkipDirection.FORWARD
    _paths = None
    
    def get_path(self):
        return self._paths
    
    def set_path(self, path):
        self._paths = path

    def get_direction(self):
        return self._direction
    
    def set_direction(self, direction):
        self._direction = direction
        
    def evaluate(self):
        log.debug(self._id, 'SkipNode: evaluating')        
        
        # check document is loaded and of structured format
        doc_type = self._context.get_doc_type()        
        validate_eval(self._id, self._sline, doc_type != None and doc_type != DocType.UNKNOWN,
            'SkipNode: document should be loaded using {0} command'.format(syntax.OP_GET))        
        validate_eval(self._id, self._sline, doc_type != DocType.TXT,
            'SkipNode: document should be of structured format')
        
        # try to parse path, if empty - exit
        paths = None
        path_string = ''
        if self._paths.get_right() != None:    
            path_string = self._paths.get_right().evaluate()
            paths = parse_xpath(self._id, self._sline, path_string)
            
        if paths == None or len(paths) == 0:
            return
        
        tags = None        
        for path in paths:        
            for segment in path:
                
                if self._direction == syntax.SkipDirection.FORWARD:
                    if segment.is_current():
                        break
                    
                    if tags == None:
                        tags = self._context.get_branch()
                    else:
                        tags = [c for t in tags for c in t.get_children()]
                            
                    for s in segment.get_selectors():
                        tags = s.filter(tags)
                        
                    if tags == None or len(tags) == 0:
                        tags = None
                        break
    
                else: # self._direction == syntax.SkipDirection.REVERSE:                    
                    if self._context.get_doc_path_ptr() == None:
                        break
                    
                    if tags == None:
                        tags = [self._context.get_doc_path_ptr()]
                        
                    for s in segment.get_selectors():
                        tags = s.filter(tags)
                        
                    if tags == None or len(tags) == 0 or tags[0].get_parent() == None:
                        tags = None
                        break
                    else:
                        tags = [tags[0].get_parent()]
           
        if tags != None and len(tags) > 0:
            self._context.set_doc_path_ptr(tags[0])
        else:
            log.warning(self._id, 'SkipNode: couldn\'t resolve path: {0}, line {1}'.format(path_string, self._sline.number+1))
        
    def parse(self, line_num):
        log.debug(self._id, 'SkipNode: parsing')
        self._sline = self._context.get_script()[line_num]
        line = self._sline.string
        idx = line.index(syntax.OP_SKIP) + len(syntax.OP_SKIP)
        exp = line[idx:].strip()
        
        # parse path
        ep = exp_parser.ExpressionParser(self._context, line_num)
        self._paths = ep.parse(exp)
        
        # parse direction
        direction = ep.get_stop_word()
        if direction != '':
            validate(self._id, self._sline, direction == syntax.SkipDirection.FORWARD
                  or direction == syntax.SkipDirection.REVERSE,
                'SkipNode: invalid skip direction')
            self._direction = direction
        
    def __str__(self):
        string = syntax.OP_SKIP + syntax.WHITESPACE + str(self._paths) + syntax.WHITESPACE + self._direction
        return string 