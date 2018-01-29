 

.. _scalebar.json#/:

scalebar
========

:type: ``object``

**Properties:** :ref:`scalebar.json#/properties/align`, :ref:`scalebar.json#/properties/backgroundcolor`, :ref:`scalebar.json#/properties/color`, :ref:`scalebar.json#/properties/extent`, :ref:`scalebar.json#/properties/image`, :ref:`scalebar.json#/properties/imagecolor`, :ref:`scalebar.json#/properties/interlace`, :ref:`scalebar.json#/properties/intervals`, :ref:`scalebar.json#/properties/label`, :ref:`scalebar.json#/properties/marker`, :ref:`scalebar.json#/properties/markersize`, :ref:`scalebar.json#/properties/maxboxsize`, :ref:`scalebar.json#/properties/minboxsize`, :ref:`scalebar.json#/properties/offset`, :ref:`scalebar.json#/properties/outlinecolor`, :ref:`scalebar.json#/properties/position`, :ref:`scalebar.json#/properties/postlabelcache`, :ref:`scalebar.json#/properties/size`, :ref:`scalebar.json#/properties/status`, :ref:`scalebar.json#/properties/style`, :ref:`scalebar.json#/properties/transparent`, :ref:`scalebar.json#/properties/units`


.. _scalebar.json#/properties/align:

align
+++++

:type: ``string``

**Allowed values:** 

- left
- center
- right


.. _scalebar.json#/properties/backgroundcolor:

backgroundcolor
+++++++++++++++

:Reference: :ref:`color.json#/`


.. _scalebar.json#/properties/color:

color
+++++

:Reference: :ref:`color.json#/`


.. _scalebar.json#/properties/extent:

extent
++++++

:Reference: :ref:`extent.json#/`


.. _scalebar.json#/properties/image:

image
+++++

filename

:type: ``string``


.. _scalebar.json#/properties/imagecolor:

imagecolor
++++++++++

:Reference: :ref:`color.json#/`


.. _scalebar.json#/properties/interlace:

interlace
+++++++++

:type: ``boolean``


.. _scalebar.json#/properties/intervals:

intervals
+++++++++

:type: ``integer``


.. _scalebar.json#/properties/label:

label
+++++

:Reference: :ref:`label.json#/`


.. _scalebar.json#/properties/marker:

marker
++++++

Must satisfy *exactly one* of the following definitions:


.. _scalebar.json#/properties/marker/oneOf/0:

0
#

:type: ``integer``


.. _scalebar.json#/properties/marker/oneOf/1:

1
#

:type: ``string``


.. _scalebar.json#/properties/markersize:

markersize
++++++++++

:type: ``integer``


.. _scalebar.json#/properties/maxboxsize:

maxboxsize
++++++++++

:type: ``integer``


.. _scalebar.json#/properties/minboxsize:

minboxsize
++++++++++

:type: ``integer``


.. _scalebar.json#/properties/offset:

offset
++++++

:type: ``array``

:maxItems: ``2``

:minItems: ``2``

.. container:: sub-title

 Every element of **offset**  is:

:type: ``integer``


.. _scalebar.json#/properties/offset/metadata:

metadata
--------

:minVersion: ``7.02``


.. _scalebar.json#/properties/outlinecolor:

outlinecolor
++++++++++++

:Reference: :ref:`color.json#/`


.. _scalebar.json#/properties/position:

position
++++++++

:Reference: :ref:`position.json#/`


.. _scalebar.json#/properties/postlabelcache:

postlabelcache
++++++++++++++

:type: ``boolean``


.. _scalebar.json#/properties/size:

size
++++

:type: ``array``

:maxItems: ``2``

:minItems: ``2``

.. container:: sub-title

 Every element of **size**  is:

:type: ``integer``


.. _scalebar.json#/properties/status:

status
++++++

:type: ``string``

**Allowed values:** 

- on
- off
- embed


.. _scalebar.json#/properties/style:

style
+++++

:type: ``integer``


.. _scalebar.json#/properties/transparent:

transparent
+++++++++++

:Reference: :ref:`onoff.json#/`


.. _scalebar.json#/properties/units:

units
+++++

:Reference: :ref:`sizeunits.json#/`
