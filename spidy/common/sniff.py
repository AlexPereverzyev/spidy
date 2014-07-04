
''' Common data types sniffing routines. '''
    
_TRUE = 'True'
_FALSE = 'False'
_QUOTE_SINGLE = '\''
_QUOTE_DOUBLE = '"'
    
def is_none(string):
    ''' Returns value which indicates whether the string represents None value. '''    
    return string == 'None'

def is_const(string):
    ''' Returns value which indicates whether the string represents a constant (number or string). '''    
    return is_number_const(string) or is_string_const(string)

def is_int(string):
    ''' Returns True if the string can be converted to integer number. '''
    try:
        int(string)
        return True
    except ValueError:
        return False

def is_number_const(string):
    ''' Returns value which indicates whether the string represents a number constant. '''    
    try:
        float(string)
        return True
    except ValueError:
        return False
    
def is_bool_const(string):
    ''' Returns value which indicates whether the string represents a boolean constant. '''    
    return string == _TRUE or string == _FALSE
    
def is_string_const(string):
    ''' Returns value which indicates whether the string represents a string constant. '''
    
    return string != None and (
           string.startswith(_QUOTE_DOUBLE) and string.endswith(_QUOTE_DOUBLE) or
           string.startswith(_QUOTE_SINGLE) and string.endswith(_QUOTE_SINGLE))