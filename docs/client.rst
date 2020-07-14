.. _cli:

Command-line Interface
======================

mappyfile includes two command line applications, :ref:`client-format` and :ref:`client-validate`. A command line interface (CLI), allows mappyfile 
to be easily integrated into Continuous Integration (CI) platforms such as Travis and Appveyor, and to automate validation and formatting
of Mapfiles. 

.. _client-format:

format
------

The ``format`` command can be used to apply consistent formatting and whitespace to a Mapfile, and to remove comments. 
It has the same parameters as the :ref:`save <api-save>` function. 

To format ``valid.map`` to a new ``valid_formatted.map`` file using the default formatting settings use the following syntax: 

.. code-block:: bat

    mappyfile format valid.map valid_formatted.map

Other examples are included in the ``help`` documentation for the command, shown below. To display this at the command line run 
the following: 

.. code-block:: bat

    mappyfile format --help

.. literalinclude:: format.txt
    :language: console

..
    echo run from python3 as click in Python2 doesn't pick up the correct terminal size when redirecting to a file
    mode con:cols=250
    mappyfile format --help > docs/format.txt

.. _client-validate:

validate
--------

The ``validate`` command can be used to check values used in a Mapfile are valid, by comparing its contents to the Mapfile
schema. It has the same parameters as the :ref:`validate <api-validate>` function. 

mappyfile also allows validation against different versions of MapServer, for example validating Mapfiles 
for MapServer 7.0, or for 7.6. 

.. note::

    When using wildcards to search for Mapfiles the Python ``glob`` module is used on Windows. This only searches subfolders
    that are one level-deep. On Linux wildcards are typically expanded in the shell, so Mapfiles in subfolders of any depth can 
    be validated. 

If validation errors are encountered in the Mapfile they will be displayed in the console output similar to below:

.. literalinclude:: validation_errors.txt
    :language: console

Example 1
+++++++++

To validate all Mapfiles in the ``ms-ogc-workshop`` folder and all subfolders:

.. code-block:: bat

    mappyfile validate D:\ms-ogc-workshop\ms4w\apps\ms-ogc-workshop\**\*.map

Example 2
+++++++++

To validate a single Mapfile, without expanding any ``INCLUDE`` directives:

.. code-block:: bat

    mappyfile validate /world.map --no-expand

Example 3
+++++++++

To validate a Mapfile for version 7.6 of MapServer:

.. code-block:: bat

    mappyfile validate /world.map --version=7.6

To display the command's help text run the following: 

.. code-block:: bat

    mappyfile validate --help

.. literalinclude:: validate.txt
    :language: console

..
    echo run from python3 as click in Python2 doesn't pick up the correct terminal size when redirecting to a file
    mode con:cols=200
    mappyfile validate --help > docs/validate.txt
    mappyfile validate C:/Temp/*.map > docs/validation_errors.txt

.. _client-schema:

schema
------

Save the Mapfile schema to a file. Set the version parameter to output a specific version.

.. code-block:: bat

    mappyfile schema --help

.. literalinclude:: format.txt
    :language: console