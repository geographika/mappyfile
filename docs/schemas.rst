.. _mapfile-schema:

Mapfile Schema
==============

The full Mapfile schema is shown below. It can also be downloaded directly from this link - :download:`mapfile.json <schemas/mapfile.json>`. 
The current schema is valid for the most recent release of MapServer (7.2). There are plans on the development roadmap to create schemas for
different versions of MapServer, so Mapfiles can be validated against older or newer releases of MapServer to see if they are still valid. 

The Mapfile schema shown below is planned to be proposed as an official Mapfile language schema, subject to voting by the MapServer
PSC (Project Steering Committee). Further details on the schema are outlined in the draft RFC (Request for Comment) at :ref:`rfc123`. 

.. literalinclude:: schemas/mapfile.json
    :language: json

..
    .. include:: schemas/map.rst

    .. include:: schemas/layer.rst

..
    For docs: https://github.com/inspirehep/jsonschema2rst
    Could have different schema for different purposes, e.g. a valid WMS schema. 
    Nested schemas are in the Draft 4 spec only - https://spacetelescope.github.io/understanding-json-schema/structuring.html