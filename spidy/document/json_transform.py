
''' JSON-to-tag-tree transformation routines. '''

__all__ = ['JsonTransform']

import json

from transform import *
from tag import Tag

ARRAY_TAG_NAME = 'tag'
        
class JsonTransform(Transform):
    ''' Transforms JSON document to tag-tree ready for traversing. Rules are the following:
    
        - 'tag' is reserved for naming root elements or nested lists
        - list treated as lists of objects with the same name, but different indexes
        - single dictionary is treated as object w/ attributes, but w/o value
        - single value is treated as object w/o attributes, but w/ value
    '''
    
    def perform(self, json_string):        
        self._roots = []
        stack = []                
        objects = json.loads(json_string)
        
        # initiate traversing 
        if not isinstance(objects, list):
            objects = [objects]
        
        for i in reversed(range(len(objects))):        
            nt = Tag()
            nt.set_name(ARRAY_TAG_NAME)
            nt.set_index(i+1)
            v = objects[i]        
            if isinstance(v, dict):
                nt.set_attrs(v)
            elif isinstance(v, list):
                nt.get_attrs()[ARRAY_TAG_NAME] = v
            else:
                nt.set_value(v)
            stack.append(nt)
        
        # traverse parsed objects, make tags 
        while len(stack) > 0:
            cur = stack.pop()    
            
            for k in cur.get_attrs().keys():
                value = cur.get_attrs()[k]
                
                if isinstance(value, dict):
                    nt = Tag()
                    nt.set_name(k)
                    nt.set_attrs(value)
                    nt.set_parent(cur)                    
                    nt.set_is_closed(True)
                    nt.set_depth(cur.get_depth() + 1)
                    cur.get_children().append(nt)                    
                    cur.set_scope(cur.get_scope() + 1)
                    stack.append(nt)
                    cur.get_attrs().pop(k)
                    
                elif isinstance(value, list):
                    for i,v in enumerate(value):
                        nt = Tag()
                        nt.set_name(k)
                        nt.set_index(i+1)
                        if isinstance(v, dict):
                            nt.set_attrs(v)
                        elif isinstance(v, list):
                            nt.get_attrs()[k] = v
                        else:
                            nt.set_value(v)
                        nt.set_parent(cur)
                        nt.set_is_closed(True)
                        nt.set_depth(cur.get_depth() + 1)
                        cur.get_children().append(nt)
                        cur.set_scope(cur.get_scope() + 1)
                        stack.append(nt)
                    cur.get_attrs().pop(k)
            
            if cur.get_parent() == None:
                self._roots.append(cur)
            
        if len(self._roots) == 0:
            return None    
        return self._roots

    def start_tag(self, name, attrs):
        pass
    
    def end_tag(self, name):
        pass
    
    def data(self, data):
        pass