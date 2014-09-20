
''' XPath expression parser. Please see Spidy documentation for what's supported. '''

__all__ = ['XPath']

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

class XPath(object):
    ''' XPath helper class, contains commonly used XPath parsing and evaluation
        routines. '''
    
    _id = None
    _sline = None
    _exp_string = None
    _paths = None 
    
    def __init__(self, id, sline, exp_string):
        self._id = id
        self._sline = sline
        self._exp_string = exp_string
        self._paths = []
        self._parse()
    
    def is_empty(self):
        ''' Indicates that XPath expression has no selectors specified. '''
        return len(self._paths) == 0
    
    def get_paths(self):
        ''' Returns parsed path segments. '''
        return self._paths
    
    def apply(self, tags, cursor):
        ''' Applies XPath expression to supplied tag tree and returns value. '''
        
        cur_tags = None
        value = None
        last = None            
        for path in self._paths:
            
            # init
            last = path[-1]    
            if cursor != None: cur_tags = cursor.get_children()
            else: cur_tags = tags
            
            # apply selectors, ignore 'current tag' ones    
            for segment in [s for s in path if not s.is_current()]:
                for s in segment.get_selectors():
                    cur_tags = s.filter(cur_tags)                
                if segment != last:    
                    cur_tags = [c for t in cur_tags for c in t.get_children()]
            
            value = self._extract_value(cursor, cur_tags, last)
            
            if value != None:
                break
            cur_tags = None
            
        # never return None
        if value == None:
            msg = 'XPath: couldn\'t resolve path when applying: {0}, line {1}'.format(self._exp_string, self._sline.number+1)
            log.warning(self._id, msg)
            
            if last == None or last.is_single():
                value = ''
            elif last != None:
                value = []

        return value        
    
    def skip(self, tags, cursor, reverse = False):
        ''' Skips tag tree to specified by XPath expression tag element and
            returns it. '''
        cur_tags = None        
        for path in self._paths:
            
            # init
            last = path[-1]
            if not reverse:
                if cursor != None: cur_tags = cursor.get_children()
                else: cur_tags = tags
            else:
                cur_tags = [cursor]
            
            for segment in [s for s in path if not s.is_current()]:
                if not reverse:                    
                    for s in segment.get_selectors():
                        cur_tags = s.filter(cur_tags)
                        
                    if segment != last:
                        cur_tags = [c for t in cur_tags for c in t.get_children()]
                        
                    if cur_tags == None or len(cur_tags) == 0:
                        cur_tags = None
                        break
    
                else: 
                    if cursor == None:
                        break
                        
                    for s in segment.get_selectors():
                        cur_tags = s.filter(cur_tags)
                        
                    if cur_tags == None or len(cur_tags) == 0 or cur_tags[0].get_parent() == None:
                        cur_tags = None
                        break
                    else:
                        cur_tags = [cur_tags[0].get_parent()]
           
        if cur_tags != None and len(cur_tags) > 0:
            return cur_tags[0]
        else:
            msg = 'XPath: couldn\'t resolve path when skipping: {0}, line {1}'.format(self._exp_string, self._sline.number+1)
            log.warning(self._id, msg)
            return None
         
    def _parse(self):
        ''' Parses XPath expression and returns list of paths segments
            ready for evaluation (each path is composed of segments).
            
            Note: thou its seems natural to reduce the result to plain list of
                  selectors, validation can get very kinky w/o segments which
                  carry current state. '''
        path = []    
        cur = ''    
        pi = None
        s = XP_SEEK_NAME
        str_sep = None    
        i = -1
        
        for c in self._exp_string:        
            i += 1
            if c in XP_STRING and not s & XP_READ_STRING:
                validate(self._id, self._sline, s == XP_SEEK_CLOSURE, 'XPath: invalid syntax')
                s |= XP_READ_STRING
                str_sep = c
                
            elif c == str_sep and s & XP_READ_STRING and (i < 1 or self._exp_string[i-1] != '\\'):
                validate(self._id, self._sline, s == (XP_READ_STRING | XP_SEEK_CLOSURE), 'XPath: invalid syntax')
                s ^= XP_READ_STRING
                str_sep = None
                
            elif s & XP_READ_STRING:
                cur += c
                
            elif c == '|':            
                validate(self._id, self._sline, not s & XP_START_NEW, 'XPath: invalid syntax')
                validate(self._id, self._sline, cur != '' or not s & XP_SEEK_NAME, 'XPath: tag name should be specified')
                            
                # finish current, validate current path is not empty, start new path
                if pi == None and cur != '': pi = Segment()
                if pi != None:
                    self._complete_path(path, pi, cur, s)
                self._paths.append(path)
                path = []
                cur = ''    
                pi = None
                s = XP_SEEK_NAME | XP_START_NEW
                    
            elif c == '/':
                if pi == None and cur != '': pi = Segment()
                if pi != None and not s & XP_SEEK_SEARCH:
                    self._complete_path(path, pi, cur, s)
                
                if not s & XP_SEEK_SEARCH:
                    pi = Segment()
                    s = XP_SEEK_NAME | XP_SEEK_SEARCH
                else:
                    pi.add_selector(FlattenSelector())
                    s = XP_SEEK_NAME
                cur = ''
                
            elif c == '[':
                validate(self._id, self._sline, cur != '' or not s & XP_SEEK_NAME, 'XPath: tag name should be specified')
                validate(self._id, self._sline, s & (XP_SEEK_NAME | XP_SEEK_ATTR | XP_SEEK_CLOSURE), 'XPath: invalid syntax')
                
                if s & XP_SEEK_NAME:
                    validate(self._id, self._sline, cur != '', 'XPath: invalid syntax')
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
                validate(self._id, self._sline, cur != '' or s & XP_SEEK_CLOSURE, 'XPath: index or attribute must be specified')
                validate(self._id, self._sline, s & XP_SEEK_INDEX and is_int(cur) or s & (XP_SEEK_ATTR_MATCH | XP_SEEK_CLOSURE), 'XPath: invalid syntax')
                
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
                validate(self._id, self._sline, s & (XP_SEEK_NAME | XP_SEEK_ATTR | XP_SEEK_ATTR_EXIST), 'XPath: invalid syntax')
                
                if s & XP_SEEK_NAME:
                    validate(self._id, self._sline, cur != '', 'XPath: invalid syntax')
                    if pi == None: pi = Segment()
                    pi.add_selector(NameSelector(cur))
                else:
                    validate(self._id, self._sline, cur == '', 'XPath: invalid syntax')
                    
                if s & XP_SEEK_ATTR_EXIST:
                    s = XP_SEEK_ATTR_MATCH
                else:
                    s = XP_SEEK_ATTR
                cur = ''
                
            elif c == '=':    
                validate(self._id, self._sline, cur != '' and s & XP_SEEK_ATTR_MATCH, 'XPath: invalid syntax')
                pi.add_selector(AttributeValueSelector(cur))
                s = XP_SEEK_CLOSURE
                cur = ''
                
            elif c != ' ' and c != '\t':
                validate(self._id, self._sline,
                    not (c == '.' and pi != None and pi.has_search())
                    and not ('.' in cur or '*' in cur), 'XPath: invalid syntax')
                s &= ~XP_SEEK_SEARCH
                cur += c            
                
        if cur != '' or not s & XP_SEEK_NAME:
            if pi == None: pi = Segment()
            self._complete_path(path, pi, cur, s)
            
        if len(path) > 0:
            self._paths.append(path)
    
        validate(self._id, self._sline, not s & XP_START_NEW, 'XPath: invalid syntax')
        validate(self._id, self._sline, len(self._paths) > 0, 'XPath: path expression should be specified')
        for p in self._paths:        
            if len(p) > 0:
                for pi in p[:-1]:
                    validate(self._id, self._sline, pi.get_attr() == None, 'XPath: only last path segment can specify attribute selector')
                for pi in p:        
                    validate(self._id, self._sline, pi.has_name(), 'XPath: only one current tag selector is allowed')
    
    def _complete_path(self, path, segment, cur, state):
        c = cur.strip()
        if state & XP_SEEK_NAME:
            segment.add_selector(NameSelector(c))
        elif state & XP_SEEK_ATTR and c != '':
            segment.set_attr(c)
        elif c != '':
            validate(id, sline, not state & XP_SEEK_INDEX, 'XPath: invalid syntax')
        path.append(segment)
    
    def _extract_value(self, cursor, tags, segment):        
        value = None
        if segment.is_single():
            # extract single value
            tag = None
            if tags != None and len(tags) > 0:
                tag = tags[0]            
            else:
                # accessing current tag
                tag = cursor
            
            if tag != None:
                attr = segment.get_attr()
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
                    attr = segment.get_attr()
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