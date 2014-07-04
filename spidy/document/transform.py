
''' Base structured text-to-tag-tree transformation routines'''

from tag import Tag

class Transform(object):
    ''' Base class for structured text-to-tag-tree transformations. '''

    _roots = None
    _current = None

    def __init__(self):
        self._roots = []
        
    def perform(self, string):
        ''' Starts transformation, returns document tag-tree. '''
        return None
    
    def start_tag(self, name, attrs):
        ''' Start tag callback, called every time parser spots tag in structured text. '''
        tag = Tag()
        tag.set_name(name)
        tag.set_parent(self._current)
        
        for ak in attrs.keys():
            tag.get_attrs()[ak] = attrs[ak]

        if self._current != None:

            # calc index
            idx = 1
            for t in self._current.get_children():
                idx += (t.get_name() == name)            
            tag.set_index(idx)
            
            # calc scope/depth
            self._current.set_scope(
                self._current.get_scope() + 1)
            tag.set_depth(
                self._current.get_depth() + 1)
            
            self._current.get_children().append(tag)
                
        self._current = tag
        
        if self._current.get_parent() == None:
           self._roots.append(self._current)
        
    def end_tag(self, name):
        ''' End tag callback, called every time parser spots closing tag in structured text. '''
        tag = self._current
        while tag != None and tag.get_name() != name:
            tag = tag.get_parent()
    
        if tag != None:
            tag.set_is_closed(True)
            self._current = tag.get_parent()

    def data(self, data):
        ''' Tag data callback, called every time tag data is spotted in structured text. '''
        self._append_value(data)
                
    def entity(self, name):
        ''' Tag data callback, called every time entity (&something;) is spotted in structured text. '''
        self._append_value('&{0};'.format(name))
            
    def _append_value(self, value):
        if self._current != None:
            cv = self._current.get_value()            
            if cv != None:
                self._current.set_value(cv+value)
            else:
                self._current.set_value(value)