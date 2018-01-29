 

.. _legend.json#/:

legend
======

:type: ``object``

**Properties:** :ref:`legend.json#/properties/imagecolor`, :ref:`legend.json#/properties/interlace`, :ref:`legend.json#/properties/keysize`, :ref:`legend.json#/properties/keyspacing`, :ref:`legend.json#/properties/label`, :ref:`legend.json#/properties/outlinecolor`, :ref:`legend.json#/properties/position`, :ref:`legend.json#/properties/postlabelcache`, :ref:`legend.json#/properties/status`, :ref:`legend.json#/properties/template`, :ref:`legend.json#/properties/transparent`


.. _legend.json#/properties/imagecolor:

imagecolor
++++++++++

:Reference: :ref:`color.json#/`


.. _legend.json#/properties/interlace:

interlace
+++++++++

:Reference: :ref:`onoff.json#/`


.. _legend.json#/properties/keysize:

keysize
+++++++

:type: ``array``

:maxItems: ``2``

:minItems: ``2``

.. container:: sub-title

 Every element of **keysize**  is:

:type: ``integer``


.. _legend.json#/properties/keyspacing:

keyspacing
++++++++++

:type: ``array``

:maxItems: ``2``

:minItems: ``2``

.. container:: sub-title

 Every element of **keyspacing**  is:

:type: ``integer``


.. _legend.json#/properties/label:

label
+++++

:Reference: :ref:`label.json#/`


.. _legend.json#/properties/outlinecolor:

outlinecolor
++++++++++++

:Reference: :ref:`color.json#/`


.. _legend.json#/properties/position:

position
++++++++

:Reference: :ref:`position.json#/`


.. _legend.json#/properties/postlabelcache:

postlabelcache
++++++++++++++

:type: ``boolean``


.. _legend.json#/properties/status:

status
++++++

:type: ``string``

**Allowed values:** 

- on
- off
- embed


.. _legend.json#/properties/template:

template
++++++++

filename

:type: ``string``


.. _legend.json#/properties/transparent:

transparent
+++++++++++

:Reference: :ref:`onoff.json#/`
