
''' High-level error handling and exception raising routines and classes. '''

__all__ = ['validate', 'validate_eval', 'raise_eval', 'format_msg',
           'ParsingException', 'EvaluationException', 'DocumentException', 'WebException']

import log

from exceptions import Exception

def validate(id, sline, expression, message):
    ''' If expression is False, logs critical error and raises ParsingException. '''    
    if not expression:
        msg = format_msg(message, sline.string, sline.number)
        log.critical(id, msg)
        raise ParsingException(msg)
    
def validate_eval(id, sline, expression, message):
    ''' If expression is False, logs critical error and raises EvaluationException. '''    
    if not expression:
        msg = format_msg(message, sline.string, sline.number)
        log.critical(id, msg)
        raise EvaluationException(msg)
    
def raise_eval(id, sline, message):
    ''' Raises EvaluationException with message and line number. '''
    msg = format_msg(message, sline.string, sline.number)
    log.critical(id, msg)
    raise EvaluationException(msg)

def format_msg(message, line, lnum):
    ''' Fromats and returns error message with line number. '''
    return '{0}, line {2}: {1}'.format(message, line.strip(), lnum+1)

class ExceptionWithArgs(Exception):
    ''' Generic exception with message. '''
    def __init__(self, *args):
        self.args = [a for a in args]
        
class ParsingException(ExceptionWithArgs):
    ''' Raised by synatax tree nodes, during parsing. '''
    pass
        
class EvaluationException(ExceptionWithArgs):
    ''' Raised by synatax tree nodes, during evaluation. '''
    pass

class DocumentException(ExceptionWithArgs):
    ''' Raised by document doc_loader. '''
    pass

class WebException(ExceptionWithArgs):
    ''' Raised by web client. '''
    pass