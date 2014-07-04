
''' HTML-to-tag-tree transformation routines. '''

__all__ = ['HtmlTransform']

from HTMLParser import HTMLParser
from transform import Transform

HTML_TEXT_FORMAT = ['b', 'i', 'em', 'small', 'strong', 'sub', 'sup', 'ins' 'del' 'mark']
HTML_IGNORE = HTML_TEXT_FORMAT

class HtmlTransform(Transform):
    ''' Transforms raw HTML document to document tag-tree ready for traversing. '''
    
    _last_closed = None
    
    def perform(self, html_string):
        self._roots = []
        self._current = None
        self._last_closed = None
        
        p = HtmlParserProxy()
        p.start_tag_handler = self.start_tag
        p.end_tag_handler = self.end_tag
        p.data_handler = self.data
        p.entity_handler = self.entity
        p.feed(html_string)
        
        return self._roots
    
    def start_tag(self, name, attrs):
        if name in HTML_IGNORE:
            return
        
        super(HtmlTransform, self).start_tag(name, attrs)
        self._last_closed = None
    
    def end_tag(self, name):        
        if name in HTML_IGNORE:
            return
        # dont close tr/td more than once regardles of markup
        if self._last_closed == name and (name == 'tr' or name == 'td'):            
            return
        
        super(HtmlTransform, self).end_tag(name)
        self._last_closed = name
    
class HtmlParserProxy(HTMLParser):
    ''' Wraps HTMLParser to expose standard parsing interface for base Transform. '''
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.start_tag_handler = None
        self.end_tag_handler = None        
        self.data_handler = None
        self.entity_handler = None

    def handle_starttag(self, tag, attrs):        
        attributes = {}
        for a in attrs:
            attributes[a[0]] = a[1]        
        self.start_tag_handler(tag, attributes)
        
    def handle_endtag(self, tag):
        self.end_tag_handler(tag)
        
    def handle_data(self, data):
        self.data_handler(data)
        
    def handle_entityref(self, name):
        self.entity_handler(name)