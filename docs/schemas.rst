.. _mapfile-schema:

Mapfile Schema
==============

The full Mapfile schema can be downloaded directly from this link - :download:`mapfile-latest.json <schemas/mapfile-latest.json>`. 
The schema stores ``minVersion`` and ``maxVersion`` properties in a ``metadata`` object for each keyword. This allow Mapfiles to be validated against
older or newer releases of MapServer to see if they are still valid. 

Other versions available online are:

+ :download:`mapfile-schema-8-0.json <schemas/mapfile-schema-8-0.json>`
+ :download:`mapfile-schema-7-6.json <schemas/mapfile-schema-7-6.json>`

The Mapfile schema shown below is planned to be proposed as an official Mapfile language schema, subject to voting by the MapServer
PSC (Project Steering Committee). Further details on the schema are outlined in the draft RFC (Request for Comment) at :ref:`rfc123`. 

Exporting the Schema
++++++++++++++++++++

The schema can be exported via the command-line using the following syntax:

.. code-block:: bat

    mappyfile schema mapfile-schema-7-6.json --version=7.6

The schema can be exported using Python, as shown in the example below:

.. code-block:: python

    import json
    from mappyfile.validator import Validator

    validator = Validator()
    jsn = validator.get_versioned_schema(version=8.0)
    print(json.dumps(jsn, indent=4))

Creating a Mappyfile Object with Defaults
+++++++++++++++++++++++++++++++++++++++++

If MapServer uses default values for an object, the `create` function can be used to create
a new object using these defaults. For example to output a `MAP` object with default settings
run the following code:

.. code-block:: python

    import json
    import mappyfile

    m = mappyfile.create("map", version=8.0)
    print(json.dumps(m, indent=4, sort_keys=True))
    mappyfile.dumps(m)

This outputs the following:

.. code-block:: mapfile

    MAP
        ANGLE 0
        DEBUG 0
        DEFRESOLUTION 72
        IMAGETYPE "png"
        MAXSIZE 4096
        NAME "MS"
        RESOLUTION 72
        SIZE -1 -1
    END

Notes
-----

``enum`` is used to check attribute keywords, and output them without quotes by the pretty printer. The ``CLUSTER`` ``REGION`` keyword
is a fixed list, but has to be a string and output in quotes, therefore the following construct is used:

.. code-block:: json

    "type": "string",
    "pattern": "^rectangle$"

..
    For docs: https://github.com/inspirehep/jsonschema2rst
    Could have different schema for different purposes, e.g. a valid WMS schema. 
    Nested schemas are in the Draft 4 spec only - https://spacetelescope.github.io/understanding-json-schema/structuring.html