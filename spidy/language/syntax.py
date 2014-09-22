
''' Spidy scripting language operators, precedence, syntax rules and stop words. '''

import re

# constants
EMPTY = ''
WHITESPACE = ' '
TAB = '\t'
LINEFEED = '\n'
COLON = ':'
LEFT_PAREN = '('
RIGHT_PAREN = ')'
LEFT_SQUARE = '['
RIGHT_SQUARE = ']'
QUOTE_SINGLE = '\''
QUOTE_DOUBLE = '"'
BACKSLASH = '\\'
SLASH = '/'
COMMENT = '//'
COMMA = ','
DOT = '.'
UNDERSCORE = '_'

# operators
OP_GET = 'get'
OP_SKIP = 'skip'
OP_SET = '='
OP_RETURN = 'return'
OP_IF = 'if'
OP_ELSE = 'else'
OP_FOR = 'for'
OP_TRAVERSE = 'traverse'
OP_WHILE = 'while'
OP_IN = 'in'
OP_AS = 'as'
OP_BREAK = 'break'
OP_CONTINUE = 'continue'
OP_OR = 'or'
OP_AND = 'and'
OP_NOT = 'not'
OP_PLUS = '+'
OP_MINUS = '-'
OP_MULT = '*'
OP_DIVIDE = '/'
OP_UNARY_MINUS = 'u-'
OP_UNARY_PLUS = 'u+'
OP_EQUALS = '=='
OP_NOT_EQUALS = '!='
OP_LESS = '<'
OP_LESS_OR_EQUALS = '<='
OP_GREATER = '>'
OP_GREATER_OR_EQUALS = '>='
OP_PATH = '&'
OP_CONVERT_TO_NUM = '#'
OP_CONVERT_TO_STR = '$'
OP_ATTRIBUTE = '@'
OP_INDEXER = '[]'
OP_LIST = '[,]'
OP_PUSH = '<<'
OP_POP = '>>'
OP_MERGE = 'merge'
OP_LOG = 'log'
OP_REGEX = '%'

MARK_UNARY = 'u'

class TraverseMode:
    ''' Enumerates document traverse modes. '''
    DEPTH_FIRST     = 'depthfirst'
    BREADTH_FIRST   = 'breadthfirst'

class SkipDirection:
    ''' Enumerates document skip directions. '''
    FORWARD         = 'forward'
    REVERSE         = 'reverse'

# operators precedence 
OPS_PREC            = { OP_INDEXER:12,
                        OP_POP:11, OP_PUSH:11, OP_PATH:11,
                        OP_UNARY_MINUS:10, OP_UNARY_PLUS:10, OP_CONVERT_TO_NUM:10, OP_CONVERT_TO_STR:10, OP_REGEX:10,
                        OP_PLUS:6, OP_MINUS:7, OP_MULT:8, OP_DIVIDE:9,
                        OP_EQUALS:5, OP_NOT_EQUALS:5, OP_LESS:5, OP_LESS_OR_EQUALS:5, OP_GREATER:5, OP_GREATER_OR_EQUALS:5,
                        OP_OR:1, OP_AND:2, OP_NOT:3, OP_IN:4,
                        OP_SET:0 }

# syntax rules used by expression parser
OPS_CAN_BE_UNARY    = [OP_NOT, OP_MINUS, OP_PLUS, OP_PATH, OP_CONVERT_TO_NUM, OP_CONVERT_TO_STR]
OPS_UNARY           = [OP_NOT, OP_UNARY_MINUS, OP_UNARY_PLUS, OP_PATH, OP_CONVERT_TO_NUM, OP_CONVERT_TO_STR]
OPS_LOGICAL         = [OP_NOT, OP_OR, OP_AND, OP_IN]
OPS_ASSIGNMENT      = [OP_SET, OP_POP, OP_PUSH]
OPS_INCOMPLETE      = [OP_POP, OP_PATH]
OPS_SEPARATORS      = [OP_MINUS, OP_PLUS, OP_PATH, OP_CONVERT_TO_NUM, OP_CONVERT_TO_STR]

# operator separators definitions
SPACE               = [EMPTY, WHITESPACE, TAB]
STRING              = [QUOTE_SINGLE, QUOTE_DOUBLE]
SEPARATORS          = [LEFT_PAREN, RIGHT_PAREN, LEFT_SQUARE, RIGHT_SQUARE]
ALL_SEPARATORS      =  SPACE + STRING + SEPARATORS + OPS_SEPARATORS

# expression parser stop words
PARSER_STOPWORDS    = [TraverseMode.BREADTH_FIRST, TraverseMode.DEPTH_FIRST,
                       SkipDirection.FORWARD, SkipDirection.REVERSE,
                       OP_AS, COMMENT]

# regex to perform header name validation
HEADER_PATTERN      = re.compile('[a-zA-Z\-]')

# regex to perform identity name validation
IDENTITY_PATTERN    = re.compile('^(?!({0}|{1}|{2}|{3}|{4}|{5}|{6}|{7}|{8}|{9}|{10}|{11}|{12}|{13}|{14}|{15}|{16}|{17}|{18}|{19}|{20})$)[a-zA-Z_][a-zA-Z0-9_]*$'
                            .format(
                                OP_GET, OP_SKIP, OP_RETURN, OP_IF, OP_ELSE, OP_FOR, OP_TRAVERSE, OP_WHILE, OP_MERGE,
                                TraverseMode.DEPTH_FIRST, TraverseMode.BREADTH_FIRST,
                                SkipDirection.FORWARD, SkipDirection.REVERSE,
                                OP_AS, OP_BREAK, OP_CONTINUE,
                                OP_AND, OP_OR, OP_NOT, OP_IN,
                                OP_LOG))

# regex to perform operator matching
OPERATOR_PATTERN = re.compile(
    '{0}({1}|{2}|{3}|{4}|{5}|{6}|{7}|{8}|{25}){0}|({9}(?!{9})|{10}(?!{9}|{10})|{11}(?!{9}|{11})|{12}|{13}|{14}|{15}|{16}|{17}|\{18}|\{19}|\{20}|{21}(?!{21})|\{22}|{23}|\{24}|{26})(?!$)'
        .format(
            '[{0}{1}\{2}{3}{4}{5}{6}\{7}\{8}\{10}{11}\{12}\{9}]'
                .format(
                    WHITESPACE, TAB,
                    QUOTE_SINGLE, QUOTE_DOUBLE,
                    LEFT_PAREN, RIGHT_PAREN, LEFT_SQUARE, RIGHT_SQUARE,
                    OP_MINUS, OP_PLUS, OP_PATH,
                    OP_CONVERT_TO_NUM, OP_CONVERT_TO_STR),
            SkipDirection.FORWARD, SkipDirection.REVERSE,
            TraverseMode.DEPTH_FIRST, TraverseMode.BREADTH_FIRST,
            OP_AS,
            OP_AND, OP_OR, OP_NOT,        
            OP_SET, OP_LESS, OP_GREATER,
            OP_PUSH, OP_POP,
            OP_EQUALS, OP_NOT_EQUALS, OP_LESS_OR_EQUALS, OP_GREATER_OR_EQUALS,
            OP_PLUS, OP_MINUS, OP_MULT, OP_DIVIDE,
            OP_PATH, OP_CONVERT_TO_NUM, OP_CONVERT_TO_STR,
            OP_IN, OP_REGEX))

def to_unary(operator):
    ''' Marks operator as unary for consistant precedence (only for + and -). '''
    if operator == OP_PLUS or operator == OP_MINUS:
        operator = MARK_UNARY + operator
    return operator

def is_incomplete(operator):
    ''' Returns value which indicates whether the operator may not be complete. '''    
    return operator in OPS_INCOMPLETE

def is_assignment(operator):
    ''' Returns value which indicates whether the operator is assignment or pop/push. '''    
    return operator in OPS_ASSIGNMENT

def is_logical(operator):
    ''' Returns value which indicates whether the operator is logical. '''    
    return operator in OPS_LOGICAL

def is_unary(operator):
    ''' Returns value which indicates whether the operator is unary. '''    
    return operator in OPS_UNARY

def can_be_unary(operator):
    ''' Returns value which indicates whether the operator can be unary (+,-). '''
    return operator in OPS_CAN_BE_UNARY

def is_var_name(string):
    ''' Returns value which indicates that the string is a valid variable name. '''
    return string != None and IDENTITY_PATTERN.match(string) != None

def is_header_name(string):
    ''' Returns value which indicates that the string is a valid header name. '''
    return string != None and HEADER_PATTERN.match(string) != None

def get_indent(string):
    ''' Returns string indentation. '''    
    indent = ''
    i = 0
    while i < len(string) and (string[i] == WHITESPACE or string[i] == TAB):
        indent += string[i]
        i += 1        
    return indent

def is_indented_block(two_lines):
    ''' Returns value which indicates whether two lines are mutually indented. '''    
    first_line = two_lines[0]
    first_indent = get_indent(first_line)    
    second_line = two_lines[1]
    second_indent = get_indent(second_line)    
    return second_indent.startswith(first_indent) and len(first_indent) < len(second_indent)