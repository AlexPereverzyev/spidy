
''' Regex '%' operator evaluation routines. '''

import re
import syntax

from spidy.common import *
from nodes import BinaryNode

class RegexNode(BinaryNode):
    '''
    Regex operator allows to extract sub-string from strings using capturing groups.
    If two or more capturing groups are specified, operator returns list of captured
    values.
    
    Note, if regex is matched agains list, regex is matched against every list
    item same way it's matched against single value. Eventually left and right operands
    should be of string type, otherwise evaluation exception is raised.
    
    Regex operator tries to find all matches in the input string, not just stops
    at the first match. If two or more matches found, operator returns list of
    matches. The resulting list size is multiple of matches and number of capturing
    groups specified.
    
    If capturing groups are omitted, operator returns the whole match - same
    way standard regex does.
    
    Example::
    
        r = 'hello, John!' % 'hello, ([a-zA-Z]+)!'
        
    will result in: ``'John'``.
        
    Or for list of strings::
        
        r = ['hello, John!', 'hello, Kate!'] % 'hello, ([a-zA-Z]+)!'
        
    returns the following list: ``['John', 'Kate']`` 
    '''
    
    def evaluate(self):
        log.debug(self._id, 'RegexNode: evaluating')
        
        # eval and validate operands
        target = self._left.evaluate()
        regex = self._right.evaluate()        
        is_list = isinstance(target, list) 
        
        validate_eval(self._id, self._sline,
            target != None
            and (isinstance(target, basestring)
            or is_list and all(s != None and isinstance(s, basestring) for s in target)),
            'RegexNode: left operand should be of string or list of strings type')
        
        validate_eval(self._id, self._sline,
            regex != None and isinstance(regex, basestring),
            'RegexNode: right operand should be of string type')

        # abstract from single value
        result_lst = []
        target_lst = target
        if not is_list:
            target_lst = [target]
        
        # now do regex search on each list item, never return None        
        compiled_regex = re.compile(regex)
        
        for s in target_lst:
            captures = compiled_regex.findall(s)
            
            if captures == None or len(captures) == 0:
                result_lst.append('')
                continue
        
            # need to flatten before appending - not for plain strings thou
            flat_captures = []
            for match in captures:
                if isinstance(match, basestring):
                    flat_captures.append(match)
                else:
                    flat_captures.extend(match)

            # append single-item lists as values
            if len(flat_captures) > 1:
                result_lst.append(flat_captures)
            else:
                result_lst.append(flat_captures[0])
        
        # back to single value, if needed
        if not is_list:
            return result_lst[0]
        else:
            return result_lst
    
    def __str__(self):
        return str(self._left) + syntax.WHITESPACE + syntax.OP_REGEX + syntax.WHITESPACE + str(self._right)