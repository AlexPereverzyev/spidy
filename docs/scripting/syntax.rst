.. _syntax:

================
Syntax Reference
================

Spidy is a dynamic single-context scripting language written in Python.
It borrows certain syntax specifics, like indentation, from Python, because
of it's clearness and simplicity and adds a few statements and operators
useful for Web scraping.

This documents describes Spidy language syntax, statements and operators.

Spidy Commands
==============

get
---

.. autoclass:: spidy.language.get_node.GetNode
    

skip
----

.. autoclass:: spidy.language.skip_node.SkipNode

traverse
--------

.. autoclass:: spidy.language.traverse_node.TraverseNode

for...in
--------

.. autoclass:: spidy.language.forin_node.ForInNode

while
-----

.. autoclass:: spidy.language.while_node.WhileNode

break
-----

.. autoclass:: spidy.language.break_node.BreakNode

continue
--------

.. autoclass:: spidy.language.continue_node.ContinueNode

if...else
---------

.. autoclass:: spidy.language.ifelse_node.IfElseNode

merge
-----

.. autoclass:: spidy.language.merge_node.MergeNode

log
---

.. autoclass:: spidy.language.log_node.LogNode

return
------

.. autoclass:: spidy.language.return_node.ReturnNode

Spidy Operators
===============

Spidy syntax supports all basic arithmetic, logical and comparison 
operators as well as some custom ones, e.g.: XPath ``&`` or ``%`` regex.
The table below describe operators precedence:

================ ==============
    Operator       Precedence 
================ ==============
  x[index]             13
---------------- --------------
  >>, <<, &            12
---------------- --------------
-x, +x, $, #, %        11
---------------- --------------
  /                    10
---------------- -------------- 
  \*                   9
---------------- --------------
  \-                   8
---------------- --------------
  \+                   7
---------------- --------------
==,!=,<,>,<=,>=        6
---------------- --------------
  in                   5
---------------- --------------
  not                  4
---------------- --------------
  and                  3
---------------- --------------
  or                   2
---------------- --------------
  =                    1
================ ==============

Containment Test
----------------

``in`` operator is applicable to lists or strings.

.. note:: When used with strings, ``in`` always compares strings in lower case.

Lists
-----

**Instantiating**::

    list = []
    list = [1,2,3]

**Indexer**::

    list = [1,2,3]
    second = list[1]

**Pop** ``>>``:

.. autoclass:: spidy.language.pop_node.PopNode

**Push** ``<<``:

.. autoclass:: spidy.language.push_node.PushNode

Type Conversion
---------------

**To string** ``$``::

    number = 1010101
    string = $number
    
**To number** ``#``::

    string = '1010101'
    number = #string

XPath
-----

.. autoclass:: spidy.language.path_node.PathNode

Regex
-----

.. autoclass:: spidy.language.regex_node.RegexNode

Comments
--------

``//``::    
    
    // initialize
    log 'warming up...'
    host = 'http://somehost.org''

Grammar Definition
==================

Spidy grammar in slightly modified Extended Backus–Naur Form. Primitive types,
e.g.: string, bool are omitted::

    script           =  statement*
    
    statement        = for_stmnt
                     | traverse_stmnt
                     | while_stmnt
                     | break_stmnt
                     | continue_stmnt
                     | if_stmnt
                     | else_stmnt
                     | get_stmnt
                     | skip_stmnt
                     | return_stmnt
                     | merge_stmnt
                     | log_stmnt
                     | expression 
    
    for_stmnt        =  "for" identity "in" list ":"
    
    break_stmnt      =  "break"
    
    continue_stmnt   =  "continue"
    
    while_stmnt      =  "while" bool:
    
    traverse_stmnt   =  "traverse" identity "in" path [mode depth]

    path             =  & | &string
    
    mode             =  breadthfirst | depthfirst
    
    depth            =  number
    
    if_stmnt         =  "if" bool ":"
    
    else_stmnt       =  "else:"
    
    get_stmnt        =  "get" string[":"]
                           [header_stmnt]
    
    header_stmnt     =  string ":" string
    
    skip_stmnt       =  "skip" path [direction]
    
    direction        =  forward | reverse
    
    return_stmnt     =  "return" [expression]
    
    merge_stmnt      =  "merge" template_string "as" identity
    
    log_stmnt        =  “log” string
    
    expression       =  value
                     | "(" ")" | "(" e ")" |   "-"   e |   "+"  e     
                     | e "+" e | e "-"  e  | e "*"   e | e "/"  e  
                     | e "<" e | e "<=" e  | e "=="  e | e "!=" e
                     | e ">" e | e ">=" e 
                     | "not" e | e "or" e  | e "and" e | e "in" e
                     |  path   |  "#" e    | "$" e     | e "%"  e
                     | indexer 
                     |(indexer | identity) = e         
                     |(indexer | list) << e 
                     |(indexer | list) >> (indexer | identity)
    
    e                =  expression
    
    value            =  none | number | string | bool | list
    
    list             =  "[" [e ("," e)*] "]"
    
    indexer          =  e "[" e "]"