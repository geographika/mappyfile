.. _pretty-printing:
    
Pretty Printing
===============

*Please note this page is currently a draft and subject to further updates.*

A Mapfile with inconsistent formatting such as the example below:

.. literalinclude:: examples/before.map
   :language: mapfile

Can be converted using mappyfile to a nicely formatted version using the code below

.. literalinclude:: examples/pretty_printing.py
   :language: python

The result:

.. literalinclude:: examples/after.map
   :language: mapfile
        

.. warning::

    When standardising quotes be careful that no quotes chosen for formatting are found within string values. 
    For example large ``DATA`` blocks of SQL may contain single quotes, that would then create an invalid Mapfile. 

Notes:

+ Comments will be removed
+ Quotes will be standardised
+ Indentation can be set as an option e.g. 2 or 4 spaces