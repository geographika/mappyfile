 

.. _color.json#/:

color
=====

Must satisfy *exactly one* of the following definitions:


.. _color.json#/oneOf/0:

0
+

:type: ``array``

:maxItems: ``3``

:minItems: ``3``

.. container:: sub-title

 Every element of **0**  is:

:type: ``number``

:minimum: ``0``

:maximum: ``255``


.. _color.json#/oneOf/1:

1
+

:type: ``string``

:pattern: ``^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$``

:example: ``#aa33cc``
