
.. _general:

====================
General Syntax Rules
====================

Spidy is a dynamic domain-specific single-context scripting language written
in Python. It borrows certain syntax specifics, like indentation, from Python,
because of it's clearness and simplicity and adds a few statements and operators
useful for Web scraping.

Here *single-context* means that the language doesn't have functions, 
procedures or method calls - everything is handled by commands or operators.
Thou, to some extent, notion of context is present in nested blocks - see below.

Spidy's script files are composed of statements or, we can say, each file
can be represented by a list of statements which executed sequentially.
With some exceptions (more about it will follow shortly), every line of script
code considered a statement.

Statement itself can be a command or an expression. Some statements can have
nested blocks of statements, e.g.: ``if...else`` statement, others can have
optional nested blocks, like ``get`` statement may have optional nested headers
block. Block nesting is specified by indentation, in other words, nested statements
from the same block should have the same indentation. The rule is borrowed from
Python.

In some cases, statements can span multiple lines, but only if they wrapped
into parenthesis or square brackets. This way Spidy parser is able to detect
and properly parse multiline instructions allowing for better script code
formatting.

Expressions are combined of operators and operands and also can be nested
into each other using parenthesis. There is nothing fancy, however you may
want to check out the full list of whats supported by Spidy parser here
:ref:`syntax`.

Finally, each script line can be commented out by a ``//`` sequence at start::

    //x = 0 -- commented out
    if y < 10:
        ...

Comments inside of multiline statements are also OK::
    
    list = [
        1,
        //2, -- commented out
        3
    ]
    
And inline comments are acceptable too::

    for i in list: // -- comment here
        r = r + i
        
Alright, thats all about it!