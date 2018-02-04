 

.. _style.json#/:

style
=====

:type: ``object``

**Properties:** :ref:`style.json#/properties/angle`, :ref:`style.json#/properties/angleitem`, :ref:`style.json#/properties/antialias`, :ref:`style.json#/properties/backgroundcolor`, :ref:`style.json#/properties/color`, :ref:`style.json#/properties/colorrange`, :ref:`style.json#/properties/datarange`, :ref:`style.json#/properties/gap`, :ref:`style.json#/properties/geomtransform`, :ref:`style.json#/properties/initialgap`, :ref:`style.json#/properties/linecap`, :ref:`style.json#/properties/linejoin`, :ref:`style.json#/properties/linejoinmaxsize`, :ref:`style.json#/properties/maxscaledenom`, :ref:`style.json#/properties/maxsize`, :ref:`style.json#/properties/maxwidth`, :ref:`style.json#/properties/minscaledenom`, :ref:`style.json#/properties/minsize`, :ref:`style.json#/properties/minwidth`, :ref:`style.json#/properties/offset`, :ref:`style.json#/properties/opacity`, :ref:`style.json#/properties/outlinecolor`, :ref:`style.json#/properties/outlinewidth`, :ref:`style.json#/properties/pattern`, :ref:`style.json#/properties/polaroffset`, :ref:`style.json#/properties/size`, :ref:`style.json#/properties/symbol`, :ref:`style.json#/properties/width`


.. _style.json#/properties/angle:

angle
+++++

Must satisfy *exactly one* of the following definitions:


.. _style.json#/properties/angle/oneOf/0:

0
#

:type: ``number``


.. _style.json#/properties/angle/oneOf/1:

1
#

attribute

:type: ``string``

:pattern: ``^\[(.*?)\]$``


.. _style.json#/properties/angle/oneOf/2:

2
#

:type: ``string``

:pattern: ``^auto$``


.. _style.json#/properties/angleitem:

angleitem
+++++++++

:type: ``string``


.. _style.json#/properties/antialias:

antialias
+++++++++

:type: ``boolean``


.. _style.json#/properties/backgroundcolor:

backgroundcolor
+++++++++++++++

:Reference: :ref:`color.json#/`


.. _style.json#/properties/color:

color
+++++

Must satisfy *exactly one* of the following definitions:


.. _style.json#/properties/color/oneOf/0:

0
#

:Reference: :ref:`color.json#/`


.. _style.json#/properties/color/oneOf/1:

1
#

attribute

:type: ``string``

:pattern: ``^\[(.*?)\]$``


.. _style.json#/properties/colorrange:

colorrange
++++++++++

Must satisfy *exactly one* of the following definitions:


.. _style.json#/properties/colorrange/oneOf/0:

0
#

:type: ``array``

:maxItems: ``6``

:minItems: ``6``

.. container:: sub-title

 Every element of **0**  is:

:type: ``integer``


.. _style.json#/properties/colorrange/oneOf/1:

1
#

:type: ``array``

:maxItems: ``2``

:minItems: ``2``

.. container:: sub-title

 Every element of **1**  is:

:type: ``string``


.. _style.json#/properties/datarange:

datarange
+++++++++

:type: ``array``

:maxItems: ``2``

:minItems: ``2``

.. container:: sub-title

 Every element of **datarange**  is:

:type: ``number``


.. _style.json#/properties/gap:

gap
+++

:type: ``number``


.. _style.json#/properties/geomtransform:

geomtransform
+++++++++++++

Must satisfy *exactly one* of the following definitions:


.. _style.json#/properties/geomtransform/oneOf/0:

0
#

**Allowed values:** 

- bbox
- centroid
- end
- labelpnt
- labelpoly
- start
- vertices


.. _style.json#/properties/geomtransform/oneOf/1:

1
#

expression

:type: ``string``

:pattern: ``^\((.*?)\)$``


.. _style.json#/properties/initialgap:

initialgap
++++++++++

:type: ``number``


.. _style.json#/properties/linecap:

linecap
+++++++

**Allowed values:** 

- butt
- round
- square


.. _style.json#/properties/linejoin:

linejoin
++++++++

**Allowed values:** 

- round
- miter
- bevel
- none


.. _style.json#/properties/linejoinmaxsize:

linejoinmaxsize
+++++++++++++++

:type: ``integer``


.. _style.json#/properties/maxscaledenom:

maxscaledenom
+++++++++++++

:type: ``number``


.. _style.json#/properties/maxsize:

maxsize
+++++++

:type: ``number``


.. _style.json#/properties/maxwidth:

maxwidth
++++++++

:type: ``number``


.. _style.json#/properties/minscaledenom:

minscaledenom
+++++++++++++

:type: ``number``


.. _style.json#/properties/minsize:

minsize
+++++++

:type: ``number``


.. _style.json#/properties/minwidth:

minwidth
++++++++

:type: ``number``


.. _style.json#/properties/offset:

offset
++++++

:type: ``array``

:maxItems: ``2``

:minItems: ``2``

.. container:: sub-title

 Every element of **offset**  is:

:type: ``number``


.. _style.json#/properties/opacity:

opacity
+++++++

Must satisfy *exactly one* of the following definitions:


.. _style.json#/properties/opacity/oneOf/0:

0
#

:type: ``integer``


.. _style.json#/properties/opacity/oneOf/1:

1
#

attribute

:type: ``string``

:pattern: ``^\[(.*?)\]$``


.. _style.json#/properties/outlinecolor:

outlinecolor
++++++++++++

Must satisfy *exactly one* of the following definitions:


.. _style.json#/properties/outlinecolor/oneOf/0:

0
#

:Reference: :ref:`color.json#/`


.. _style.json#/properties/outlinecolor/oneOf/1:

1
#

attribute

:type: ``string``

:pattern: ``^\[(.*?)\]$``


.. _style.json#/properties/outlinewidth:

outlinewidth
++++++++++++

Must satisfy *exactly one* of the following definitions:


.. _style.json#/properties/outlinewidth/oneOf/0:

0
#

:type: ``number``


.. _style.json#/properties/outlinewidth/oneOf/1:

1
#

attribute

:type: ``string``

:pattern: ``^\[(.*?)\]$``


.. _style.json#/properties/pattern:

pattern
+++++++

:Reference: :ref:`points.json#/`


.. _style.json#/properties/polaroffset:

polaroffset
+++++++++++

:type: ``array``

.. container:: sub-title

 Every element of **polaroffset**  is:

:maxItems: ``2``

:minItems: ``2``

Must satisfy *exactly one* of the following definitions:


.. _style.json#/properties/polaroffset/items/oneOf/0:

0
#

:type: ``number``


.. _style.json#/properties/polaroffset/items/oneOf/1:

1
#

attribute

:type: ``string``

:pattern: ``^\[(.*?)\]$``


.. _style.json#/properties/size:

size
++++

Must satisfy *exactly one* of the following definitions:


.. _style.json#/properties/size/oneOf/0:

0
#

:type: ``number``


.. _style.json#/properties/size/oneOf/1:

1
#

attribute

:type: ``string``

:pattern: ``^\[(.*?)\]$``


.. _style.json#/properties/symbol:

symbol
++++++

Must satisfy *exactly one* of the following definitions:


.. _style.json#/properties/symbol/oneOf/0:

0
#

:type: ``string``


.. _style.json#/properties/symbol/oneOf/1:

1
#

:Reference: :ref:`symbol.json#/`


.. _style.json#/properties/width:

width
+++++

Must satisfy *exactly one* of the following definitions:


.. _style.json#/properties/width/oneOf/0:

0
#

:type: ``number``


.. _style.json#/properties/width/oneOf/1:

1
#

attribute

:type: ``string``

:pattern: ``^\[(.*?)\]$``
