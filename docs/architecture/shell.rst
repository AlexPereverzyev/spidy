.. _shell:

========================
Working with Spidy Shell
========================

Spidy's shell makes Spidy do what you want. It's single access point to all 
Spidy's features, like checking scripts for syntax errors or executing them.

.. note:: Here *shell* means programming shell, but not CLI shell.

Shell Commands
==============

Here are the available commands signatures::

    def check_file(script_file, log_file = None, log_level = 20)
    
    def check(script, log_file = None, log_level = 20)
    
    def run(script_file, out_file = None, log_file = None, log_level = 20)

    def do(script, out_file = None, log_file = None, log_level = 20)
    
Validating Scripts
==================

To check scripts for syntax errors Spidy shell has two commands: ``check_file``
and ``check``. Each of them returns ``True`` if script is OK, the only difference
is that ``check`` accepts script string, but ``check_file`` - path to script file.

Running Scripts
===============

``run`` and ``do`` commands execute script file or script string correspondingly.
Both commands have an option either to return output or to write it to *out_file*
file.

If script fails at some point, ``run`` and ``do`` commands will log and raise an
appropriate exception.

.. note:: ``do`` command different from ``run`` not only in the way you specify
    script. When ``run``, Spidy sets script working directory and uses it later,
    to resolve locations of template files. ``do`` doesn't set script directory,
    thereby absolute paths should be used to specify template files.
    
A Word About Logging
====================

Besides mentioned, Spidy shell allows to specify file for logging *log_file* and
log verbosity using *log_level* argument. If *log_file* is not specified, Spidy
logs messages to *stdout*.

The default log level is 20 or *INFO*, it means messages with log level below it 
(e.g.:  *DEBUG*) will not get into the logs.

.. note:: ``log`` command writes *INFO* messages to logs.