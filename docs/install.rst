.. _install:

=========================
Installation Instructions
=========================

Installing Spidy is easy since it doesn't have external dependencies. This
page explains how.

Mac OS X
========

- Install pip (Python package manager): https://pypi.python.org/pypi/pip
- Now install Spidy using pip::

   pip install Spidy

Windows
=======

Installing Spidy for Windows is a bit complicated, since Python is not part 
of Windows distribution.

Prerequisites
-------------

- Install Python 2.7: https://www.python.org/download/.
- Add ``C:\Python27`` (or your custom Python location) folder to ``PATH`` environment variable.
- Set ``PYTHONPATH`` environment variable to the ``C:\Python27`` folder.
- Download Spidy source files from GitHub.

Installation
------------

In command prompt, change directory to Spidy's folder and enter:: 
	
	python setup.py bdist_wininst

The command will produce Windows installer in ``spidy/dist`` folder, e.g.: 
``dist/Spidy-0.1.win32``. Now simply run the installer and enjoy the process.