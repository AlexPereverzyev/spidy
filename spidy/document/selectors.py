
''' XPath data structures and selectors. '''

class Segment(object):
    ''' Represents XPath query syntaxical unit; contains selectors and optional attribute getter. '''
    
    _selectors     = None  # segment selectors
    _get_attr      = None  # attribute getter name, optional
    _has_name      = False # name selector is set, and so on...
    _has_index     = False
    _has_attr_val  = False
    _has_search    = False
    
    def __init__(self):        
        self._selectors = []
        
    def __str__(self):
        string = ''  
        for s in self._selectors:
            string += str(s)                
        if self._get_attr != None:
            string += '@' + self._get_attr
        return string

    def get_selectors(self):
        ''' Returns path segment's selectors. Use add_selector to add selectors to segment. '''
        return self._selectors
    
    def add_selector(self, selector):
        ''' Adds selector to path segment and updates parsing flags. ''' 
        self._has_name      = self._has_name     or isinstance(selector, NameSelector)
        self._has_index     = self._has_index    or isinstance(selector, IndexSelector)        
        self._has_attr_val  = self._has_attr_val or isinstance(selector, AttributeValueSelector)
        self._has_search    = self._has_search   or isinstance(selector, FlattenSelector)        
        self._selectors.append(selector)

    def get_attr(self):
        return self._get_attr
    
    def set_attr(self, attr):
        self._get_attr = attr
    
    def has_attr(self):
        return self._get_attr != None

    def has_name(self):
        return self._has_name

    def has_index(self):
        return self._has_index
    
    def has_attr_val(self):
        return self._has_attr_val
    
    def has_search(self):
        return self._has_search
    
    def is_current(self):
        ''' Returns True if path segment selects current tag. ''' 
        for s in self._selectors:
            if isinstance(s, NameSelector) and str(s) == '.':
                return True
        return False

    def is_single(self):
        ''' Returns True if path segment selects single tag - either has index selector or selects current. ''' 
        return self.is_current() or self.has_index()

class Selector(object):
    ''' Base selector class, defines filter method. '''
    def filter(self, tags):
        pass

class NameSelector(Selector):
    ''' Selects all tags which name is equal to specified value. '''
    
    _name = None
    
    def __init__(self, name):
        self._name = name
        
    def __str__(self):
        return self._name
        
    def filter(self, tags):
        
        return [t for t in tags if self._name == '*' or self._name == t.get_name()]

class IndexSelector(Selector):
    ''' Selects single tag by collection index. '''
    
    _index = -1
    
    def __init__(self, index):
        self._index = index
        
    def __str__(self):
        return '[{0}]'.format(self._index)
        
    def filter(self, tags):        
        return [t for i,t in enumerate(tags) if i == self._index-1]

class AttributeValueSelector(Selector):
    ''' Selects all tags with either any attribute equals value (name = '*') or attribute with specified name and value. '''
    
    _attr = None
    _value = None
    
    def __init__(self, attr):
        self._attr = attr
        self._value = None
        
    def __str__(self):
        value = ''
        if self._value != None:
            value = '=' + self._value
        string = '[@{0}{1}]'.format(self._attr, value)
        return string
    
    def set_value(self, value):
        self._value = value 
        
    def filter(self, tags):        
        return [t for t in tags                
                if ((self._attr == '*' and (self._value == None and len(t.get_attrs()) > 0 or len([a for a in t.get_attrs().items() if a[1] == self._value]) > 0))
                 or (self._attr != '*' and t.get_attrs().has_key(self._attr) and (self._value == None or self._value == t.get_attrs()[self._attr])))]
    
class FlattenSelector(Selector):
    ''' Transforms tag tree branch into flat list suitable for search. '''
    
    def __str__(self):
        return '//'
        
    def filter(self, tags):        
        flat = []
        flat.extend(tags)
        stack = []
        stack.extend(reversed(tags))
        while len(stack) > 0:
            cur = stack.pop()            
            stack.extend(reversed(cur.get_children()))
            flat.extend(cur.get_children())
        return flat