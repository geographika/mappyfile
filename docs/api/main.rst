.. _mappyfile-api:

mappyfile API
=============

This page lists the top-level mappyfile API. 

Mapfile Reader and Writer Functions
-----------------------------------

These are functions used to open and write Mapfiles to files and strings. 

+ :func:`mappyfile.open`
+ :func:`mappyfile.load`
+ :func:`mappyfile.loads`
+ :func:`mappyfile.dump`
+ :func:`mappyfile.dumps`
+ :func:`mappyfile.save`

.. automodule:: mappyfile

    .. autofunction:: open

    .. autofunction:: load

    .. autofunction:: loads

.. _api-dump:

    .. autofunction:: dump

.. _api-dumps:

    .. autofunction:: dumps

.. _api-save:

    .. autofunction:: save


Dictionary Helper Functions
---------------------------

Summary
+++++++

These are functions to help work with the Mapfile dictionary structure,
such as finding objects by keys. 

+ :func:`mappyfile.find`
+ :func:`mappyfile.findall`
+ :func:`mappyfile.findunique`
+ :func:`mappyfile.findkey`
+ :func:`mappyfile.update`

.. automodule:: mappyfile

    .. autofunction:: find

    .. autofunction:: findall

    .. autofunction:: findunique

    .. autofunction:: findkey

    .. autofunction:: update

Mapfile Validation Functions
----------------------------

Summary
+++++++

These are functions used to validate Mapfiles, and ensure the match the 
Mapfile schema. 

+ :func:`mappyfile.validate`

.. automodule:: mappyfile

.. _api-validate:

    .. autofunction:: validate