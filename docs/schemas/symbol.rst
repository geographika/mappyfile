 

.. _symbol.json#/:

symbol
======

:type: ``object``

**Properties:** :ref:`symbol.json#/properties/anchorpoint`, :ref:`symbol.json#/properties/antialias`, :ref:`symbol.json#/properties/backgroundcolor`, :ref:`symbol.json#/properties/character`, :ref:`symbol.json#/properties/filled`, :ref:`symbol.json#/properties/font`, :ref:`symbol.json#/properties/image`, :ref:`symbol.json#/properties/name`, :ref:`symbol.json#/properties/points`, :ref:`symbol.json#/properties/transparent`, :ref:`symbol.json#/properties/type`


.. _symbol.json#/properties/anchorpoint:

anchorpoint
+++++++++++

:type: ``array``

:maxItems: ``2``

:minItems: ``2``

.. container:: sub-title

 Every element of **anchorpoint**  is:


.. _symbol.json#/properties/anchorpoint/items/0:

0
-

:type: ``number``

:minimum: ``0``

:maximum: ``1``


.. _symbol.json#/properties/antialias:

antialias
+++++++++

:type: ``boolean``


.. _symbol.json#/properties/backgroundcolor:

backgroundcolor
+++++++++++++++

:Reference: :ref:`color.json#/`


.. _symbol.json#/properties/character:

character
+++++++++

:type: ``string``

:maxLength: ``1``

:minLength: ``1``


.. _symbol.json#/properties/filled:

filled
++++++

:type: ``boolean``


.. _symbol.json#/properties/font:

font
++++

:type: ``string``


.. _symbol.json#/properties/image:

image
+++++

:type: ``string``


.. _symbol.json#/properties/name:

name
++++

:type: ``string``


.. _symbol.json#/properties/points:

points
++++++

:Reference: :ref:`points.json#/`


.. _symbol.json#/properties/transparent:

transparent
+++++++++++

:type: ``integer``


.. _symbol.json#/properties/type:

type
++++

**Allowed values:** 

- ellipse
- hatch
- pixmap
- svg
- truetype
- vector
