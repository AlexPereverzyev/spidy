======
Spidy
======

.. image:: https://badge.fury.io/py/Spidy.png
   :target: http://badge.fury.io/py/Spidy

.. image:: https://travis-ci.org/AlexPereverzyev/spidy.svg
   :target: https://travis-ci.org/AlexPereverzyev/spidy

Overview
========

Spidy is an open source scripting language for Web scraping. Spidy makes
scraping easy because it has::

* Flexibility of scripting language
* XPath selectors to extract data
* Support for HTML and JSON formats
* Templates for output formatting

Requirements
============

Spidy is written in Python and relies on Python Standard Library only.

* Python 2.7
* Mac OS X, Windows, Linux, BSD

Install
=======

Installing from Python Package Index::

    pip install spidy
	
For Windows installation instructions, please see documentation in ``docs`` 
directory.
    
Usage
=====

'Hello world' example with Spidy shell::

    import spidy
    print spidy.do('''return 'Hello, world!' ''')

Documentation
=============

Documentation is available in the ``docs`` directory. Script examples are located
in ``examples`` directory. 