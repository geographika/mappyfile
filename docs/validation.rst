.. _validation-docs:

Validation
==========

A key part of the mappyfile library is to validate Mapfiles - checking that options for various keywords are valid. In order to achieve this
a full definition of the Mapfile language has been encoded in a JSON file - see :ref:`mapfile-schema`.

`jsonschema <https://pypi.python.org/pypi/jsonschema>`_ is used to validate a Mapfile by converting the transformed dictionary to JSON. 
For details on creating JSON schemas see the excellent documentation `here <https://spacetelescope.github.io/understanding-json-schema/>`_. 

What is Validated?
------------------

Each of the Mapfile keywords has a limited set of allowed values. For example a `UNIT`` setting for a ``LAYER`` must be one of the strings 
in the list below:

.. code-block:: json

    {
    "units": {
        "enum": [
            "dd", 
            "feet", 
            "inches", 
            "kilometers", 
            "meters", 
            "miles", 
            "nauticalmiles", 
            "percentages", 
            "pixels"
        ]
    }
    }

If the Mapfile contains a value not in this list then an error will be raised. 

For settings such as ``COLOR`` either RGB values or hex codes are allowed. This is accounted for in the schema using the ``oneOf``
property:

.. code-block:: json

    {
    "color": {
        "oneOf": [
            {
                "minItems": 3, 
                "items": {
                    "minimum": -1, 
                    "type": "number", 
                    "maximum": 255
                }, 
                "type": "array", 
                "maxItems": 3
            }, 
            {
                "pattern": "^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$", 
                "type": "string", 
                "example": "#aa33cc"
            }
        ]
    }
    }

How to Validate
---------------

Mapfile validation can either be run using the :ref:`cli`, or directly in Python code:

.. code-block:: python

    s = """MAP
        NAME "sample"
        LAYER
            NAME "test"
            STATUS DEFAULT
            DATA "SELECT GEOM
            FROM
            TABLE"
            TYPE LINEX
        END
    END"""

    d = mappyfile.loads(s, include_position=True)
    v = Validator()
    errors = v.validate(d, add_comments=True, version=7.6)
    for e in errors:
        print(e)

Outputs the following:

.. code-block:: python

    {'column': 9, 'message': 'ERROR: Invalid value in TYPE', 'line': 9, 'error': "u'linex' is not one of [u'chart', u'circle', u'line', u'point', u'polygon', u'raster', u'query', u'annotation']"}

The ``include_position`` parameter can be set to ``True`` when loading a Mapfile (or Mapfile snippet), so that any validation errors
include line positions. 

The optional ``version`` parameter can be used to validate the Mapfile against a specific 
version of MapServer. 

..
    If a ``$ref`` is used then all other properties are ignored. 

        You will always use $ref as the only key in an object: any other keys you put 
        there will be ignored by the validator.

    See https://json-schema.org/understanding-json-schema/structuring.html#reuse

    .. code-block:: json

        "color": {
          "allOf": [
            {
              "$ref": "color.json"
            }
          ],
          "metadata": {
            "deprecated": true,
            "maxVersion": 7.6
          }
        },


..
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

..
    Examples of snippets and validating against sub-schemas

    additionalProperties true to allow for metadata such as __position__

    Any named symmbols which do not exist cause mappyscript to crash
    SIZE when using POLYGON and no SYMBOL - crash

..
    Check that layer, map, and group names are unique or get wrong legends etc.

    Only layers of TYPE POINT are supported for a layer with CLUSTER set
    "enum": [ "ellipse", "rectangle" ] - if add these they are converted to strings without quotes