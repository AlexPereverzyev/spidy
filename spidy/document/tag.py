
''' Spidy primitive document element. '''

class Tag(object):
    ''' Basic abstract data element of structured document. '''
    
    _name = None
    _attrs = None
    _value = None        
    _parent = None
    _children = None
    _scope = 0
    _depth = 0
    _index = 1             # allows to generate document-wide XPath for given tag
    _is_closed = False     # whether the tag was closed correctly in original document
        
    def __init__(self):        
        self._attrs = {}        
        self._children = []

    def __str__(self):
        string = ''
        stack = [self]
        
        while len(stack) > 0:            
            cur = stack.pop()            
            mark = '+'
            if cur.is_closed():
                mark = '-'
                
            string += '{0}{1}[{2}]\n'.format(cur.get_depth()*mark, cur.get_name(), cur.get_index())
            stack.extend(reversed(cur.get_children()))
            
        return string
        
    def get_name(self):
        return self._name
    
    def set_name(self, name):
        self._name = name
    
    def get_attrs(self):
        return self._attrs
    
    def set_attrs(self, attrs):
        self._attrs = attrs
        
    def get_value(self):
        return self._value
    
    def set_value(self, value):
        self._value = value
                
    def get_parent(self):
        return self._parent
    
    def set_parent(self, parent):
        self._parent = parent
        
    def get_children(self):
        return self._children
    
    def set_children(self, children):
        self._children = children
    
    def get_scope(self):
        return self._scope
    
    def set_scope(self, scope):
        self._scope = scope
    
    def get_depth(self):
        return self._depth
    
    def set_depth(self, depth):
        self._depth = depth        
        for c in self._children:
            c.set_depth(depth + 1)
        
    def get_index(self):
        return self._index
    
    def set_index(self, index):
        self._index = index
        
    def is_closed(self):
        return self._is_closed
    
    def set_is_closed(self, is_closed):
        self._is_closed = is_closed
        
    def findall(self, name):
        return [c for c in self._children if c.get_name() == name]
    
    def indexof(self, child):
        idx = -1
        i = 0
        for t in self._children:
            if t == child:
                idx = i
                break
            i += 1
        return idx
    
    def update_scope(self):
        self._scope = len(self._children)
        
    def update_depth(self):
        self.set_depth(self._depth)
            
    def update_indexes(self):
        update_indexes(self._children)
     
    def make_path(self, branch_parent):
        path_string = ''
        path = []
        t = self
        
        while t != None and t != branch_parent:
            path.insert(0, t)
            t = t.get_parent()
                    
        for t in path:
            path_string += '/{0}[{1}]'.format(t.get_name(), t.get_index())
            
        return path_string
    
def update_scope(tag):
    if tag == None:
        return
    tag.set_scope(len(tag.get_children()))
    
def update_depth(tag):
    if tag == None:
        return
    tag.set_depth(tag.get_depth())
    
def update_indexes(tags):
    if tags == None:
        return
    indexes = {}
    for t in tags:                    
        if not indexes.has_key(t.get_name()):
            indexes[t.get_name()] = 0
        else:
            indexes[t.get_name()] += 1                        
        t.set_index(indexes[t.get_name()]+1)