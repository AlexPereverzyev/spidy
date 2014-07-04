
''' 'merge' statement parsing and evaluation. '''

import syntax
import exp_parser

from string import Template
from spidy.common import *
from spidy.document.doc_loader import *
from nodes import Node

class MergeNode(Node):
    '''
    Merges current execution context (all defined variables at the step) with
    specified template and stores result in variable. Defines new variable if
    not exists.
    
    The statement uses standard Python string template syntax, e.g.::
    
        Hello, ${name}!
        
    Having variable name set to 'Alex' results in::
    
        Hello, Alex!
        
    Example::
    
        merge 'master_page.html' as page
    '''
    
    _ident = None
    _template = None
        
    def get_ident(self):
        return self._ident
    
    def set_ident(self, ident):
        self._ident = ident
        
    def get_template(self):
        return self._template
    
    def set_template(self, template):
        self._template = template
        
    def evaluate(self):
        log.debug(self._id, 'MergeNode: evaluating')        
        
        # load template from file        
        template_file = self._template.evaluate()
        validate_eval(self._id, self._sline, template_file != None and template_file.strip() != '',
            'MergeNode: template should be specified')

        # load template file
        template_file = join_path(self._context.get_dir() , template_file)
        doc_loader = DocLoader()
        doc_loader.load(template_file, DocType.TXT, mode = LoadMode.LOAD)
        template = doc_loader.get_doc_raw()
        
        # merge context with the template
        t = Template(template)
        bs = self._context.get_bindings()
        r = t.safe_substitute(bs)        
        self._context.make_var(self._ident, r)    

    def parse(self, line_num):
        log.debug(self._id, 'MergeNode: parsing')
        self._sline = self._context.get_script()[line_num]
        line = self._sline.string
        idx = line.index(syntax.OP_MERGE) + len(syntax.OP_MERGE)
        template_exp = line[idx:].strip()
        
        # parse template name
        ep = exp_parser.ExpressionParser(self._context, line_num)
        self._template = ep.parse(template_exp)
        
        # parse output variable name
        stop_word = ep.get_stop_word()
        validate(self._id, self._sline, stop_word != None and stop_word != '' and stop_word == syntax.OP_AS, 'MergeNode: invalid syntax')
        ident_idx = ep.get_stop_idx() + len(stop_word)
        ident = template_exp[ident_idx:].strip()
        validate(self._id, self._sline, syntax.is_var_name(ident), 'MergeNode: invalid output variable name')        
        self._ident = ident

    def __str__(self):
        string = syntax.OP_MERGE + syntax.WHITESPACE + str(self._template) + syntax.WHITESPACE + syntax.OP_AS + syntax.WHITESPACE + self._ident        
        return string