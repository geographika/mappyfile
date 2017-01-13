mappyfile
=========

.. image:: images/roll-36697_640.png  
    :align: right
    :scale: 50 %
    
A Python library to create and modify `MapServer <http://mapserver.org/documentation.html>`_ Mapfiles. 

+ Python 2 and Python 3 compatible
+ Windows and Linux
+ Pure Python - no issues with mixing C-runtimes for MapServer and other Python libraries

Parsing
-------

Keywords:

+ All the tokens used by MapServer are listed in the following file: https://github.com/mapserver/mapserver/blob/master/maplexer.l
  To create the grammar perhaps this file can itself be parsed to output the tokens? This would help with keeping the two projects in sync.
+ The keywords are also listed at: http://mapserver.org/mapfile/index.html
+ There is also a Lexer for code formatting used for map file code snippets at https://github.com/mapserver/docs/blob/branch-7-0/conf.py (see bottom of file)

Details on the structure of the Mapfile can be found at: http://mapserver.org/mapfile/index.html#notes

Note:

+ The Mapfile is NOT case-sensitive
+ Strings containing non-alphanumeric characters or a MapServer keyword MUST be quoted. It is recommended to put ALL strings in double-quotes.
+ The Mapfile has a hierarchical structure, with the MAP object being the root All other objects fall under this one.
+ Comments are designated with a #.
+ Note C-style comments have recently been added: https://github.com/mapserver/mapserver/pull/5362 - Both single line (e.g. /* foo /) and multi-line comments work.

Including Files
---------------

File paths may be given as absolute paths, or as paths relative to the location of the Mapfile. In addition:

+ Includes may be nested, up to 5 deep.
+ File location can be given as a full path to the file, or as a path relative to the mapfile

http://mapserver.org/mapfile/include.html

.. code-block:: mapfile

    MAP
        NAME "include_mapfile"
        EXTENT 0 0 500 500
        SIZE 250 250

        INCLUDE "test_include_symbols.map"
        INCLUDE "test_include_layer.map"
    END

Design Notes and Questions
--------------------------

#. A new ``mapfile.g`` plyplus grammar file will be created.
#. This should be tested to work with all the available test case sample maps (see :ref:`testing` section below).
#. To allow updates of objects, the best approach may be to use a transformer to change the tree into a ``OrderedDict`` type class? STree objects are read-only? How can STree collections
   be turned into a dictionary type object? It would then need to be turned back into a tree object to use the STransformer class for pretty printing. Alternatively the standard pretty printing
   function could be used directly on the dictionary type Mapfile class?

mappyfile will include a single method, ``parse`` which will return a ``Mapfile`` object, which can be treated in a similar manner to a dictionary.

.. code-block:: python

    mappyfile.parse(string)

This will take any string and attempt to create a valid Mapfile object.
If no valid object can be created a parsing exception will be thrown.

*Unsure on how this will be best achieved. Assuming a single grammar at the Mapfile level, would any subclass need to be wrapped in its parent hierarchy to
parse correctly?*

E.g. a STYLE is associated with a CLASS associated with a LAYER which in turn is associated with a MAP. Other hierarchies and relationships can be seen
on the https://geographika.github.io/mapscript/mapscript.html page.

.. code-block:: bat

    +-------+ 0..*    1 +-------+
    | Style | <-------- | Class |
    +-------+           +-------+

    +-------+ 0..*     1 +-------+
    | Class | <--------> | Layer |
    +-------+            +-------+

     +-----+ 0..1  0..* +-------+
     | Map | <--------> | Layer |
     +-----+            +-------+

.. code-block:: python

    style_string = """
    STYLE
        COLOR 107 208 107
        OUTLINECOLOR 2 2 2
        WIDTH 1
    END
    """

    new_class = mappyfile.parse(style_string)

*Would the library need to take care of this by wrapping the string in a CLASS, LAYER, and MAP object to parse correctly?*

*If so would each need to be a separate method e.g. mappyfile.parse_layer, mappyfile.parse_class etc.*

API Examples
------------

The API is based on Python's configparser API.
https://docs.python.org/3/library/configparser.html#mapping-protocol-access

+ all keys will be lower case
+ all values will be returned as strings by default from the parsing?

Accessing Values
++++++++++++++++

.. code-block:: python

    import mappyfile

    mf = r"C:\MapFiles\example.map"
    mapfile = mappyfile.parse(mf) # will accept a filename or a string

    # print the map name
    print(mapfile["name"]) # would output "MyMap"
    
    # access layers
    layers = mapfile["layers"] # note this will be an OrderedDict-like object

    layer1 = layers.items()[0]
    # depending on if an iterator approach is used may need to do something like the below
    #layer1 = list(d.items())[0] # for Python 3 - http://stackoverflow.com/questions/10058140/accessing-items-in-a-ordereddict

    # access classes in a layer
    classes = layer1["classes"]

    for c in classes:
        print(c["name"])

Modifying Values
++++++++++++++++

.. code-block:: python

    import mappyfile

    mf = r"C:\MapFiles\example.map"
    mapfile = mappyfile.parse(mf)

    # update the map name
    mapfile["name"] = "MyMap"

    # update the error file path in the map config section
    # note key names will always need to be lower case
    mapfile["config"]["ms_errorfile"] = "/ms4w/tmp/ms_error.txt"

    layer = layers.items()[0]
    layer["name"] = "MyLayer"

Adding Items
++++++++++++

Adding a new layer:

.. code-block:: python

    layers = mapfile["layers"]

    new_layer_string = """
    LAYER
        NAME 'land'
        TYPE POLYGON
        DATA '../data/vector/naturalearth/ne_110m_land'
        CLASS
            STYLE
                COLOR 107 208 107
                OUTLINECOLOR 2 2 2
                WIDTH 1
            END
        END
    END
    """

    new_layer = mappyfile.parse(new_layer_string)
    layers.insert(0, new_layer) # can insert the new layer at any index

Adding a new class to a layer:

.. code-block:: python

    layers = mapfile["layers"]
    layer = layers.items()[0]

    new_class_string = """
    CLASS
        STYLE
            COLOR 107 208 107
            OUTLINECOLOR 2 2 2
            WIDTH 1
        END
    END
    """

    new_class = mappyfile.parse(new_class_string)
    layer["classes"].insert(1, new_class) # can insert the new class at any index

Pretty Printing
+++++++++++++++

+ Any ``INCLUDE`` directives will have been parsed and treated as part of the original Mapfile so there will never be any ``INCLUDE`` keywords in the output
+ Should there be an option to include or remove comments?
+ Should the indentation be available as an option? E.g. 2 or 4 spaces?

Taking an input similar to below:

.. code-block:: mapfile

    MAP
    WEB
    METADATA
    "wms_enable_request"  "*"
    END
    END
    PROJECTION
    "init=epsg:4326"
    END

    # START OF THE LAYER DEFINITION
    LAYER
    NAME 'land'
    TYPE POLYGON
    DATA '../data/vector/naturalearth/ne_110m_land'
    # START OF THE CLASS DEFINITION
    CLASS
    # START OF THE STYLE DEFINITION
    STYLE
    COLOR 107 208 107
    OUTLINECOLOR 2 2 2
    WIDTH 1
    END
    END
    END
    END

``mappyfile`` will output a nicely indented version.

.. code-block:: python

    mf = r"C:\Mapfiles\example.map"
    mapfile = mappyfile.parse(mf)

    with open('compact.map', 'w') as mf2:
        mapfile.write(mf2, indent=4, with_comments=False)
        
Output:

.. code-block:: mapfile

    MAP
        WEB
            METADATA
                "wms_enable_request"  "*"
            END
        END
        PROJECTION
            "init=epsg:4326"
        END

        LAYER
            NAME 'land'
            TYPE POLYGON
            DATA '../data/vector/naturalearth/ne_110m_land'
            CLASS
                STYLE
                    COLOR 107 208 107
                    OUTLINECOLOR 2 2 2
                    WIDTH 1
                END
            END
        END
    END
    
Hierarchy
---------

http://mapserver.org/mapscript/mapscript.html#mapscript-classes

Once a Mapfile can be parsed a nice diagram showing the full structure of a Mapfile can be generated similar to the one at https://github.com/erezsh/plyplus#working-with-the-python-ast-using-the-builtin-python-grammar:

.. image:: images/calling_popen.png    

.. _testing:

Testing
-------

Testing - there are many sample Mapfiles available in the testing suite of MapServer:

+ https://github.com/mapserver/mapserver/tree/master/msautotest/misc
+ https://github.com/mapserver/mapserver/tree/master/msautotest/wxs
+ https://github.com/mapserver/mapserver/tree/master/msautotest/renderers
+ https://github.com/mapserver/mapserver/tree/master/msautotest/gdal

These have been downloaded and added to the ``/tests`` folder. This folder also contains a script to download these files again in the future.
