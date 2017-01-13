MappyFile Design Notes
======================

Python 2 and Python 3 compatible. 
Windows and Linux. 
Pure Python - no issues with having to match C-runtimes

Parsing
-------

All the tokens used by MapServer are listed in the following file: https://github.com/mapserver/mapserver/blob/master/maplexer.l
To create the grammar perhaps this file can itself be parsed to output the tokens? This would help with keeping the two projects in sync. 

The keywords are also listed at: http://mapserver.org/mapfile/index.html
There is also a Lexer for code formatting used for map file code snippets at https://github.com/mapserver/docs/blob/branch-7-0/conf.py

http://mapserver.org/mapfile/index.html#notes

+ The Mapfile is NOT case-sensitive
+ Strings containing non-alphanumeric characters or a MapServer keyword MUST be quoted. It is recommended to put ALL strings in double-quotes.
+ The mapfile has a hierarchical structure, with the MAP object being the “root”. All other objects fall under this one.
+ Comments are designated with a #.
+ Note C-style comments have recently been added: https://github.com/mapserver/mapserver/pull/5362 - Both single line (e.g. /* foo /) and multi-line comments work. 

Hierarchy
---------

http://mapserver.org/mapscript/mapscript.html#mapscript-classes

Once a MapFile can be parsed a nice diagram showing the full structure of a MapFile can be generated similar to the one at https://github.com/erezsh/plyplus#working-with-the-python-ast-using-the-builtin-python-grammar:

.. image:: images/calling_popen.png

Including Files
---------------

File paths may be given as absolute paths, or as paths relative to the location of the mapfile. In addition,

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

API Examples
------------


The API is based on Python's configparser API. 
https://docs.python.org/3/library/configparser.html#mapping-protocol-access

+ all values will be returned as strings by default from the parsing?

Accessing Values
++++++++++++++++

.. code-block:: python

    import mappyfile
    
    mf = r"C:\MapFiles\example.map"
    mapfile = mappyfile.parse(mf)
    
    # access layers
    layers = mapfile["layers"] # note this will be an OrderedDict
    
    layer1 = layers.items()[0]     
    #layer1 = list(d.items())[0] # for Python 3 - http://stackoverflow.com/questions/10058140/accessing-items-in-a-ordereddict

    # access classes in a layer
    classes = layer1["classes"]
    
    for c in classes:
        print(c["name"])
        
Modifying Values
++++++++++++++++

.. code-block:: python

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

.. code-block:: python

    mf = r"C:\MapFiles\example.map"
    mapfile = mappyfile.parse(mf)
    
    with open('compact.map', 'w') as mf2:
    mapfile.write(mf2)

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
    
mappyfile will output a nicely indented version. 

*Can there be an option to include or remove comments?*

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