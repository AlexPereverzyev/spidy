
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
    
    def evaluate(self):
        log.debug(self._id, 'PathNode: evaluating')
        if self._context.get_test():
            return self.to_metrics()    
        
        # check document is at least tried to load
        doc         = self._context.get_doc()
        doc_type    = self._context.get_doc_type()
        tried_load  = (doc_type != None and doc_type != DocType.UNKNOWN)
        validate_eval(self._id, self._sline, tried_load,
            'PathNode: document should be loaded using {0} command'.format(syntax.OP_GET))
        
        # try to parse path
        xpath = None        
        if self._right != None:
            exp_string = self._right.evaluate()
            xpath      = XPath(self._id, self._sline, exp_string)
        
        # if path is not empty - evaluate it
        if xpath != None and not xpath.is_empty():            
            validate_eval(self._id, self._sline, doc_type != DocType.TXT,
                'PathNode: unstructured documents can\'t be traversed')
            # return empty if failed to load
            if doc == None:
                if xpath.get_path()[-1].is_single(): return ''
                else: return []            
            cursor = self._context.get_doc_cursor()
            value = xpath.apply(doc, cursor)            
            return value

        # otherwise return the whole document's contents
        else:
            doc_raw = self._context.get_doc_raw()
            if doc_raw == u'empty':
                return None
            return doc_raw
    
    def __str__(self):
        string = syntax.OP_PATH
        if self._right != None:
            string += str(self._right)
        return string
    
    def to_metrics(self):
        l = 0
        if self._right != None:
            exp_string = self._right.evaluate()
            xpath = XPath(self._id, self._sline, exp_string)
            l = sum([len(p) for p in xpath.get_paths()])
        return '[items:{0}]'.format(l)