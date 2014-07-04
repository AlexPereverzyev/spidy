
''' Script statements split and operators parsing routines. '''

from syntax import *
from spidy.common.context import ScriptLine
        
def split_statements(script):
    ''' Splits script file into list of statements.
        Replaces pairs \t and \n with tab and line feed in strings. '''    
    i = 0
    lines = []
    line_count = 0
    line = EMPTY
    is_string = EMPTY    
    
    while i < len(script):
        char = script[i]
        
        if char in STRING:
            if is_string == EMPTY:
                is_string = char        
            elif is_string == char and script[i-1] != BACKSLASH:
                is_string = EMPTY
                
        # chop out line
        if is_string == EMPTY and char == LINEFEED:            
            line_strip = line.strip()                
            if line_strip != EMPTY and not line_strip.startswith(COMMENT):
                lines.append(ScriptLine(line_count, line))
            line_count += 1    
            line = EMPTY
            
        # implement control symbols
        elif (is_string != EMPTY
              and char == BACKSLASH 
              and (i-1) >= 0
              and (i+1) < len(script)
              and script[i-1] != BACKSLASH):
            
            if (script[i+1] == 'n'):
                line += LINEFEED
                i += 1
            elif (script[i+1] == 't'):
                line += TAB
                i += 1
        else:
            line += char

        i += 1   
        
    line_strip = line.strip()                
    if line_strip != EMPTY and not line_strip.startswith(COMMENT):
        lines.append(ScriptLine(line_count, line))
        
    return lines

def read_operator(string, next_char):
    ''' Reads operator from the string. '''    
    s = WHITESPACE + string + next_char    
    result = OPERATOR_PATTERN.search(s)
    if result != None:
        g = 1 + (result.group(2) != None)
        return result.group(g)
    return ''

def skip_token(string):
    ''' Returns index of sub-string after skiping token. '''    
    i = 0    
    char = string[i]
    string += WHITESPACE # sentinel
    
    while i < len(string) and char != COLON and char not in ALL_SEPARATORS:
        i += 1
        char = string[i]
    return i

def skip_space(string):
    ''' Returns index of sub-string after skipping whitespaces or tabs. '''    
    i = 0
    char = SPACE[0]    
    while i < len(string) and char in SPACE:
        char = string[i]
        i += 1
    return i - 1

def strip_parenths(string):
    ''' Removes both parenthesis (ignores strings), strips whats left. '''    
    s = ''
    char = ''
    is_string = ''
    i = 0    
    while i < len(string):
        char = string[i]
        
        if char in STRING:
            if is_string == '':
                is_string = char        
            elif is_string == char and string[i-1] != BACKSLASH:
                is_string = ''
                
        if (is_string != '' or
            is_string == '' and char != LEFT_PAREN and char != RIGHT_PAREN):
            s += char
            
        i += 1        
    return s.strip()