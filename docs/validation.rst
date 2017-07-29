Validation
==========

**Please note this part of the library is currently experimental.**

Approach
--------

`jsonschema <https://pypi.python.org/pypi/jsonschema>`_ is used to validate the library, by converting the dictionary to JSON. 
For details on creating schemas see the excellent documentation `here <https://spacetelescope.github.io/understanding-json-schema/>`_. 

What to Validate?
-----------------

Some keywords when missing will raise errors when trying to generate a map, for example if a ``MAP`` has no ``SIZE``:

.. code-block:: bat

    msDrawMap(): Image handling error. Unable to initialize image. <br>
    msPrepareImage(): General error message. Image dimensions not specified. <br>

However this parameter can be set from the command line, so the ``MAP`` may not actually be invalid. This is similar for ``EXTENT``:

.. code-block:: bat

    shp2img -m test.map -i png -o test.png -s 200 200
    msDrawMap(): Image handling error. Unable to initialize image. <br>
    msCalculateScale(): General error message. Invalid image extent, minx=-1.000000, miny=-1.000000, maxx=-1.000000, maxy=-1.000000

Would need to use:

.. code-block:: bat

    shp2img -m test.map -i png -o test.png -s 200 200 -e 0 0 5 5

Whilst keywords are not case-sensitive, some attributes are, for example ``STATUS "on"`` is not valid:

.. code-block:: bat

    getSymbol(): Symbol definition error. Parsing error near (on):(line 3) <br>

For non-case-sensitive attributes may need to enforce lower case on all keywords prior to validation to avoid having to make ``enum`` lists of "ON","on","On" etc. 

``CONFIG`` keywords (see http://mapserver.org/mapfile/map.html) have many MapServer and GDAL options, so won't validate these. 

Alert deprecated keywords? This appears to be a suggested feature of JSON Schema, see https://github.com/json-schema-org/json-schema-spec/pull/173. 

Schemas
-------

Could have different schema for different purposes, e.g. a valid WMS schema. 
Nested schemas are in the Draft 4 spec only - https://spacetelescope.github.io/understanding-json-schema/structuring.html

..
    For docs: https://github.com/inspirehep/jsonschema2rst