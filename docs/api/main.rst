.. _mappyfile-api:

mappyfile API
=============

This page lists the top-level mappyfile API. 

.. contents::
    :local:
    :backlinks: none
    :depth: 2

.. _mapfile-reader-writer-api:

Mapfile Reader and Writer Functions
-----------------------------------

These are functions used to open and write Mapfiles to files and strings. 

+ :func:`mappyfile.open`
+ :func:`mappyfile.load`
+ :func:`mappyfile.loads`
+ :func:`mappyfile.dump`
+ :func:`mappyfile.dumps`
+ :func:`mappyfile.save`
+ :func:`mappyfile.create`

.. automodule:: mappyfile
    :noindex:

    .. autofunction:: open

    .. autofunction:: load

    .. autofunction:: loads

.. _api-dump:

    .. autofunction:: dump

.. _api-dumps:

    .. autofunction:: dumps

.. _api-save:

    .. autofunction:: save

.. _api-create:

    .. autofunction:: create


Dictionary Helper Functions
---------------------------

These are functions to help work with the Mapfile dictionary structure,
such as finding objects by keys. 

+ :func:`mappyfile.find`
+ :func:`mappyfile.findall`
+ :func:`mappyfile.findunique`
+ :func:`mappyfile.findkey`
+ :func:`mappyfile.update`

.. automodule:: mappyfile
    :noindex:

    .. autofunction:: find

    .. autofunction:: findall

    .. autofunction:: findunique

    .. autofunction:: findkey

    .. autofunction:: update

Mapfile Validation Functions
----------------------------

These are functions used to validate Mapfiles, and ensure the match the 
Mapfile schema. See :ref:`validation-docs` for further details. 

+ :func:`mappyfile.validate`

.. _api-validate:

.. automodule:: mappyfile
    :noindex:

    .. autofunction:: validate

.. _yaml-api:

YAML Functions
--------------

These are functions used to read and write Mapfile dictionaries to YAML format.
Requires PyYAML to be installed: ``pip install mappyfile[yaml]``.

+ :func:`mappyfile.yaml.open`
+ :func:`mappyfile.yaml.load`
+ :func:`mappyfile.yaml.loads`
+ :func:`mappyfile.yaml.dump`
+ :func:`mappyfile.yaml.dumps`
+ :func:`mappyfile.yaml.save`

.. automodule:: mappyfile.yaml
    :noindex:

.. _api-yaml-open:

    .. autofunction:: open

.. _api-yaml-load:

    .. autofunction:: load

.. _api-yaml-loads:

    .. autofunction:: loads

.. _api-yaml-dump:

    .. autofunction:: dump

.. _api-yaml-dumps:

    .. autofunction:: dumps

.. _api-yaml-save:

    .. autofunction:: save
