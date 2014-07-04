
==============
Consuming JSON
==============

If you reading this, you know that Web is made not only of XML documents. Another
popular data format is JSON. Spidy eats JSON data as well. Even more - you can
apply familiar XPath selectors to JSON documents! Here is how Spidy processes
JSON documents (docstring from *JsonTransform* class).

.. autoclass:: spidy.document.json_transform.JsonTransform 

As you already guessed, internally, Spidy parses JSON response and converts it
to the same document model it uses for HTML or XML documents.

JSON Weather API Example
========================

This time we will make it really simple. No need to disable cookies or
JavaScript - JSON is pure data. The following example finds out weather in
Kiev, Ukraine using nice JSON weather API at http://openweathermap.org/.

However, lets add one more command to the mix - ``log``. It simply logs message
to *stdout* or to specified log file. How to specify log file see :ref:`shell`.
Log command is very convenient when debugging or if you simply want to know what
script is doing at the moment.

.. note:: Spidy's logging is based on Python's *logging* module.

So here is the script to get current weather in Kiev::

    1     
    2     // cookies - on
    3     // javascript - on
    4     
    5     log      'sending request'
    6     get      'http://api.openweathermap.org/data/2.5/weather?q=kiev,ua&units=metric' as json
    7     log      'processing response'
    8     skip    &'tag[1]'
    9     city  = &'.@name'
    10    desc  = &'weather[1]@description'
    11    temp  = &'main[1]@temp'
    12    pres  = &'main[1]@pressure'
    13    humid = &'main[1]@humidity'
    14    log      'returning results'
    15    return   [city, desc, temp, pres, humid]
    
Running the script returns the following::    

    import spidy
    print spidy.run('examples/weather.sp')
    
*stdout*::
    
    [2014-06-25 19:37:20,274] INFO: Spidy: executing script file: examples/weather.sp
    [2014-06-25 19:37:20,305] INFO: sending request
    [2014-06-25 19:37:20,431] INFO: processing response
    [2014-06-25 19:37:20,439] INFO: returning results            
    [2014-06-25 19:37:20,440] INFO: Spidy: finished executing script file: examples/weather.sp
    [u'Kiev', u'Sky is Clear', 20.33, 1009, 47]