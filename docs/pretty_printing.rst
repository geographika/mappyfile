.. _pretty-printing:
    
Pretty Printing
===============

Taking an input similar to below:

.. literalinclude:: examples/before.map
   :language: mapfile

The following code will output a nicely formatted version. 

.. literalinclude:: examples/pretty_printing.py
   :language: python

Result:

.. literalinclude:: examples/after.map
   :language: mapfile
        

.. warning::

    When standardising quotes be careful that no quotes chosen for formatting are found within string values. 
    For example large ``DATA`` blocks of SQL may contain single quotes, that would then create an invalid Mapfile. 

Notes:

+ Comments will be removed
+ Quotes will be standardised
+ Indentation can be set as an option e.g. 2 or 4 spaces