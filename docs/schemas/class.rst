 

.. _class.json#/:

class
=====

:type: ``object``

**Properties:** :ref:`class.json#/properties/backgroundcolor`, :ref:`class.json#/properties/color`, :ref:`class.json#/properties/debug`, :ref:`class.json#/properties/expression`, :ref:`class.json#/properties/group`, :ref:`class.json#/properties/keyimage`, :ref:`class.json#/properties/label`, :ref:`class.json#/properties/leader`, :ref:`class.json#/properties/maxscale`, :ref:`class.json#/properties/maxscaledenom`, :ref:`class.json#/properties/maxsize`, :ref:`class.json#/properties/minscale`, :ref:`class.json#/properties/minscaledenom`, :ref:`class.json#/properties/minsize`, :ref:`class.json#/properties/name`, :ref:`class.json#/properties/outlinecolor`, :ref:`class.json#/properties/size`, :ref:`class.json#/properties/status`, :ref:`class.json#/properties/style`, :ref:`class.json#/properties/symbol`, :ref:`class.json#/properties/template`, :ref:`class.json#/properties/text`, :ref:`class.json#/properties/title`, :ref:`class.json#/properties/validation`


.. _class.json#/properties/backgroundcolor:

backgroundcolor
+++++++++++++++

:Reference: :ref:`color.json#/`


.. _class.json#/properties/color:

color
+++++

:Reference: :ref:`color.json#/`


.. _class.json#/properties/debug:

debug
+++++

:Reference: :ref:`onoff.json#/`


.. _class.json#/properties/expression:

expression
++++++++++

:Reference: :ref:`expression.json#/`


.. _class.json#/properties/group:

group
+++++

:type: ``string``


.. _class.json#/properties/keyimage:

keyimage
++++++++

filename

:type: ``string``


.. _class.json#/properties/label:

label
+++++

:Reference: :ref:`label.json#/`


.. _class.json#/properties/leader:

leader
++++++

:Reference: :ref:`leader.json#/`


.. _class.json#/properties/maxscale:

maxscale
++++++++

:type: ``number``

:deprecated: ``True``


.. _class.json#/properties/maxscaledenom:

maxscaledenom
+++++++++++++

:type: ``number``


.. _class.json#/properties/maxsize:

maxsize
+++++++

:type: ``integer``


.. _class.json#/properties/minscale:

minscale
++++++++

:type: ``number``

:deprecated: ``True``


.. _class.json#/properties/minscaledenom:

minscaledenom
+++++++++++++

:type: ``number``


.. _class.json#/properties/minsize:

minsize
+++++++

:type: ``integer``


.. _class.json#/properties/name:

name
++++

:type: ``string``


.. _class.json#/properties/outlinecolor:

outlinecolor
++++++++++++

:Reference: :ref:`color.json#/`


.. _class.json#/properties/size:

size
++++

:type: ``integer``


.. _class.json#/properties/status:

status
++++++

:Reference: :ref:`onoff.json#/`


.. _class.json#/properties/style:

style
+++++

:Reference: :ref:`style.json#/`


.. _class.json#/properties/symbol:

symbol
++++++

Must satisfy *exactly one* of the following definitions:


.. _class.json#/properties/symbol/oneOf/0:

0
#

:type: ``string``


.. _class.json#/properties/symbol/oneOf/1:

1
#

:Reference: :ref:`symbol.json#/`


.. _class.json#/properties/template:

template
++++++++

filename

:type: ``string``


.. _class.json#/properties/text:

text
++++

:Reference: :ref:`expression.json#/`


.. _class.json#/properties/title:

title
+++++

missing

:type: ``string``


.. _class.json#/properties/validation:

validation
++++++++++

:Reference: :ref:`validation.json#/`
