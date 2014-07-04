
''' Path ``&`` operator evaluation. '''

import syntax

from spidy.document import *
from spidy.common import *
from nodes import UnaryNode

class PathNode(UnaryNode):
    '''
    Interprets input string as XPath expression and evaluates it against current
    document. If index selector is specified in XPath expression, return single
    value, otherwise returns list.
    
    .. note:: Document should be loaded using ``get`` command before using ``&``
        operator.
        
    If used without path - ``&``, returns raw document's contents.
    
    If XPath expression can't be resolved, returns either empty string or list.
    
    Example::
    
        get 'http://myprofile/main.html'
        name = &'//span[@class=namefield][1]'
        
    Supports the following selectors:
    
    - children selector: ``/``
    - self plus all descendants selector: ``//``
    - name selector, 'any' and 'current' wildcards: ``/div`` or ``/*`` or ``.``
    - index selector: ``/div[2]``
    - attribute and/or it's value selector: ``/div[@class]`` or ``/div[@class=header]``
    - attribute getter: ``/div@class``
    - alternative paths: ``/div[2] | /span[1]``   
    '''
    
    _paths = None
    
    def __init__(self, context):
        super(PathNode, self).__init__(context)
        self._paths = []
        
    def __str__(self):
        string = syntax.OP_PATH
        if self._right != None:
            string += str(self._right)
        return string
    
    def get_path(self):
        return self._paths
    
    def evaluate(self):
        log.debug(self._id, 'PathNode: evaluating')
        if self._context.get_test():
            return self.to_metrics()    
        
        path_string = None
        if self._right != None:
            path_string = self._right.evaluate()
            self._paths = parse_xpath(self._id, self._sline, path_string)

        # check document is loaded
        doc = self._context.get_doc()
        doc_type = self._context.get_doc_type()
        if doc == None and doc_type != None and doc_type != DocType.UNKNOWN:
            return None
        
        validate_eval(self._id, self._sline, doc != None,
            'PathNode: document should be loaded using {0} command'.format(syntax.OP_GET))

        # filter document tree to get path value
        if self._right != None or len(self._paths) > 0:
            validate_eval(self._id, self._sline, doc_type != DocType.TXT,
                'PathNode: unstructured documents can\'t be traversed')
            tags = None
            value = None
            last = None            
            for path in self._paths:
                for segment in path:
                    if segment.is_current():
                        break
                    
                    if tags == None:
                        tags = self._context.get_branch()
                    else:
                        tags = [c for t in tags for c in t.get_children()]
                        
                    for s in segment.get_selectors():
                        tags = s.filter(tags)                    

                last = path[-1]
                value = self._extract_value(tags, last)
                
                if value != None:
                    break
                else:                    
                    tags = None
                    log.warning(self._id, 'PathNode: couldn\'t resolve path: {0}, line {1}'.format(path_string, self._sline.number+1))
                
            # never return None
            if value == None:
                if last == None or last.is_single():
                    value = ''
                elif last != None:
                    value = []
            return value

        # otherwise return the whole document's contents
        else:
            doc_raw = self._context.get_doc_raw()            
            validate_eval(self._id, self._sline, doc_raw != None,
                'PathNode: document should be loaded using {0} command'.format(syntax.OP_GET))
            return doc_raw

    def _extract_value(self, tags, selector):        
        value = None
        if selector.is_single():
            # extract single value
            tag = None
            if tags != None and len(tags) > 0:
                tag = tags[0]
            else:
                tag = self._context.get_doc_path_ptr()
            
            if tag != None:
                attr = selector.get_attr()
                if attr != None:
                    if tag.get_attrs().has_key(attr):
                        value = tag.get_attrs()[attr]
                else:
                    value = tag.get_value()
                    
                if value != None and isinstance(value, basestring):
                    value = value.strip()
        else:
            # extract list of values
            if tags != None and len(tags) > 0:
                value = []
                for t in tags:
                    v = None
                    attr = selector.get_attr()
                    if attr != None:                    
                        if t.get_attrs().has_key(attr):
                            v = t.get_attrs()[attr]
                    else:
                        v = t.get_value()
                    if v != None and isinstance(value, basestring):
                        v = v.strip()
                    elif value == None:
                        v = ''
                    value.append(v)
        return value
    
    def to_metrics(self):
        l = 0
        if self._right != None:
            path_string = self._right.evaluate()
            paths = parse_xpath(self._id, self._sline, path_string)
            l = sum([len(p) for p in paths])
        return '[items:{0}]'.format(l)