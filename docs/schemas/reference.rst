 

.. _reference.json#/:

reference
=========

:type: ``object``

**Properties:** :ref:`reference.json#/properties/color`, :ref:`reference.json#/properties/extent`, :ref:`reference.json#/properties/image`, :ref:`reference.json#/properties/marker`, :ref:`reference.json#/properties/markersize`, :ref:`reference.json#/properties/maxboxsize`, :ref:`reference.json#/properties/minboxsize`, :ref:`reference.json#/properties/outlinecolor`, :ref:`reference.json#/properties/size`, :ref:`reference.json#/properties/status`


.. _reference.json#/properties/color:

color
+++++

:Reference: :ref:`color.json#/`


.. _reference.json#/properties/extent:

extent
++++++

:Reference: :ref:`extent.json#/`


.. _reference.json#/properties/image:

image
+++++

filename

:type: ``string``


.. _reference.json#/properties/marker:

marker
++++++

Must satisfy *exactly one* of the following definitions:


.. _reference.json#/properties/marker/oneOf/0:

0
#

:type: ``integer``


.. _reference.json#/properties/marker/oneOf/1:

1
#

:type: ``string``


.. _reference.json#/properties/markersize:

markersize
++++++++++

:type: ``integer``


.. _reference.json#/properties/maxboxsize:

maxboxsize
++++++++++

:type: ``integer``


.. _reference.json#/properties/minboxsize:

minboxsize
++++++++++

:type: ``integer``


.. _reference.json#/properties/outlinecolor:

outlinecolor
++++++++++++

:Reference: :ref:`color.json#/`


.. _reference.json#/properties/size:

size
++++

:type: ``array``

:maxItems: ``2``

:minItems: ``2``

.. container:: sub-title

 Every element of **size**  is:

:type: ``integer``


.. _reference.json#/properties/status:

status
++++++

:Reference: :ref:`onoff.json#/`
