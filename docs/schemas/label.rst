 

.. _label.json#/:

label
=====

:type: ``object``

**Properties:** :ref:`label.json#/properties/align`, :ref:`label.json#/properties/angle`, :ref:`label.json#/properties/antialias`, :ref:`label.json#/properties/backgroundcolor`, :ref:`label.json#/properties/buffer`, :ref:`label.json#/properties/color`, :ref:`label.json#/properties/encoding`, :ref:`label.json#/properties/expression`, :ref:`label.json#/properties/font`, :ref:`label.json#/properties/force`, :ref:`label.json#/properties/maxlength`, :ref:`label.json#/properties/maxoverlapangle`, :ref:`label.json#/properties/maxscaledenom`, :ref:`label.json#/properties/maxsize`, :ref:`label.json#/properties/mindistance`, :ref:`label.json#/properties/minfeaturesize`, :ref:`label.json#/properties/minscaledenom`, :ref:`label.json#/properties/minsize`, :ref:`label.json#/properties/offset`, :ref:`label.json#/properties/outlinecolor`, :ref:`label.json#/properties/outlinewidth`, :ref:`label.json#/properties/partials`, :ref:`label.json#/properties/position`, :ref:`label.json#/properties/priority`, :ref:`label.json#/properties/repeatdistance`, :ref:`label.json#/properties/shadowcolor`, :ref:`label.json#/properties/shadowsize`, :ref:`label.json#/properties/size`, :ref:`label.json#/properties/style`, :ref:`label.json#/properties/text`, :ref:`label.json#/properties/type`, :ref:`label.json#/properties/wrap`


.. _label.json#/properties/align:

align
+++++

:type: ``string``

**Allowed values:** 

- left
- center
- right


.. _label.json#/properties/angle:

angle
+++++

Must satisfy *exactly one* of the following definitions:


.. _label.json#/properties/angle/oneOf/0:

0
#

:type: ``string``

**Allowed values:** 

- auto
- auto2
- follow


.. _label.json#/properties/angle/oneOf/1:

1
#

:type: ``number``


.. _label.json#/properties/angle/oneOf/2:

2
#

attribute

:type: ``string``

:pattern: ``^\[(.*?)\]$``


.. _label.json#/properties/antialias:

antialias
+++++++++

:type: ``boolean``


.. _label.json#/properties/backgroundcolor:

backgroundcolor
+++++++++++++++

:Reference: :ref:`color.json#/`


.. _label.json#/properties/buffer:

buffer
++++++

:type: ``integer``


.. _label.json#/properties/color:

color
+++++

Must satisfy *exactly one* of the following definitions:


.. _label.json#/properties/color/oneOf/0:

0
#

:Reference: :ref:`color.json#/`


.. _label.json#/properties/color/oneOf/1:

1
#

attribute

:type: ``string``

:pattern: ``^\[(.*?)\]$``


.. _label.json#/properties/encoding:

encoding
++++++++

:type: ``string``


.. _label.json#/properties/expression:

expression
++++++++++

:Reference: :ref:`expression.json#/`


.. _label.json#/properties/font:

font
++++

Must satisfy *exactly one* of the following definitions:


.. _label.json#/properties/font/oneOf/0:

0
#

:type: ``string``


.. _label.json#/properties/font/oneOf/1:

1
#

attribute

:type: ``string``

:pattern: ``^\[(.*?)\]$``


.. _label.json#/properties/force:

force
+++++

:type: ``boolean``


.. _label.json#/properties/maxlength:

maxlength
+++++++++

:type: ``integer``


.. _label.json#/properties/maxoverlapangle:

maxoverlapangle
+++++++++++++++

:type: ``number``


.. _label.json#/properties/maxscaledenom:

maxscaledenom
+++++++++++++

:type: ``number``


.. _label.json#/properties/maxsize:

maxsize
+++++++

:type: ``integer``


.. _label.json#/properties/mindistance:

mindistance
+++++++++++

:type: ``integer``


.. _label.json#/properties/minfeaturesize:

minfeaturesize
++++++++++++++

Must satisfy *exactly one* of the following definitions:


.. _label.json#/properties/minfeaturesize/oneOf/0:

0
#

:type: ``string``

:pattern: ``^auto$``


.. _label.json#/properties/minfeaturesize/oneOf/1:

1
#

:type: ``integer``


.. _label.json#/properties/minscaledenom:

minscaledenom
+++++++++++++

:type: ``number``


.. _label.json#/properties/minsize:

minsize
+++++++

:type: ``integer``


.. _label.json#/properties/offset:

offset
++++++

:type: ``array``

:maxItems: ``2``

:minItems: ``2``

.. container:: sub-title

 Every element of **offset**  is:

:type: ``number``


.. _label.json#/properties/outlinecolor:

outlinecolor
++++++++++++

Must satisfy *exactly one* of the following definitions:


.. _label.json#/properties/outlinecolor/oneOf/0:

0
#

:Reference: :ref:`color.json#/`


.. _label.json#/properties/outlinecolor/oneOf/1:

1
#

attribute

:type: ``string``

:pattern: ``^\[(.*?)\]$``


.. _label.json#/properties/outlinewidth:

outlinewidth
++++++++++++

:type: ``integer``


.. _label.json#/properties/partials:

partials
++++++++

:type: ``boolean``


.. _label.json#/properties/position:

position
++++++++

Must satisfy *exactly one* of the following definitions:


.. _label.json#/properties/position/oneOf/0:

0
#

**Allowed values:** 

- auto


.. _label.json#/properties/position/oneOf/1:

1
#

:Reference: :ref:`position.json#/`


.. _label.json#/properties/priority:

priority
++++++++

Must satisfy *exactly one* of the following definitions:


.. _label.json#/properties/priority/oneOf/0:

0
#

:type: ``integer``


.. _label.json#/properties/priority/oneOf/1:

1
#

attribute

:type: ``string``

:pattern: ``^\[(.*?)\]$``


.. _label.json#/properties/repeatdistance:

repeatdistance
++++++++++++++

:type: ``integer``


.. _label.json#/properties/shadowcolor:

shadowcolor
+++++++++++

:Reference: :ref:`color.json#/`


.. _label.json#/properties/shadowsize:

shadowsize
++++++++++

Must satisfy *exactly one* of the following definitions:


.. _label.json#/properties/shadowsize/oneOf/0:

0
#

:type: ``array``

:maxItems: ``2``

:minItems: ``2``

.. container:: sub-title

 Every element of **0**  is:

:type: ``integer``


.. _label.json#/properties/shadowsize/oneOf/1:

1
#

:type: ``array``

:maxItems: ``2``

:minItems: ``2``

.. container:: sub-title

 Every element of **1**  is:


.. _label.json#/properties/shadowsize/oneOf/1/items/0:

0
~

:type: ``integer``


.. _label.json#/properties/shadowsize/oneOf/1/items/1:

1
~

attribute

:type: ``string``

:pattern: ``^\[(.*?)\]$``


.. _label.json#/properties/size:

size
++++

Must satisfy *exactly one* of the following definitions:


.. _label.json#/properties/size/oneOf/0:

0
#

:type: ``integer``


.. _label.json#/properties/size/oneOf/1:

1
#

:type: ``string``

**Allowed values:** 

- tiny
- small
- medium
- large
- giant


.. _label.json#/properties/size/oneOf/2:

2
#

attribute

:type: ``string``

:pattern: ``^\[(.*?)\]$``


.. _label.json#/properties/style:

style
+++++

:Reference: :ref:`style.json#/`


.. _label.json#/properties/text:

text
++++

:Reference: :ref:`expression.json#/`


.. _label.json#/properties/type:

type
++++

:type: ``string``

**Allowed values:** 

- bitmap
- truetype


.. _label.json#/properties/wrap:

wrap
++++

:type: ``string``

:maxLength: ``1``

:minLength: ``1``
