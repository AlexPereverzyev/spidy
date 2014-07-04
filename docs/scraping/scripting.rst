.. _scripting:

===============
Writing Scripts
===============

It's time to write first serious script. Spidy script is a file with \*.sp
extension. Yes, Spidy claims \*.sp extension for its script files and \*.spt -
for templates used by the scripts. First, lets briefly speak about fundamentals.

Typical Script
==============

Typical script consists of the following snippets:

- loading document and checking results
- skip to branch where data is located (optional)
- applying selectors or traversing document to collect data
- preparing and returning results

Documents and Formats
=====================

Loading document is an important first step, if it fails the whole script
may be aborted. To accomplish that, Spidy has a very cool command - ``get``. It
sends simple Web GET request and returns response. If command succeeds, document
becomes available for scraping.

By default, Spidy sniffs document format from extension. If URL doesn't have one -
it should be explicitly specified using ``as`` operator. At the moment the following
formats are supported:

- HTML
- XML
- TXT
- JSON

.. note:: When loading document as text (TXT), ``path``, ``skip`` and ``traverse``
    statements will not work since response is treated as not structured document.

News Example
============

Alright, the time has come to scrap news Web site! There are many potential targets,
but lets stop at http://news.google.com/. The goal is to get all top stories titles
with an original link to the article.

This time we will use ``run`` command, which accepts script name and output file
name, like this::
    
    import spidy as ss
    ss.run('examples/news.sp', 'examples/news.html')
    
First of all, we get XPaths for our data using procedure described in
:ref:`guidelines`:
    
- news container  : ``html/body/div[3]/div/div/div/div[3]/div/div/table/tbody/tr/td/div/div/div/div[2]``
- article element : news container  + ``/div/div/div/div[2]/table/tbody/tr/td[2]/div/h2/a[1]``
- article title   : article element + ``/span[1]``
- article link    : article element + ``@href``

We definitely can prepare shorter selectors, but lets simply use what FireBug
gives us for now. Next, the script itself::
    
    1     
    2     // cookies - off
    3     // javascript - off
    4     
    5     markup = '<html xmlns="http://www.w3.org/1999/xhtml"><head/><body><div>\n'
    6        
    7     get 'http://news.google.com/news?pz=1&cf=all&ned=en_us&hl=en&q&js=0' as html:
    8         User-Agent:'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:27.0) Gecko/20100101 Firefox/27.0'
    9         
    10    if & != None:
    11        traverse div in &'html/body/div[3]/div/div/div/div[3]/div/div/table/tbody/tr/td/div/div/div/div[2]':                
    12            
    13            if &(div + '@class') == 'esc-separator':
    14                continue
    15            
    16            anchor_path  = div + '/div/div/div/div[2]/table/tbody/tr/td[2]/div/h2/a[1]'
    17            anchor_ref   = &(anchor_path+'@href')        
    18            anchor_title = &(anchor_path+'/span[1]')        
    19            anchor       = ('\t<a href="' + anchor_ref + '">' + anchor_title + '</a><br/>\n')
    20            
    21            markup = markup + anchor
    22    else:
    23        markup = (markup + '\t<p>failed :(</p>\n')
    24        
    25    markup = (markup + '</div></body></html>')
    26    return markup
    
**Line 5** - initiate output HTML document in string variable ``markup``, so the
script returns HTML page. Article links will be appended to the variable.

**Lines 7, 8** - we load GNews main page with the same header as my browser has.
Your browser and corresponding user agent header might be different.

.. note:: HTTPS is not supported yet :(

**Line 11** - ``traverse`` helps to traverse structured documents. In it's basic
form it accepts path to container and enumerates it's direct children XPaths -
`div` variable. See more about it in :ref:`syntax`.

**Lines 13, 14** - workaround for non-article elements inside of the main
container.

Alright, this is all about it - hit *Run* and look for ``examples/news.html``
HTML file. Actually, we can make the script cleaner - see :ref:`templating`
to learn how.