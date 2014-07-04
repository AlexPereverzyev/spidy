
''' XPath expression parser. Please see Spidy documentation for whats supported. '''

__all__ = ['parse_xpath']

from selectors import *
from spidy.common import *
from spidy.common.sniff import is_int

XP_STRING = ['\'', '"']

XP_UNDEFINED       = 0 
XP_SEEK_NAME       = 1 
XP_SEEK_INDEX      = 2 
XP_SEEK_ATTR       = 4 
XP_SEEK_ATTR_EXIST = 8 
XP_SEEK_ATTR_MATCH = 16
XP_SEEK_CLOSURE    = 32
XP_SEEK_SEARCH     = 64
XP_READ_STRING     = 128
XP_START_NEW       = 256

def parse_xpath(id, sline, expression):
    ''' Parses XPath expression and returns list of list of paths segments ready for evaluation. '''
    paths = []
    path = []    
    cur = ''    
    pi = None
    s = XP_SEEK_NAME
    str_sep = None    
    i = -1
    
    for c in expression:        
        i += 1
        if c in XP_STRING and not s & XP_READ_STRING:
            validate(id, sline, s == XP_SEEK_CLOSURE, 'XPath: invalid syntax')
            s |= XP_READ_STRING
            str_sep = c
            
        elif c == str_sep and s & XP_READ_STRING and (i < 1 or expression[i-1] != '\\'):
            validate(id, sline, s == (XP_READ_STRING | XP_SEEK_CLOSURE), 'XPath: invalid syntax')
            s ^= XP_READ_STRING
            str_sep = None
            
        elif s & XP_READ_STRING:
            cur += c
            
        elif c == '|':            
            validate(id, sline, not s & XP_START_NEW, 'XPath: invalid syntax')
            validate(id, sline, cur != '' or not s & XP_SEEK_NAME, 'XPath: tag name should be specified')
                        
            # finish current, validate current path is not empty, start new path
            if pi == None and cur != '': pi = Segment()
            if pi != None:
                _complete_path(id, sline, path, pi, cur, s)            
            paths.append(path)
            path = []
            cur = ''    
            pi = None
            s = XP_SEEK_NAME | XP_START_NEW
                
        elif c == '/':
            if pi == None and cur != '': pi = Segment()
            if pi != None and not s & XP_SEEK_SEARCH:
                _complete_path(id, sline, path, pi, cur, s)
            
            if not s & XP_SEEK_SEARCH:
                pi = Segment()
                s = XP_SEEK_NAME | XP_SEEK_SEARCH
            else:
                pi.add_selector(FlattenSelector())
                s = XP_SEEK_NAME
            cur = ''
            
        elif c == '[':
            validate(id, sline, cur != '' or not s & XP_SEEK_NAME, 'XPath: tag name should be specified')
            validate(id, sline, s & (XP_SEEK_NAME | XP_SEEK_ATTR | XP_SEEK_CLOSURE), 'XPath: invalid syntax')
            
            if s & XP_SEEK_NAME:
                validate(id, sline, cur != '', 'XPath: invalid syntax')
                if pi == None: pi = Segment()
                pi.add_selector(NameSelector(cur))
            elif s & XP_SEEK_ATTR and cur.strip() != '':
                pi.set_attr(cur)
            
            s = XP_UNDEFINED
            if not pi.has_index():
                s |= XP_SEEK_INDEX                
            if not pi.has_attr_val():
                s |= XP_SEEK_ATTR_EXIST         
            cur = ''
            
        elif c == ']':
            validate(id, sline, cur != '' or s & XP_SEEK_CLOSURE, 'XPath: index or attribute must be specified')
            validate(id, sline, s & XP_SEEK_INDEX and is_int(cur) or s & (XP_SEEK_ATTR_MATCH | XP_SEEK_CLOSURE), 'XPath: invalid syntax')
            
            if s & XP_SEEK_INDEX:
                pi.add_selector(IndexSelector(int(cur)))
                s = XP_UNDEFINED
                if not pi.has_attr():
                    s |= XP_SEEK_ATTR                                
                
            elif s & XP_SEEK_ATTR_MATCH:
                pi.add_selector(AttributeValueSelector(cur))
                s = XP_UNDEFINED
                if not pi.has_index():
                    s |= XP_SEEK_INDEX                
                if not pi.has_attr():
                    s |= XP_SEEK_ATTR
                    
            elif s & XP_SEEK_CLOSURE:
                pi.get_selectors()[-1].set_value(cur)
                s = XP_UNDEFINED
                if not pi.has_index():
                    s |= XP_SEEK_INDEX                
                if not pi.has_attr():
                    s |= XP_SEEK_ATTR
            cur = ''
            
        elif c == '@':
            validate(id, sline, s & (XP_SEEK_NAME | XP_SEEK_ATTR | XP_SEEK_ATTR_EXIST), 'XPath: invalid syntax')
            
            if s & XP_SEEK_NAME:
                validate(id, sline, cur != '', 'XPath: invalid syntax')
                if pi == None: pi = Segment()
                pi.add_selector(NameSelector(cur))
            else:
                validate(id, sline, cur == '', 'XPath: invalid syntax')
                
            if s & XP_SEEK_ATTR_EXIST:
                s = XP_SEEK_ATTR_MATCH
            else:
                s = XP_SEEK_ATTR
            cur = ''
            
        elif c == '=':    
            validate(id, sline, cur != '' and s & XP_SEEK_ATTR_MATCH, 'XPath: invalid syntax')
            pi.add_selector(AttributeValueSelector(cur))
            s = XP_SEEK_CLOSURE
            cur = ''
            
        elif c != ' ' and c != '\t':
            validate(id, sline,
                not (c == '.' and pi != None and pi.has_search())
                and not ('.' in cur or '*' in cur), 'XPath: invalid syntax')
            s &= ~XP_SEEK_SEARCH
            cur += c            
            
    if cur != '' or not s & XP_SEEK_NAME:
        if pi == None: pi = Segment()
        _complete_path(id, sline, path, pi, cur, s)
        
    if len(path) > 0:
        paths.append(path)

    validate(id, sline, not s & XP_START_NEW, 'XPath: invalid syntax')
    validate(id, sline, len(paths) > 0, 'XPath: path expression should be specified')
    for p in paths:        
        if len(p) > 0:
            for pi in p[:-1]:
                validate(id, sline, pi.get_attr() == None, 'XPath: only last path item can return attribute value')            
            for pi in p:        
                validate(id, sline, pi.has_name(), 'XPath: only one path item is allowed to access current tag')
                
    return paths
    
def _complete_path(id, sline, path, segment, cur, state):
    c = cur.strip()
    if state & XP_SEEK_NAME:
        segment.add_selector(NameSelector(c))
    elif state & XP_SEEK_ATTR and c != '':
        segment.set_attr(c)
    elif c != '':
        validate(id, sline, not state & XP_SEEK_INDEX, 'XPath: invalid syntax')
    path.append(segment)