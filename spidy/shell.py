
''' Spidy shell: routines to check and execute scripts and analyze documents. '''

__all__ = ['run', 'do', 'check_file', 'check', 'read']

import codecs

from exceptions import Exception
from spidy.language import *
from spidy.common import *
from spidy.document import *

def run(script_file, out_file = None, log_file = None, log_level = 20):
    ''' Opens and executes script file and returns output. '''
    
    context = Context()
    id = context.get_id()
    log.setup(id, log_file, log_level)
    log.info(id, 'Spidy: executing script file: {0}'.format(script_file))
    script_dir = get_file_dir(script_file)
    context.set_dir(script_dir)
    
    output = None
    try:
        output = exec_file(script_file, context)
        log.info(id, 'Spidy: finished executing script file: {0}'.format(script_file))
        if out_file != None:
            log.info(id, 'Spidy: writing output to file: {0}'.format(out_file))
            if output == None: output = ''
            with codecs.open(out_file, 'w', 'UTF8') as f:
                f.write(output)
            log.info(id, 'Spidy: finished writing output: {0}'.format(out_file))
            output = ''
            
    except Exception as e:
        log.critical(id, "Spidy: failed to execute script: {0}".format(script_file))
        raise e
    finally:
        log.dispose(id)
    return output

def do(script, out_file = None, log_file = None, log_level = 20):
    ''' Executes script and returns output. '''

    context = Context()    
    id = context.get_id()
    log.setup(id, log_file, log_level)
    script_name = script.lstrip()[:20]
    log.info(id, 'Spidy: executing script: {0}...'.format(script_name))
    
    output = None
    try:
        output = exec_inline(script, context)
        log.info(id, 'Spidy: finished executing script: {0}...'.format(script_name))
        if out_file != None:            
            log.info(id, 'Spidy: writing output to file: {0}'.format(out_file))
            if output == None: output = ''
            with codecs.open(out_file, 'w', 'UTF8') as f:
                f.write(output)
            log.info(id, 'Spidy: finished writing output: {0}'.format(out_file))
            output = ''
    
    except Exception as e:
        log.critical(id, "Spidy: failed to execute script: {0}".format(script_name))
        raise e
    finally:
        log.dispose(id)
    return output

def check_file(script_file, log_file = None, log_level = 20):
    ''' Checks specified script file for syntax errors. '''
    context = Context()    
    id = context.get_id()
    log.setup(id, log_file, log_level)
    log.info(id, 'Spidy: checking script file: {0}...'.format(script_file))    
    output = False
    try:
        parse_file(script, context)
        output = True
    except:
        pass
    finally:
        log.info(id, 'Spidy: finished checking script file: {0}...'.format(script_file))
        log.dispose(id)
    return output

def check(script, log_file = None, log_level = 20):
    ''' Checks specified script string for syntax errors. '''    
    context = Context()    
    id = context.get_id()
    log.setup(id, log_file, log_level)
    script_name = script.lstrip()[:20]
    log.info(id, 'Spidy: checking script: {0}...'.format(script_name))
    output = False
    try:
        parse_inline(script, context)
        output = True
    except:
        pass
    finally:
        log.info(id, 'Spidy: finished checking script: {0}...'.format(script_name))
        log.dispose(id)
    return output

def read(url, doc_type = DocType.UNKNOWN, mode = LoadMode.LOAD_PARSE_REFACTOR, out_file = None, log_file = None, log_level = 20):
    ''' Shows documnet tag-tree.
        Optional arguments allow to specifiy document format, output file name and additional processing. '''
    
    context = Context()
    id = context.get_id()
    log.setup(id, log_file, log_level)
    log.info(id, 'Spidy: reading document: {0}'.format(url))
    
    output = None
    doc_loader = DocLoader()
    try:
        doc_loader.load(url, doc_type, None, mode)
        
        output = ''
        if doc_loader.get_doc() != None:    
            for r in doc_loader.get_doc():
                output += str(r)
        elif doc_loader.get_doc_raw() != None:
            output = doc_loader.get_doc_raw()
            
        log.info(id, 'Spidy: finished reading document: {0}'.format(url))
        if out_file != None:            
            log.info(id, 'Spidy: writing document to file: {0}'.format(out_file))
            if output == None: output = ''
            with codecs.open(out_file, 'w', 'UTF8') as f:
                f.write(output)
            log.info(id, 'Spidy: finished writing document: {0}'.format(out_file))
            
    except Exception as e:
        log.error(id, 'Load document error: {0}'.format(str(e)))
    finally:
        log.dispose(id)
    return output