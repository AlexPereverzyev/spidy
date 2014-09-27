======
Spidy
======

.. image:: https://badge.fury.io/py/Spidy.png
   :target: http://badge.fury.io/py/Spidy

.. image:: https://travis-ci.org/AlexPereverzyev/spidy.svg
   :target: https://travis-ci.org/AlexPereverzyev/spidy

Overview
========

Spidy is an open source scripting language for Web scraping. Spidy allows building
tools and applications which provide Web scraping features to wide audience of
users.

Despite beign a scripting language, Spidy attempts to standardize Web scraping
tasks around such fundamental tools like Web-get and XPath selectors. While URLs
allow to reference arbitrary document on the Web, Spidy goes one step further
to allow to referencing arbitrary piece of data with just a few lines of script,
which is easy to create, distribute and understand.

Here are major features the package offers:

* Flexibility of scripting language
* XPath selectors to extract data
* Unified document model for HTML and JSON formats
* Templates for better output formatting
* Robust error handling and logging

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
    
'Hello, World!' in Spidy
========================

Loading document or Web resource, for example trending repos page on GitHub::

    get 'https://github.com/explore' as html
        
Selecting and returning trending repos links using XPath with class selector::

    return &'//*[@class="repo-name css-truncate css-truncate-target"]'
    
And all together using Spidy API::

    import spidy
    print spidy.do('''
                   get 'https://github.com/explore' as html
                   return &'//*[@class="repo-name css-truncate css-truncate-target"]'
                   ''')
                   
will output list of relative links to stdout. Check out documentation for more
examples.

Documentation
=============

Documentation is available in the ``docs`` directory. Script examples are located
in ``examples`` directory.

Feedback
========

Spidy is non-profit, meaning further development needs good reason to go on.
We are happy to hear positive feedback, but also we can't wait to learn what's
bad, so please send your thoughts and our bugs to **spidy.feedback@gmail.com**.
Thank you and have a good scraping!