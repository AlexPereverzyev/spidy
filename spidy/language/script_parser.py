
''' Spidy script statements parsing routines. '''

__all__ = ['parse_script']

from spidy.common import *
from syntax import *
from tokenizer import *

from script_node import ScriptNode
from get_node import GetNode
from skip_node import SkipNode
from set_node import SetNode
from return_node import ReturnNode
from ifelse_node import IfElseNode
from forin_node import ForInNode
from traverse_node import TraverseNode
from while_node import WhileNode
from break_node import BreakNode
from continue_node import ContinueNode
from inline_node import InlineNode
from merge_node import MergeNode
from log_node import LogNode
from header_node import *

def parse_script(context):
    ''' Parses script file from context, returns script node which can be evaluated. '''
    id = context.get_id()
    log.debug(id, 'ScriptParser: starting parsing')    
    line_num = 0
    lines = context.get_script()
    block = ScriptNode(context)
    block.parse(0)
    stack = [block]    
        
    while len(stack) > 0:
        
        # switch to nested script block
        block = stack.pop()    
        indent = get_indent(block.get_script_line())
             
        while line_num < len(lines):
            sline = lines[line_num] 
            line = sline.string
            
            # only allow parsing blocks with the same indentation
            line_indent = get_indent(line)
            validate(id, sline, indent == line_indent or not line_indent.startswith(indent),
                'ScriptParser: unmatched indentation')
            if indent != line_indent:
                break

            # try to parse first token as operator
            skip = False
            node = None
            new_block = None
            idx = skip_space(line)
            token_idx = skip_token(line[idx:])            
            op = line[idx:idx+token_idx]
            
            # headers are special
            if isinstance(block, HeadersNode):
                node = HeaderNode(context)
            
            elif op == OP_GET:
                node = GetNode(context)                
                if node.has_headers(line_num):
                    new_block = HeadersNode(context)
                    node.set_headers(new_block)

            elif op == OP_SKIP:
                node = SkipNode(context)

            elif op == OP_RETURN:
                node = ReturnNode(context)

            elif op == OP_IF:
                node = IfElseNode(context)
                new_block = ScriptNode(context)
                node.set_if_script(new_block)
                
            elif op == OP_ELSE:
                ifelse_node = block.get_statements()[-1]
                validate(id, sline, isinstance(ifelse_node, IfElseNode), 'ScriptNode: unmatched {0} statement'.format(OP_ELSE))
                ifelse_node.parse_else(line_num)
                new_block = ScriptNode(context)                
                ifelse_node.set_else_script(new_block)
         
            elif op == OP_FOR:
                node = ForInNode(context)                
                new_block = ScriptNode(context)
                node.set_body(new_block)
                
            elif op == OP_TRAVERSE:
                node = TraverseNode(context)
                new_block = ScriptNode(context)
                node.set_body(new_block)
                
            elif op == OP_WHILE:
                node = WhileNode(context)                
                new_block = ScriptNode(context)
                node.set_body(new_block)
            
            elif op == OP_BREAK:
                node = BreakNode(context)

            elif op == OP_CONTINUE:
                node = ContinueNode(context)
                
            elif op == OP_MERGE:
                node = MergeNode(context)
            
            elif op == OP_LOG:
                node = LogNode(context)
                
            else: # parse as expression
                node = InlineNode(context)
            
            line_num += 1

            # parse and add node and/or block to tree
            if node:
                node.parse(line_num-1)
                block.get_statements().append(node)
                
            if new_block:
                new_block.parse(line_num)
                stack.append(block)
                stack.append(new_block)
                break
       
    log.debug(id, 'ScriptParser: finished parsing')     
    return block