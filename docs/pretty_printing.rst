.. _pretty-printing:
    
Pretty Printing
===============

mappyfile can be used to "pretty print" or format Mapfiles. This can be used to standardise a Mapfile with inconsistent formatting. For example:

.. literalinclude:: examples/before.map
   :language: mapfile

Can be converted using mappyfile to a nicely formatted version using the code below:

.. literalinclude:: examples/pretty_printing.py
   :language: python

The result:

.. literalinclude:: examples/after.map
   :language: mapfile

Formatting of Mapfiles can be applied using the high-level mappyfile API - see :ref:`mapfile-reader-writer-api`, 
or using the command-line :ref:`client-format`. 

Please try the online interactive demo at http://mappyfile.geographika.net/ to experiment with the various formatting options in mappyfile. 

Options
-------

The formatting of the Mapfile output can be configured with several options:

+ **spacer** - the character to use for indenting structures in the Mapfile. Typically spaces or tab characters (``\\t``)
+ **indent** - can be used to set the number of ``spacer`` characters to indent structures in the Mapfile
+ **quote** - the quote character to use in the Mapfile (double or single quotes)
+ **newlinechar** - the character used to insert newlines in the Mapfile
+ **end_comment** - add a comment with the block type at each closing END statement e.g. END # MAP

.. warning::

    When standardising quotes be careful that no quotes chosen for formatting are found within string values. 
    For example large ``DATA`` blocks of SQL may contain single quotes which would then create an invalid Mapfile. 

Examples
--------

The following example loads a Mapfile from a string, and then dumps it back out as a string. A single tab is used for indenting 
blocks of the Mapfile: 

.. code-block:: python

    s = '''MAP NAME "TEST" END'''
    d = mappyfile.loads(s)
    output = mappyfile.dumps(d, indent=1, spacer="\t")
    print(output)

This example adds the block type to its closing ``END`` tag:

    s = '''MAP NAME "TEST" LAYER NAME "Layer1" END END'''
    d = mappyfile.loads(s)
    output = mappyfile.dumps(d, end_comment=True)
    print(output)

.. code-block:: mapfile

    MAP
        NAME "TEST"
        LAYER
            NAME "Layer1"
        END # LAYER
    END # MAP

This example surrounds all attributes with single quotes, and writes the Mapfile directly to disk:

.. code-block:: python

    import tempfile
    s = '''MAP NAME "TEST" LAYER NAME "Layer1" END END'''
    d = mappyfile.loads(s)
    output_file = os.path.join(tempfile.mkdtemp(), 'test_mapfile.map')
    mappyfile.save(d, output_file)

This example writes a Mapfile to an open file object using the ``dump`` function:

.. code-block:: python

    s = """MAP NAME "TEST" END"""
    d = mappyfile.loads(s)
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as fp:
        mappyfile.dump(d, fp)
