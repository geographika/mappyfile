 

.. _layer.json#/:

layer
=====

:type: ``object``

:Required: :ref:`layer.json#/properties/type`

**Properties:** :ref:`layer.json#/properties/class`, :ref:`layer.json#/properties/classgroup`, :ref:`layer.json#/properties/classitem`, :ref:`layer.json#/properties/cluster`, :ref:`layer.json#/properties/composite`, :ref:`layer.json#/properties/connection`, :ref:`layer.json#/properties/connectiontype`, :ref:`layer.json#/properties/data`, :ref:`layer.json#/properties/debug`, :ref:`layer.json#/properties/dump`, :ref:`layer.json#/properties/encoding`, :ref:`layer.json#/properties/extent`, :ref:`layer.json#/properties/features`, :ref:`layer.json#/properties/filter`, :ref:`layer.json#/properties/filteritem`, :ref:`layer.json#/properties/footer`, :ref:`layer.json#/properties/geomtransform`, :ref:`layer.json#/properties/grid`, :ref:`layer.json#/properties/group`, :ref:`layer.json#/properties/header`, :ref:`layer.json#/properties/join`, :ref:`layer.json#/properties/labelangleitem`, :ref:`layer.json#/properties/labelcache`, :ref:`layer.json#/properties/labelitem`, :ref:`layer.json#/properties/labelmaxscaledenom`, :ref:`layer.json#/properties/labelminscaledenom`, :ref:`layer.json#/properties/labelrequires`, :ref:`layer.json#/properties/labelsizeitem`, :ref:`layer.json#/properties/mask`, :ref:`layer.json#/properties/maxfeatures`, :ref:`layer.json#/properties/maxgeowidth`, :ref:`layer.json#/properties/maxscale`, :ref:`layer.json#/properties/maxscaledenom`, :ref:`layer.json#/properties/metadata`, :ref:`layer.json#/properties/mingeowidth`, :ref:`layer.json#/properties/minscale`, :ref:`layer.json#/properties/minscaledenom`, :ref:`layer.json#/properties/name`, :ref:`layer.json#/properties/offsite`, :ref:`layer.json#/properties/opacity`, :ref:`layer.json#/properties/plugin`, :ref:`layer.json#/properties/postlabelcache`, :ref:`layer.json#/properties/processing`, :ref:`layer.json#/properties/projection`, :ref:`layer.json#/properties/requires`, :ref:`layer.json#/properties/scaletoken`, :ref:`layer.json#/properties/sizeunits`, :ref:`layer.json#/properties/status`, :ref:`layer.json#/properties/styleitem`, :ref:`layer.json#/properties/symbolscaledenom`, :ref:`layer.json#/properties/template`, :ref:`layer.json#/properties/tileindex`, :ref:`layer.json#/properties/tileitem`, :ref:`layer.json#/properties/tilesrs`, :ref:`layer.json#/properties/tolerance`, :ref:`layer.json#/properties/toleranceunits`, :ref:`layer.json#/properties/transform`, :ref:`layer.json#/properties/transparency`, :ref:`layer.json#/properties/type`, :ref:`layer.json#/properties/units`, :ref:`layer.json#/properties/utfdata`, :ref:`layer.json#/properties/utfitem`, :ref:`layer.json#/properties/validation`


.. _layer.json#/properties/class:

class
+++++

:Reference: :ref:`class.json#/`


.. _layer.json#/properties/classgroup:

classgroup
++++++++++

:type: ``string``


.. _layer.json#/properties/classitem:

classitem
+++++++++

:type: ``string``


.. _layer.json#/properties/cluster:

cluster
+++++++

:type: ``object``


.. _layer.json#/properties/composite:

composite
+++++++++

:type: ``object``


.. _layer.json#/properties/connection:

connection
++++++++++

:type: ``string``


.. _layer.json#/properties/connectiontype:

connectiontype
++++++++++++++

**Allowed values:** 

- contour
- kerneldensity
- local
- ogr
- oraclespatial
- plugin
- postgis
- sde
- union
- uvraster
- wfs
- wms
- mygis


.. _layer.json#/properties/data:

data
++++

:type: ``string``


.. _layer.json#/properties/debug:

debug
+++++

:Reference: :ref:`debug.json#/`


.. _layer.json#/properties/dump:

dump
++++

Must satisfy *exactly one* of the following definitions:


.. _layer.json#/properties/dump/oneOf/0:

0
#

:type: ``boolean``


.. _layer.json#/properties/dump/oneOf/1:

1
#

:Reference: :ref:`onoff.json#/`


.. _layer.json#/properties/encoding:

encoding
++++++++

:type: ``string``


.. _layer.json#/properties/extent:

extent
++++++

:Reference: :ref:`extent.json#/`


.. _layer.json#/properties/features:

features
++++++++

:type: ``array``

.. container:: sub-title

 Every element of **features**  is:

:Reference: :ref:`feature.json#/`


.. _layer.json#/properties/filter:

filter
++++++

:Reference: :ref:`expression.json#/`


.. _layer.json#/properties/filteritem:

filteritem
++++++++++

:type: ``string``


.. _layer.json#/properties/footer:

footer
++++++

:type: ``string``


.. _layer.json#/properties/geomtransform:

geomtransform
+++++++++++++

May satisfy *any* of the following definitions:


.. _layer.json#/properties/geomtransform/anyOf/0:

0
#

:type: ``string``


.. _layer.json#/properties/geomtransform/anyOf/1:

1
#

:type: ``string``

:pattern: ``^\((.*?)\)$``


.. _layer.json#/properties/grid:

grid
++++

:Reference: :ref:`grid.json#/`


.. _layer.json#/properties/group:

group
+++++

:type: ``string``


.. _layer.json#/properties/header:

header
++++++

:type: ``string``


.. _layer.json#/properties/join:

join
++++

:type: ``object``


.. _layer.json#/properties/labelangleitem:

labelangleitem
++++++++++++++

:type: ``string``


.. _layer.json#/properties/labelcache:

labelcache
++++++++++

:Reference: :ref:`onoff.json#/`


.. _layer.json#/properties/labelitem:

labelitem
+++++++++

:type: ``string``


.. _layer.json#/properties/labelmaxscaledenom:

labelmaxscaledenom
++++++++++++++++++

:type: ``number``


.. _layer.json#/properties/labelminscaledenom:

labelminscaledenom
++++++++++++++++++

:type: ``number``


.. _layer.json#/properties/labelrequires:

labelrequires
+++++++++++++

:type: ``string``


.. _layer.json#/properties/labelsizeitem:

labelsizeitem
+++++++++++++

:type: ``string``


.. _layer.json#/properties/mask:

mask
++++

:type: ``string``


.. _layer.json#/properties/maxfeatures:

maxfeatures
+++++++++++

:type: ``integer``


.. _layer.json#/properties/maxgeowidth:

maxgeowidth
+++++++++++

:type: ``number``


.. _layer.json#/properties/maxscale:

maxscale
++++++++

:type: ``number``


.. _layer.json#/properties/maxscale/metadata:

metadata
--------

:deprecated: ``True``

:maxVersion: ``5.0``


.. _layer.json#/properties/maxscaledenom:

maxscaledenom
+++++++++++++

:type: ``number``


.. _layer.json#/properties/metadata:

metadata
++++++++

:Reference: :ref:`metadata.json#/`


.. _layer.json#/properties/mingeowidth:

mingeowidth
+++++++++++

:type: ``number``


.. _layer.json#/properties/minscale:

minscale
++++++++

:type: ``number``


.. _layer.json#/properties/minscale/metadata:

metadata
--------

:deprecated: ``True``

:maxVersion: ``5.0``

:minVersion: ``0``


.. _layer.json#/properties/minscaledenom:

minscaledenom
+++++++++++++

:type: ``number``


.. _layer.json#/properties/name:

name
++++

:type: ``string``


.. _layer.json#/properties/offsite:

offsite
+++++++

:Reference: :ref:`color.json#/`


.. _layer.json#/properties/opacity:

opacity
+++++++

:type: ``integer``


.. _layer.json#/properties/plugin:

plugin
++++++

:type: ``string``


.. _layer.json#/properties/postlabelcache:

postlabelcache
++++++++++++++

:type: ``boolean``


.. _layer.json#/properties/processing:

processing
++++++++++

:type: ``array``

.. container:: sub-title

 Every element of **processing**  is:

:type: ``string``


.. _layer.json#/properties/projection:

projection
++++++++++

:Reference: :ref:`projection.json#/`


.. _layer.json#/properties/requires:

requires
++++++++

:type: ``string``


.. _layer.json#/properties/scaletoken:

scaletoken
++++++++++

:Reference: :ref:`scaletoken.json#/`


.. _layer.json#/properties/sizeunits:

sizeunits
+++++++++

**Allowed values:** 

- feet
- inches
- kilometers
- meters
- miles
- nauticalmiles
- pixels


.. _layer.json#/properties/status:

status
++++++

:type: ``string``

**Allowed values:** 

- on
- off
- default


.. _layer.json#/properties/styleitem:

styleitem
+++++++++

:type: ``string``


.. _layer.json#/properties/symbolscaledenom:

symbolscaledenom
++++++++++++++++

:type: ``number``


.. _layer.json#/properties/template:

template
++++++++

:type: ``string``


.. _layer.json#/properties/tileindex:

tileindex
+++++++++

:type: ``string``


.. _layer.json#/properties/tileitem:

tileitem
++++++++

:type: ``string``


.. _layer.json#/properties/tilesrs:

tilesrs
+++++++

:type: ``string``


.. _layer.json#/properties/tolerance:

tolerance
+++++++++

:type: ``number``


.. _layer.json#/properties/toleranceunits:

toleranceunits
++++++++++++++

**Allowed values:** 

- pixels
- feet
- inches
- kilometers
- meters
- miles
- nauticalmiles
- dd


.. _layer.json#/properties/transform:

transform
+++++++++

Must satisfy *exactly one* of the following definitions:


.. _layer.json#/properties/transform/oneOf/0:

0
#

:type: ``boolean``


.. _layer.json#/properties/transform/oneOf/1:

1
#

:Reference: :ref:`position.json#/`


.. _layer.json#/properties/transparency:

transparency
++++++++++++

Must satisfy *exactly one* of the following definitions:


.. _layer.json#/properties/transparency/oneOf/0:

0
#

:type: ``integer``


.. _layer.json#/properties/transparency/oneOf/1:

1
#

**Allowed values:** 

- alpha


.. _layer.json#/properties/type:

type
++++

**Allowed values:** 

- chart
- circle
- line
- point
- polygon
- raster
- query
- annotation


.. _layer.json#/properties/units:

units
+++++

**Allowed values:** 

- dd
- feet
- inches
- kilometers
- meters
- miles
- nauticalmiles
- percentages
- pixels


.. _layer.json#/properties/utfdata:

utfdata
+++++++

:type: ``string``


.. _layer.json#/properties/utfitem:

utfitem
+++++++

:type: ``string``


.. _layer.json#/properties/validation:

validation
++++++++++

:Reference: :ref:`validation.json#/`
