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
        

Notes:

+ Comments will be removed
+ Quotes will be standardised
+ Indentation can be set as an option e.g. 2 or 4 spaces
+ Any ``INCLUDE`` directives will have been parsed and treated as part of the original Mapfile 
  so there will never be any ``INCLUDE`` keywords in the output