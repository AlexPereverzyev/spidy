
''' Wraps Python logging module and exposes context-specific interface. '''

__all__ = ['setup', 'dispose', 'debug', 'info', 'warning', 'error', 'critical']

import logging 

def setup(id, logfile, level):
    ''' Initializes new logging session. '''
    logger = logging.getLogger(id)
    logger.setLevel(level)
    
    handler = None
    if logfile != None:
        handler = logging.FileHandler(logfile, 'w')
    else:
        handler = logging.StreamHandler()
    
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    
def dispose(id):
    ''' Closes logging session. '''
    logger = logging.getLogger(id)
    for h in logger.handlers[:]:
        h.close()
        logger.removeHandler(h)

def debug(id, string):
    ''' Logs debug message. '''
    logging.getLogger(id).debug(string)
    
def info(id, string):
    ''' Logs info message. '''
    logging.getLogger(id).info(string)
        
def warning(id, string):
    ''' Logs warning message. '''
    logging.getLogger(id).warning(string)
    
def error(id, string):
    ''' Logs error message. '''
    logging.getLogger(id).error(string)
    
def critical(id, string):
    ''' Logs critical error message. '''
    logging.getLogger(id).critical(string)