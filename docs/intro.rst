.. _intro:

=============
What's Spidy?
=============

Spidy is an open source scripting language for Web scraping or Web spiders 
programming. It combines flexibility of programming language with typical 
scraping tasks like loading document, extracting data from it using XPath 
selectors or rendering resulting markup with templates.

In a big picture, Spidy sees itself like a tool to build data aggregators,
news feeds or simply collecting data across the Internet. When you feed 
scraping script to Spidy, it returns ready to be consumed string, data list 
or even the whole HTML page.

While there are very nice scraping frameworks (see :ref:`references`) available,
Spidy doesn't require deep programming knowledge or skills and can
be used even by power users, who understand the domain.

Spidy is written in amazing Python 2.7, has no dependencies, but Python
Standard Library. Spidy borrows some syntax rules (e.g. indentation)
from Python as well.

A Very Basic Example
====================

Lets try a basic example without going to deep into the details. Say,
we would like to extract some content from some content Web site.
For example, lets collect all image links from ``http://imgur.com/`` from
'top images of today'.

Simple Spidy script will help us get it done, so lets write it down::
    
    import spidy as ss
    print ss.do('''
                get    'http://imgur.com/'
                skip   &'//div[@id="imagelist"]'
                return &'//img@src'
                ''')
    
What it does is very simple: it loads document, then skips to HTML element
with ``id=imagelist`` and selects ``src`` attribute values from all ``img``
elements.

Lets see what the script returns. Oops! It raises *DocumentException* which
says 'document format can't be resolved'. This means Spidy doesn't get how to
parse loaded document. Lets fix this and also add validation to check whether 
document was loaded at all::

    1    get    'http://imgur.com/' as html  
    2    if & == None:
    3        return 'failed :('        
    4    skip   &'//div[@id="imagelist"]'
    5    return &'//img@src'
    
.. note::
    & - is a magic operator which helps to evaluate XPath expressions and if
    used alone, returns the whole document's content. Second actually can help to
    determine whether document was loaded successfully.

Now it returns list of Unicode strings like ``'//i.imgur.com/<hash>.jpg'``.
Well, it seems broken, so we've got to do a bit more to get correct links from
the data. Lets prepend ``'http:'`` to each string and store the results
in a separate list::

    1     get 'http://imgur.com/' as html
    2     
    3     if & == None:
    4         return 'failed :('
    5     
    6     skip &'//div[@id="imagelist"]'
    7             
    8     image_urls = []
    9     image_sources = &'//img@src'        
    10            
    11    for src in image_sources:
    12        image_urls << ('http:' + src)
    13    
    14    return image_urls

Aright, the links are fixed now. What to do with them is up to script author,
but please remember copyright laws and simply be nice to people who bring the
content online :)