 

.. _map.json#/:

map
===

:type: ``object``

**Properties:** :ref:`map.json#/properties/__type__`, :ref:`map.json#/properties/angle`, :ref:`map.json#/properties/debug`, :ref:`map.json#/properties/extent`, :ref:`map.json#/properties/layers`, :ref:`map.json#/properties/name`, :ref:`map.json#/properties/status`


.. _map.json#/properties/__type__:

__type__
++++++++

:type: ``string``


.. _map.json#/properties/angle:

angle
+++++

:type: ``number``


.. _map.json#/properties/debug:

debug
+++++

**Allowed values:** 

- ON
- OFF
- 0
- 1
- 2
- 3
- 4
- 5


.. _map.json#/properties/extent:

extent
++++++

:type: ``array``

:maxItems: ``4``

:minItems: ``4``

.. container:: sub-title

 Every element of **extent**  is:

:type: ``number``


.. _map.json#/properties/layers:

layers
++++++

:type: ``array``

.. container:: sub-title

 Every element of **layers**  is:

:type: ``object``

:Reference: :ref:`layer.json#/`


.. _map.json#/properties/name:

name
++++

:type: ``string``


.. _map.json#/properties/status:

status
++++++

:type: ``string``

**Allowed values:** 

- ON
- OFF
