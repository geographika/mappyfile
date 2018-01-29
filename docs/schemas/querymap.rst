 

.. _querymap.json#/:

querymap
========

:type: ``object``

**Properties:** :ref:`querymap.json#/properties/color`, :ref:`querymap.json#/properties/size`, :ref:`querymap.json#/properties/status`, :ref:`querymap.json#/properties/style`


.. _querymap.json#/properties/color:

color
+++++

:Reference: :ref:`color.json#/`


.. _querymap.json#/properties/size:

size
++++

:type: ``array``

:maxItems: ``2``

:minItems: ``2``

.. container:: sub-title

 Every element of **size**  is:

:type: ``integer``


.. _querymap.json#/properties/status:

status
++++++

:Reference: :ref:`onoff.json#/`


.. _querymap.json#/properties/style:

style
+++++

:type: ``string``

**Allowed values:** 

- normal
- hilite
- selected
