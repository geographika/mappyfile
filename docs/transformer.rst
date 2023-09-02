.. _transformer:

Transforming
============

mappyfile parses a Mapfile and turns it into a Abstract Syntax Tree (AST). The mappyfile
`transformer class <https://github.com/geographika/mappyfile/blob/master/mappyfile/transformer.py>`_ then turns this tree into a Python dictionary. 
Using a dictionary provides the Python developer with a familiar data structure that can be used to edit the Mapfile further - see :ref:`editing`.

For example taking the Mapfile below:

.. literalinclude:: examples/after.map
   :language: mapfile

The following code can be used to see the dictionary structure (represented here as a JSON object):

.. literalinclude:: examples/sample_json.py
   :language: python

Output:

.. literalinclude:: examples/sample.json
   :language: json

Some notes on the above:

+ Objects that can have multiple instances (for example ``LAYER`` and ``CLASS`` in a Mapfile will be stored in lists (order is important).
+ Most objects have a set of key/value pairs. ``PROJECTION`` however is treated as a list 
  (see http://www.mapserver.org/mapfile/projection.html).
+ Some keys are already quoted e.g. in the ``METADATA`` object items such as "wms_enable_request" are strings rather than keywords.
+ Some keys are duplicated within an object. E.g.

  .. code-block:: mapfile
  
        PROCESSING "BANDS=1"
        PROCESSING "CONTOUR_ITEM=elevation"
        PROCESSING "CONTOUR_INTERVAL=20"
        
  These are turned into lists:
    
  .. code-block:: json
  
    "processing": [
        "'BANDS=1'", 
        "'CONTOUR_ITEM=elevation'", 
        "'CONTOUR_INTERVAL=20'"
    ], 
  

Python dictionaries map closely to JSON data structures, which means the Mapfile dictionary 
structure can be formalised into a JSONSchema. See :ref:`mapfile-schema` for more details, and also the draft MapServer
proposal :ref:`rfc123`.

Mappyfile Additions
-------------------

In order to ensure that no information is lost when inputting and outputting a Mapfile,
mappyfile makes use of hidden properties to store additional data. This data is
not outputted as part of the pretty-print. For example a hidden property is used to store objects of the 
same type e.g. ``LAYER``, ``CLASS``, and ``STYLE``.
