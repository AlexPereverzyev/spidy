
''' High-level interface to Spidy scripts parsing and execution runtime. '''

__all__ = ['parse_file', 'parse_inline', 'exec_file', 'exec_inline']

import codecs
import tokenizer

from script_parser import *
from spidy.common import *

def parse_file(script_file, context):
    ''' Parses script file and builds syntax tree. '''    
    with codecs.open(script_file, "r", 'UTF8') as sf:
        script = sf.read()    
    return parse_inline(script, context)

def parse_inline(script, context):
    ''' Parses script string and builds syntax tree. '''    
    log.debug(context.get_id(), 'Builder: starting parsing script')
    lines = tokenizer.split_statements(script)
    context.set_script(lines)       
    sn = parse_script(context)
    log.debug(context.get_id(), 'Builder: parsed script')
    return sn

def exec_file(script_file, context):
    ''' Executes specified script file and returns results. '''    
    with codecs.open(script_file, "r", 'UTF8') as sf:
        script = sf.read()
    return exec_inline(script, context)

def exec_inline(script, context):
    ''' Executes specified script string and returns results. '''    
    log.debug(context.get_id(), 'Builder: starting parsing script')
    lines = tokenizer.split_statements(script)
    context.set_script(lines)    
    sn = parse_script(context)
    log.debug(context.get_id(), 'Builder: parsed script')
    log.debug(context.get_id(), 'Builder: evaluating syntax tree')
    sn.evaluate()
    log.debug(context.get_id(), 'Builder: evaluated syntax tree')
    output = context.get_return()       
    return output