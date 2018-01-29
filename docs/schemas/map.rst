 

.. _map.json#/:

map
===

:type: ``object``

**Properties:** :ref:`map.json#/properties/__type__`, :ref:`map.json#/properties/angle`, :ref:`map.json#/properties/config`, :ref:`map.json#/properties/datapattern`, :ref:`map.json#/properties/debug`, :ref:`map.json#/properties/defresolution`, :ref:`map.json#/properties/extent`, :ref:`map.json#/properties/fontset`, :ref:`map.json#/properties/imagecolor`, :ref:`map.json#/properties/imagequality`, :ref:`map.json#/properties/imagetype`, :ref:`map.json#/properties/interlace`, :ref:`map.json#/properties/layers`, :ref:`map.json#/properties/legend`, :ref:`map.json#/properties/maxsize`, :ref:`map.json#/properties/name`, :ref:`map.json#/properties/outputformats`, :ref:`map.json#/properties/projection`, :ref:`map.json#/properties/querymap`, :ref:`map.json#/properties/reference`, :ref:`map.json#/properties/resolution`, :ref:`map.json#/properties/scalebar`, :ref:`map.json#/properties/scaledenom`, :ref:`map.json#/properties/shapepath`, :ref:`map.json#/properties/size`, :ref:`map.json#/properties/status`, :ref:`map.json#/properties/symbols`, :ref:`map.json#/properties/symbolset`, :ref:`map.json#/properties/templatepattern`, :ref:`map.json#/properties/transparent`, :ref:`map.json#/properties/units`, :ref:`map.json#/properties/web`


.. _map.json#/properties/__type__:

__type__
++++++++

:type: ``string``


.. _map.json#/properties/angle:

angle
+++++

:type: ``number``


.. _map.json#/properties/config:

config
++++++

:type: ``object``

**Properties:** :ref:`map.json#/properties/config/properties/CGI_CONTEXT_URL`, :ref:`map.json#/properties/config/properties/MS_ENCRYPTION_KEY`, :ref:`map.json#/properties/config/properties/MS_ERRORFILE`, :ref:`map.json#/properties/config/properties/MS_NONSQUARE`, :ref:`map.json#/properties/config/properties/ON_MISSING_DATA`, :ref:`map.json#/properties/config/properties/PROJ_LIB`


.. _map.json#/properties/config/properties/CGI_CONTEXT_URL:

CGI_CONTEXT_URL
###############

:type: ``string``


.. _map.json#/properties/config/properties/MS_ENCRYPTION_KEY:

MS_ENCRYPTION_KEY
#################

:type: ``string``


.. _map.json#/properties/config/properties/MS_ERRORFILE:

MS_ERRORFILE
############

:type: ``string``


.. _map.json#/properties/config/properties/MS_NONSQUARE:

MS_NONSQUARE
############

:Reference: :ref:`yesno.json#/`


.. _map.json#/properties/config/properties/ON_MISSING_DATA:

ON_MISSING_DATA
###############

:type: ``string``

**Allowed values:** 

- FAIL
- LOG
- IGNORE


.. _map.json#/properties/config/properties/PROJ_LIB:

PROJ_LIB
########

:type: ``string``


.. _map.json#/properties/datapattern:

datapattern
+++++++++++

:type: ``string``


.. _map.json#/properties/debug:

debug
+++++

:$refss: ``debug.json``


.. _map.json#/properties/defresolution:

defresolution
+++++++++++++

:type: ``integer``


.. _map.json#/properties/extent:

extent
++++++

:Reference: :ref:`extent.json#/`


.. _map.json#/properties/fontset:

fontset
+++++++

:type: ``string``


.. _map.json#/properties/imagecolor:

imagecolor
++++++++++

:Reference: :ref:`color.json#/`


.. _map.json#/properties/imagequality:

imagequality
++++++++++++

:type: ``integer``


.. _map.json#/properties/imagetype:

imagetype
+++++++++

:type: ``string``


.. _map.json#/properties/interlace:

interlace
+++++++++

:Reference: :ref:`onoff.json#/`


.. _map.json#/properties/layers:

layers
++++++

:type: ``array``

.. container:: sub-title

 Every element of **layers**  is:

:type: ``object``

:Reference: :ref:`layer.json#/`


.. _map.json#/properties/legend:

legend
++++++

:type: ``object``


.. _map.json#/properties/maxsize:

maxsize
+++++++

:type: ``integer``


.. _map.json#/properties/name:

name
++++

:type: ``string``


.. _map.json#/properties/outputformats:

outputformats
+++++++++++++

:type: ``array``

.. container:: sub-title

 Every element of **outputformats**  is:

:type: ``object``


.. _map.json#/properties/projection:

projection
++++++++++

:Reference: :ref:`projection.json#/`


.. _map.json#/properties/querymap:

querymap
++++++++

:Reference: :ref:`querymap.json#/`


.. _map.json#/properties/reference:

reference
+++++++++

:type: ``object``


.. _map.json#/properties/resolution:

resolution
++++++++++

:type: ``integer``


.. _map.json#/properties/scalebar:

scalebar
++++++++

:type: ``object``


.. _map.json#/properties/scaledenom:

scaledenom
++++++++++

:type: ``number``


.. _map.json#/properties/shapepath:

shapepath
+++++++++

:type: ``string``


.. _map.json#/properties/size:

size
++++

:type: ``array``

:maxItems: ``2``

:minItems: ``2``

.. container:: sub-title

 Every element of **size**  is:

:type: ``integer``


.. _map.json#/properties/status:

status
++++++

:Reference: :ref:`onoff.json#/`


.. _map.json#/properties/symbols:

symbols
+++++++

:type: ``array``

.. container:: sub-title

 Every element of **symbols**  is:

:type: ``object``


.. _map.json#/properties/symbolset:

symbolset
+++++++++

:type: ``string``


.. _map.json#/properties/templatepattern:

templatepattern
+++++++++++++++

:type: ``string``


.. _map.json#/properties/transparent:

transparent
+++++++++++

:Reference: :ref:`onoff.json#/`


.. _map.json#/properties/units:

units
+++++

:Reference: :ref:`units.json#/`


.. _map.json#/properties/web:

web
+++

:type: ``object``
