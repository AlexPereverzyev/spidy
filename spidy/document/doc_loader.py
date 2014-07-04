
''' High-level document loading routines and helper methods. '''

__all__ = ['DocType', 'DocSource', 'LoadMode', 'DocLoader',
           'from_file', 'from_web', 'detect_doc_source', 'detect_doc_type',
           'get_file_dir', 'join_path']

import codecs

from spidy.common import *
from web_client import *

from txt_transform import TxtTransform
from xml_transform import XmlTransform
from html_transform import HtmlTransform
from html_form import HtmlForm
from json_transform import JsonTransform

class DocType:
    ''' Enumerates supported document types. '''    
    UNKNOWN  = 'UNKNOWN'
    TXT      = 'TXT'
    XML      = 'XML'
    HTML     = 'HTML'
    JSON     = 'JSON'
    
class DocSource:
    ''' Enumerates supported document sources. '''    
    UNKNOWN = 0
    FILE    = 1
    WEB     = 2

class LoadMode:
    ''' Enumerates document load modes. '''
    LOAD = 0
    LOAD_PARSE = 1
    LOAD_PARSE_REFACTOR = 2

class DocLoader(object):
    ''' Provides high-level document loading routines. '''
    
    _doc_type = DocType.UNKNOWN
    _doc_raw = None
    _doc = None
        
    def get_doc_type(self):
        return self._doc_type
    
    def get_doc_raw(self):
        return self._doc_raw
    
    def get_doc(self):
        return self._doc

    def load(self, file_uri, doc_type, headers = None, mode = LoadMode.LOAD_PARSE_REFACTOR):
        ''' Loads document either from file or from URI. '''
        
        # resolve doc format
        dt = doc_type.upper()
        if dt == DocType.UNKNOWN:
            dt = detect_doc_type(file_uri)            
        if dt == DocType.UNKNOWN:
            raise DocumentException('DocumentLoader: document format can\'t be resolved')        
        self._doc_type = dt
        
        # load document
        doc_src = detect_doc_source(file_uri)
        if doc_src == DocSource.FILE:
            self._doc_raw = from_file(file_uri)            
        elif doc_src == DocSource.WEB:
            self._doc_raw = from_web(file_uri, headers)
        else:
            raise DocumentException('DocumentLoader: document source is not supported')
        
        if mode == LoadMode.LOAD:
            return
        
        # parse document
        parser = None
        fixer = None
        if dt == DocType.TXT:
            parser = TxtTransform()
            
        elif dt == DocType.XML:
            parser = XmlTransform()
            
        elif dt == DocType.HTML:
            parser = HtmlTransform()
            fixer = HtmlForm()
            
        elif dt == DocType.JSON:
            parser = JsonTransform()
            
        else:
            raise DocumentException('DocumentLoader: document format is not supported')
        
        self._doc = parser.perform(self._doc_raw)
                
        if mode == LoadMode.LOAD_PARSE:
            return
        
        # try to refactor document
        if fixer != None and len(self._doc) > 0:
            fixer.refactor(self._doc)
        
def from_file(file_name):
    ''' Loads document from file. OS-independent. '''
    with codecs.open(file_name, "r", 'UTF8') as df:
        doc = df.read()
    return doc

def from_web(file_url, headers):
    ''' Loads document from Web (URL). '''
    wc = WebClient()
    doc = wc.get(file_url, headers)
    return doc 

def detect_doc_source(file_url):
    ''' Tries to determine document source by it's URL. '''
    if WEB_URL_PATTERN.match(file_url) != None:
        return DocSource.WEB
    return DocSource.FILE
    
def detect_doc_type(file_name):
    ''' Tries to determine document type by it's extension. '''
    fn = file_name.upper()    
    if   fn.endswith('.' + DocType.TXT):
        return DocType.TXT
    elif fn.endswith('.' + DocType.XML):
        return DocType.XML
    elif fn.endswith('.' + DocType.HTML):
        return DocType.HTML
    elif fn.endswith('.' + DocType.JSON):
        return DocType.JSON
    else:
        return DocType.UNKNOWN
    
def get_file_dir(file_name):
    ''' Tries to exctract path to file directory from it's full name. '''
    idx = file_name.rfind('/')     
    if idx != -1:
        return file_name[:idx]
    return ''

def join_path(path, file_name):
    ''' Joins path with short file name. If file name is full file name - 
		returns just it. '''    
    full_name = file_name
    sep = '/'
    if path != None and path != '' and not sep in file_name:        
        if path.endswith(sep):
            sep = ''
        full_name = (path + sep + file_name)
    return full_name