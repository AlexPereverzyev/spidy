.. _templating:

==============================
Cleaner Scripts with Templates
==============================

When you want script to return richer output or say HTML page, separation of
script and markup is a good idea. Spidy has special ``merge`` command to accomplish
that. It simply merges script context with specified template file and puts
results into a variable. Script context is basically all defined variables at
the current execution step.

.. note:: As oppose to Python, Spidy's variables have scope, meaning, loop
    variables or variables defined in ``if``, ``while``, ``traverse`` or ``for``
    statement's body will no longer be available after the statement's body is
    executed.

Currencies Example
==================

The following example also returns HTML page, but this time we will format results
as table. To demonstrate how it can be accomplished using templates, lets scrap
currencies data from Reuters and Yahoo finance sites::

    1         
    2     // cookies - off
    3     // javascript - off
    4     
    5     agent   = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:27.0) Gecko/20100101 Firefox/27.0'
    6     reuters = ['http://www.reuters.com/finance/global-market-data', 'Reuters', '//table[@id="currPairs"]/tbody[1]', '//a[1]', '/td[2]']
    7     yahoo   = ['http://finance.yahoo.com/currency-investing', 'Yahoo Finance', '//table[@id="flat-rates-table"]/tbody[1]', '//a[@class="currency-link"][1]', '/td[2]']
    8     sources = [reuters, yahoo]
    9     markup  = ''
    10    
    11    for src in sources:
    12        get src[0] as html:
    13            User-Agent: agent
    14            
    15        if & != None:
    16            header = src[1]
    17            pairs  = ''
    18            prices = ''
    19            traverse tr in &src[2]:
    20                pair  = &(tr + src[3])
    21                price = &(tr + src[4])
    22                merge 'currencies_pair.spt'  as pair
    23                merge 'currencies_price.spt' as price
    24                pairs  = pairs  + pair
    25                prices = prices + price            
    26            merge 'currencies_rows.spt' as row    
    27            markup = markup + row
    28            
    29    merge 'currencies_page.spt' as markup
    30    return markup
    
**Lines 6, 7** - for convenience, we keep site's URL, name and container, pair,
price XPath selectors in one list, so the script flow can be simplified.

**Lines 22, 23** - using ``merge`` command script produces table cells for
currency pair name and price value.

*currencies_pair.spt*::
    
    <th>${pair}</th>
    
*currencies_price.spt*::

    <td>${price}</td>

**Line 26** - resulting row header, pair name and price value are merged with
table row template.

*currencies_rows.spt*::

    <tr><td colspan="2"><b>${header}</b></td></tr>
    <tr>${pairs}</tr>
    <tr>${prices}</tr>
    
**Line 29** - finally, rows markup is merged with main document template.

*currencies_page.spt*::

    <html xmlns="http://www.w3.org/1999/xhtml"><head/><body><div><table><tbody>${markup}</tbody></table></div></body></html>

.. note:: Spidy's ``merge`` command and templates are based on Python's string
    templates.
	
The example's templates may look too simple for ``merge`` command to be effective.
But look further - how about adding CSS or JavaScript event handlers to the table?
I think you've got the idea.