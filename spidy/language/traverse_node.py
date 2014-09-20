
''' ``traverse`` statement parsing and evaluation. '''

import syntax
import exp_parser

from collections import deque
from spidy.document import *
from spidy.common import *
from tokenizer import *
from nodes import Node
from nodes import NumberNode
from skip_node import SkipNode

# traverse ident in @path_string [mode depth]:
class TraverseNode(Node):
    '''
    Traverses document tree from specified element or from document root -
    sub-branch is specified by path operator.
    
    .. note:: Internally, setting sub-branch to certain element is done by
        ``skip`` command. Thereby sometimes when it fails you can see *SkipNode*
        messages in log.
        
    Sets loop variable to absolute (document-wide) element's path string, which
    can be used in path ``&``, ``skip`` or another ``traverse`` operators.
    
    Optionally, traverse method can be specified:
    
    - breadthfirst (default)
    - depthfirst
    
    If method is specified, depth of traversing can be set as well. Default is 1.

    Example, default form::
    
        traverse div in &'//div[@data_container]':
            if &div == '':
                break
                
    Or, visit each document's element to find pictures::
    
        images = []
        traverse element in & depthfirst 1000000:
            if 'img' in element:
                images << &(element + '@src')    
    '''
        
    _ident = None
    _path = None
    _body = None
    _mode = syntax.TraverseMode.BREADTH_FIRST
    _depth = None
        
    def __init__(self, context):
        super(TraverseNode, self).__init__(context)        
        self._depth = NumberNode(context)
        self._depth.set_value('1')
      
    def get_ident(self):
        return self._ident
    
    def set_ident(self, ident):
        self._ident = ident
    
    def get_path(self):
        return self._path
    
    def set_path(self, path):
        self._path = path
        
    def get_body(self):
        return self._body
    
    def set_body(self, body):
        self._body = body
        
    def get_mode(self):
        return self._mode
    
    def set_mode(self, mode):
        self._mode = mode
        
    def get_depth(self):
        return self._depth
    
    def set_depth(self, depth):
        self._depth = depth
        
    def evaluate(self):
        log.debug(self._id, 'TraverseNode: evaluating')
        doc_type = self._context.get_doc_type()
        doc = self._context.get_doc()
        
        validate_eval(self._id, self._sline, doc != None and doc_type != DocType.UNKNOWN,
            'TraverseNode: document should be loaded using {0} command'.format(syntax.OP_GET))        
        validate_eval(self._id, self._sline, doc_type != DocType.TXT,
            'TraverseNode: document should be of structured format')
        validate_eval(self._id, self._sline, not self._context.is_bound(self._ident),
            'TraverseNode: loop variable is already defined')
        
        depth = self._depth.evaluate()        
        validate_eval(self._id, self._sline, depth >= 0, 'TraverseNode: traverse depth should be equals or greater than zero')
        
        # skip to path
        cur_cursor = self._context.get_doc_cursor()
        skip = SkipNode(self._context)
        skip.set_script_line(self._sline)
        skip.set_path(self._path)
        skip.evaluate()

        # initialize
        self._context.bind_var(self._ident)
        roots = None
        doc_cursor = self._context.get_doc_cursor()
        if doc_cursor != None:
            roots = doc_cursor.get_children()
        else:
            roots = doc

        cur = None    
        cur_depth = 0
        if roots != None and len(roots) > 0:
            cur_depth = roots[0].get_depth()

        box = deque()
        if self._mode == syntax.TraverseMode.BREADTH_FIRST: 
            box.extend(roots)
        else: # self._mode == syntax.TraverseMode.DEPTH_FIRST:
            box.extend(reversed(roots))

        while len(box) > 0:
            if self._mode == syntax.TraverseMode.BREADTH_FIRST:            
                cur = box.popleft()
                if cur.get_depth() - cur_depth >= depth:
                    continue
                box.extend(cur.get_children())
                
            else: # self._mode == syntax.TraverseMode.DEPTH_FIRST:
                cur = box.pop()
                if cur.get_depth() - cur_depth >= depth:
                    continue
                box.extend(reversed(cur.get_children()))
                
            cur_path = cur.make_path(self._context.get_doc_cursor())
            self._context.set_var(self._ident, cur_path)
            self._body.evaluate()
            
            # check flags
            flags = self._context.get_flags() & ~ExecutionFlags.CONTINUE
            self._context.set_flags(flags)
            if flags & ExecutionFlags.BREAK:
                self._context.set_flags(flags & ~ExecutionFlags.BREAK)
                break
            
        self._context.unbind_var(self._ident)
        self._context.set_doc_cursor(cur_cursor)
    
    def parse(self, line_num):
        log.debug(self._id, 'TraverseNode: parsing')
        lines = self._context.get_script()
        self._sline = lines[line_num]
        line = self._sline.string
        
        # check if we have indented 'traverse...in' block
        validate(self._id, self._sline, line_num + 1 < len(lines),
            'TraverseNode: missing script block after ' + syntax.OP_FOR)            
        validate(self._id, self._sline, syntax.is_indented_block(lines[line_num:line_num + 2]),
            'TraverseNode: expected an indented block after ' + syntax.OP_TRAVERSE)
        validate(self._id, self._sline, line.rstrip().endswith(syntax.COLON),
            'TraverseNode: expected ' + syntax.COLON + ' after ' + syntax.OP_TRAVERSE + ' path string')
        
        # parse 'traverse...in' line
        idx = line.index(syntax.OP_TRAVERSE) + len(syntax.OP_TRAVERSE)
        l = line[idx:]
        idx = skip_space(l)
        l = l[idx:]
        ident_idx = skip_token(l)

        # set loop identity first
        ident = l[:ident_idx]
        validate(self._id, self._sline, syntax.is_var_name(ident), 'TraverseNode: invalid loop variable name')            
        self._ident = ident
        
        # check 'in' operator
        l = l[ident_idx:]
        idx = skip_space(l)
        l = l[idx:]
        in_idx = skip_token(l)        
        validate(self._id, self._sline, l[:in_idx] == syntax.OP_IN, 'TraverseNode: invalid syntax')
        
        # now parse path
        l = l[in_idx:]
        idx = skip_space(l)
        path = l[idx:].replace(syntax.COLON, '').strip()
        ep = exp_parser.ExpressionParser(self._context, line_num)
        self._path = ep.parse(path)
        
        # try to parse traverse mode and/or depth
        mode = ep.get_stop_word()
        if mode != '':
            validate(self._id, self._sline, mode == syntax.TraverseMode.DEPTH_FIRST
                  or mode == syntax.TraverseMode.BREADTH_FIRST,
                'TraverseNode: invalid traverse mode')
            self._mode = mode
            
            depth_shift = ep.get_stop_idx() + len(ep.get_stop_word())
            depth = path[depth_shift:]
            if depth != '':
                ep.reset()
                self._depth = ep.parse(depth)
                
    def __str__(self):
        string = (syntax.OP_TRAVERSE + syntax.WHITESPACE + self._ident + syntax.WHITESPACE +
                  syntax.OP_IN + syntax.WHITESPACE + str(self._path) + syntax.WHITESPACE + 
                  self._mode + syntax.WHITESPACE + str(self._depth) + syntax.COLON + syntax.LINEFEED)
        
        body_lines = str(self._body).strip().split(syntax.LINEFEED)
        for i in range(len(body_lines)):
            body_lines[i] = syntax.TAB + body_lines[i]            
        string += syntax.LINEFEED.join(body_lines)
        
        return string