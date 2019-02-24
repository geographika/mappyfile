.. _rfc123:

=========================================================================
MS RFC 123: Mapfile JSON Schema
=========================================================================

:Date:  2018/03
:Author: Seth Girvin
:Contact: sethg@geographika.co.uk
:Status: Proposed
:Version: MapServer 7.4

1. Introduction and Background
==============================

Writing Mapfiles is often done by hand, and errors only become apparent when a
map is generated from its Mapfile. This proposal recommends defining a JSON 
schema for the full Mapfile syntax to allow for validation of a Mapfile. 
Validating a Mapfile against a schema has the following advantages:

+ warn of incorrect keywords
+ warn of an invalid structure
+ more comprehensive and consistent documentation
+ warnings of deprecated keywords
+ a parseable definition of the Mapfile language allowing the creation of Mapfile-related syntaxes
  for the Ace Editor, Pygments, VIM etc. 

In addition it is proposed metadata for each attribute is added recording
which version of MapServer introduced a keyword, and if it has been deprecated the 
last version it was valid. 

A similar proposal was made in 2009 to introduce an XML schema for Mapfiles - 
see RFC 51. 

Storing the full Mapfile syntax in a machine-parseable format opens up other possibilities
such as automating the generation of the Mapfile syntax documentation. 

mappyfile nested dictionary structure. independent of this. Any language could be
used to create a Mapfile JSON object for validation. Printing functionality would also 
need to be created to convert the structure back to a Mapfile - however this step is
much easier than the initial parsing of the Mapfile and transformation to a dictionary 
structure. Along with the Python example in mappyfile, a JavaScript port of the pretty-printer
class should be fairly straight-forward. 

language independent

mappyfile. Web and JavaScript. 
JavaScript example. 

A first pass at a JSON Schema definition for each MapServer class has been attempted
and can be seen at TO ADD. These need to be throroughly reviewed prior to adding to 
the MapServer repository. 

UIs come and go but the Mapfile remains!

2. Implementation Details
=========================

JSON4 schema. 

New properties and object definitions will only be added to the schema, however no
properties will be removed, only marked as deprecated to allow validation for different versions
of MapServer. 

This approach will also mean the schema itself won't need to be versioned
TODO is this correct?
Metadata deprecated property would require custom checks. 


2.1 Schema Files
----------------

Each of the Mapfile classes - that is structures defined in the ``TYPE...END``
blocks, will have its own JSON Schema file. For example
a ``LAYER`` object is stored in a `layer.json <TODO ADD GITHUB LINK>`_ file. 

For certain attributes that are used in different locations in a Mapfile these
will be split out into their own schema to enable easier reuse e.g. ``EXTENT`` 
values, ``ON`` and ``OFF`` settings, and ``COLOR`` properties. 

A Python script can be provided and run as a pre-release step to the documentation builds 
that will do the following:

+ Merge the long-form documentation and JSON Schema into single documentation pages
+ Merge all the individual JSON Schema files into a single-file for easier
  distribution with a link to this file added to the MapServer documentation. This 
  merged file can also be used by the latest mappyfile distribution. 

2.2 Mapfile Classes
-------------------

Each Mapfile class will start with the standard JSON Schema properties:

.. code-block:: json

    {
        "type": "object",
        "required": [ "type" ],
        "additionalProperties": false,
        "properties": {
        }
    }

If MapServer requires any of the properties to be set, then these properties 
are listed in ``required`` property of the object. For example without a ``LAYER`` 
missing a ``TYPE`` property will throw an error in MapServer. 

The ``additionalProperties`` property defines whether or not the object can 
have properties not listed in the schema. In the majority of cases this will be 
set to ``false``, as any keywords not listed in the schema will be invalid. 

In cases where arbitrary keywords can be set such as ``METADATA`` and ``VALIDATION``
objects the ``additionalProperties`` will be set to ``true``. When any values are allowed
the JSON Schema definition is left open as follows:

.. code-block:: json

    {
      "type": "object",
      "properties": {
      },
      "additionalProperties": true
    }

If there is a known set of values these will be listed, along with the option to arbitrarily
add more, e.g. the ``CONFIG`` settings:

.. code-block:: json

    {
        "config": {
          "type": "object",
          "properties": {
            "CGI_CONTEXT_URL": { "type": "string" },
            "MS_ENCRYPTION_KEY": { "type": "string" },
            "ON_MISSING_DATA": {
              "type": "string",
              "enum": [ "FAIL", "LOG", "IGNORE" ]
            },
          },
          "additionalProperties": true
         }
     }

If any of the properties in a class are themselves classes then they will be 
referenced using the ``$ref`` property pointing to the relevant .json file. For example
a ``LAYER`` can contain a ``METADATA`` object. This schema is referenced as
follows:

.. code-block:: json

    {
        "metadata": {
          "$ref": "metadata.json"
        }
    }

+ TODO add "include":  "string"
+ Can't include   "required": [ "type" ] in layer as this could be in an include
+ "__position__"

2.3 Arrays of Mapfile Classes
-----------------------------

Several Mapfile classes can be repeated within their parent class, for 
example a ``LAYER`` can have many ``CLASS`` objects, or several ``FEATURE``
objects. In these cases the property name will be set to the plural, and will
be of type ``array``:

.. code-block:: json

    {
        "features": {
          "type": "array",
          "items": {
            "$ref": "feature.json"
          }
        }
    }

In most cases this will be simply be adding an "s" e.g. feature(s), layer(s). 
In the case where the property already ends with an "s", then "es" will be used,
e.g. class(es). 

2.4 Property Definitions
------------------------

Most property definitions are self-explanatory, for example a ``MAP`` can have
an ``ANGLE`` property, and a ``LEGEND`` can have a ``STATUS`` property. 
These are of type ``numeric``, ``string``, and ``enumeration`` respectively. 

.. code-block:: json

    {
        "angle": {
          "type": "number"
        },
        "imagetype": {
          "type": "string"
        },
        "status": {
          "type": "string",
          "enum": [ "on", "off", "embed" ]
        }
    }

Other properties are more complicated. For example the ``COLOR`` property is used
in several locations in the Mapfile. This can accept either an RGBA value, or an
HTML color code. 

.. code-block:: json

    {
      "oneOf": [
        {
          "type": "array",
          "items": {
            "type": "number",
            "minimum": 0,
            "maximum": 255
          },
          "minItems": 3,
          "maxItems": 3
        },
        {
          "pattern": "^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$",
          "example": "#aa33cc",
          "type": "string"
        }
      ]
    }


2.5 Property Metadata
---------------------

The recommended approach to storing metadata in a JSON schema is in 
a ``metadata`` attribute TODO ADD LINK. Metadata will only be added for attributes which 
have been deprecated or recently introduced in to the Mapfile syntax. Recent is defined here 
as if it is still currently mentioned in the documentation. 

For example the ``LABELMAXSCALE`` attribute on a ``LAYER`` object was deprecated
in MapServer version 5.0 (according to the documentation). Without digging into the 
source code history the version the attribute was introduced is unknown. In this case the
``minVersion`` will be set to 0. 

.. code-block:: json

    {
        "labelmaxscale": {
          "type": "number",
          "metadata": {
            "deprecated": true,
            "minVersion": 0,
            "maxVersion": 5.0
          }
        }
    }

Another standard JSON Schema property that will be used occastionally in the
schema is the ``example`` property TODO ADD LINK. This will primarily be used 
to document examples of valid values to list in the MapServer documentation. 
For example one of the valid values for a ``COLOR`` property is an HTML color code. 
An example value is listed in the property definition. 

.. code-block:: json

    {
        "pattern": "^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$",
        "example": "#aa33cc",
        "type": "string"
    }

3. Documentation Changes
========================

Currently the MapServer Mapfile syntax is documented in restructured text (RST). 

The `jsonschema2rst <https://github.com/inspirehep/jsonschema2rst>`_ project converts a 
JSON schema into RST. 

It is proposed that the current document's structure is modified to make it easier to comnbine
the existing long-form documentation, with the JSON Schema details, and removing any
duplication between the two. 

It is important the long-form text can be easily edited and examples added, so this approach
aims to enhance the hand-written documentation rather than replace it. 

This would avoid issues such as https://github.com/mapserver/mapserver/issues/5748

4. Online Validator
===================

JavaScript-based validator?
Select version. Default to latest (7.2). 

5. Implementation Details
=========================

5.1 Affected files
------------------

+ no code files will require modifications
+ all documentation in the ``/mapfile`` folder could gradually be restructured
  to allow the insertion of property definitions from the JSON Schema

5.2 Tracking Issue
------------------

TBD

6. Discussion
=============

+ Multipoints
+ Use of __type__ attributes?
+ Are there any other attribute or type metadata values that could / should
  be stored?

7. Voting History
=================

