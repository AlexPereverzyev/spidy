
''' Script statements split and operators parsing routines. '''

from syntax import *
from spidy.common.context import ScriptLine
        
def split_statements(script):
    ''' Splits script file into list of statements. Also does the following:
        
        - Completely strips comments and removes empty lines.
        - Replaces pairs \t and \n with tab and line feed in strings.        
        - Allows multiline statements if nested inside of parenthesis or
          square brackets. '''
    lines       = []
    i           = -1
    line_count  = 0         # total lines counter
    line_span   = 1         # counts line span for multiline statements
    nesting     = 0         # counts level of nesting in () or []
    is_comment  = 0         # 1 if reading commented out line
    line        = EMPTY     # accumulated line to add
    is_string   = EMPTY     # contains ' or " when reading string content    
    
    while i < len(script) - 1:
        i += 1
        char = script[i]
        
        # detect and skip commented out lines
        if (not is_comment and is_string == EMPTY
            and char == SLASH and len(line) > 0 and line[-1] == SLASH):
            line        = line[:-1]
            is_comment  = 1            
            continue
        
        elif is_comment and char == LINEFEED:
            is_comment = 0
            line_count += 1
            
            # reset indent - comment not inside of multiline statement
            if line.strip() == EMPTY:
                line = EMPTY
                
            # chop out completed line w/ inline comment
            elif nesting <= 0:                
                lines.append(ScriptLine(line_count, line))
                line_span   = 1
                nesting     = 0
                line        = EMPTY
                
            continue
        
        elif is_comment:
            continue
        
        # detect string content
        elif char in STRING:
            if is_string == EMPTY:
                is_string = char        
            elif is_string == char and script[i-1] != BACKSLASH:
                is_string = EMPTY
        
        # detect multiline statements nested inside of parenthesis
        elif is_string == EMPTY and (char == LEFT_PAREN or char == LEFT_SQUARE):
            nesting += 1
            
        elif is_string == EMPTY and (char == RIGHT_PAREN or char == RIGHT_SQUARE):
            nesting -= 1
        
        # chop out line, ignore empty lines
        if  char == LINEFEED and is_string == EMPTY and nesting <= 0:
            if line.strip() != EMPTY:
                lines.append(ScriptLine(line_count, line))            
            line_count += line_span
            line_span   = 1
            nesting     = 0
            line        = EMPTY                                    
            
        # implement control symbols in strings
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
                
        # accumulate statement string, skip nested line feeds
        elif char != LINEFEED or nesting <= 0:
            line += char
        
        # reached when previous is not satisfied - ending multiline statement's line
        else:
            line_span += 1
        
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