
''' XML-to-tag-tree transformation routines. '''

__all__ = ['XmlTransform']

import xml.parsers.expat

from transform import Transform

class XmlTransform(Transform):
    ''' Transforms XML document to document tag-tree ready for traversing. '''

    def perform(self, xml_string):
        self._roots = []
        self._current = None 
        
        p = xml.parsers.expat.ParserCreate()
        p.StartElementHandler = self.start_tag
        p.EndElementHandler = self.end_tag
        p.CharacterDataHandler = self.data
        p.EntityDeclHandler = self._xml_entity
        p.Parse(xml_string)
        
        if len(self._roots) == 0:
            return None
        return self._roots
    
    def _xml_entity(self, entityName, is_parameter_entity, value, base, systemId, publicId, notationName):
        self.entity(entityName)