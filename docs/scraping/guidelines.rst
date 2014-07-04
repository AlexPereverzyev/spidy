.. _guidelines:

=======================
Gearing Up for Scraping
=======================

Before we even start to think about writing first script, lets prepare, set up
tools and understand rules. Lets start from tools.

Tools Complementing Spidy
=========================

- **FireFox**:
    Browser of choice, great add-ons support.    
- **FireBug**:
    FireFox add-on. Must have, this is what we need to prepare XPath selectors
    for our data.    
- **Web Developer**:
    FireFox add-on. Nice to have, helps to disable cookies, javascript or cache
    quickly.

.. note:: Seems Chrome can substitute FireFox+FireBug.
          For simplicity, in this documentation we will focus on FireFox+FireBug only.

For download links to all the tools see :ref:`references`.

Getting Data Selectors
======================

Proper XPath selector is a key to everything in Spidy. However, XPath expressions
can be quite complex when it comes to manual work. How many elements does average
HTML document have? Hundreds? Thousands? Dozens of thousands? Getting selectors
can be tedious task. This is where FireFox+FireBug helps a lot.

There is one importatnt thing to mention, before we return to FireBug. Document tree
shown in FireBug (or Chrome developer tools) is not really what the document is.
Real-life HTML document is broken, meaning, it will contain not closed elements,
broken table layouts or else. Even Google doesn't return perfect HTML.

Good news is that Spidy makes sure it's internal document model is consistent with
FireBug's document model. Or, in other words, Spidy applies the same HTML error
handling rules as FireBug. This makes getting XPath selectors straightforward:

1. Open document in browser
2. Launch FireBug
3. Activate 'Inspect Element' tool
4. Select element
5. Right-click it in FireBug's DOM browser
6. Click 'Copy XPath' or 'Copy Minimal XPath'

The resulting XPath expression can be fed to Spidy script to extract element
or attribute value.

Later you may want to check out :ref:`syntax` for details about path ``&`` operator.

Things to Keep in Mind
======================

Sometimes the mentioned above won't work, but don't panic - there is a reason for
everything. Web servers can respond with different or slightly different HTML
depending on cookies, user agent or generate parts of DOM dynamically using
JavaScript. Usually, before getting XPaths for data you want to:

- disable cookies
- disable JavaScript

And when you run script:

- use same user-agent header as your browser

.. note:: Some content Web sites use JavaScript to load images, thus you won't
    find them in HTML with JavaScript disabled. Image URLs might be injected
    into site's JavaScript files.
    
Finally, remember that Web sites to remain attractive change page layout
time-to-time, so scraping script should be maintained too.