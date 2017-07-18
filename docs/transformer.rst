Transforming
============

Once mappyfile has parsed a Mapfile, it uses a transformer to transform it into a dict object. This allows a familiar API to edit
the Mapfile further. 

For example taking the Mapfile below:

.. literalinclude:: examples/after.map
   :language: mapfile

The following code can be used to see the dictionary structure (represented here as a JSON object):

.. literalinclude:: examples/sample_json.py
   :language: python
	
Output:

.. literalinclude:: examples/sample.json
   :language: json
    
Notes on the above:

+ Objects that can have multiple instances in a Mapfile will be stored in lists (order is important).
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
  

Mappyfile Additions
-------------------

Hidden containers - these containers are not outputted as part of the pprint. They are used to store objects of the same type 
e.g. LAYERs, CLASSes, STYLEs

..
    + Could make use of https://github.com/bcj/AttrDict to allow property-like access to dictionary objects (see proposed API examples below)?
	