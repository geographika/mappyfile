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

#. A new ``mapfile.g`` plyplus grammar file will be created.
#. This should be tested to work with all the available test case sample maps (see :ref:`testing` section below).

Keywords
++++++++

+ All the tokens used by MapServer are listed in the following file: https://github.com/mapserver/mapserver/blob/master/maplexer.l
  To create the grammar perhaps this file can itself be parsed to output the tokens? This would help with keeping the two projects in sync.
+ The keywords are also listed at: http://mapserver.org/mapfile/index.html
+ There is also a Lexer for code formatting used for map file code snippets at https://github.com/mapserver/docs/blob/branch-7-0/conf.py (see bottom of file)

MapFiles
++++++++

Details on the structure of the Mapfile can be found at: http://mapserver.org/mapfile/index.html#notes

+ The Mapfile is NOT case-sensitive
+ Strings containing non-alphanumeric characters or a MapServer keyword MUST be quoted. It is recommended to put ALL strings in double-quotes.
+ The Mapfile has a hierarchical structure, with the MAP object being the root All other objects fall under this one.
+ Comments are designated with a #.
+ Note C-style comments have recently been added: https://github.com/mapserver/mapserver/pull/5362 - Both single line (e.g. ``/* foo */``) and multi-line comments work.

Design Notes
++++++++++++

``mappyfile`` will include a single method, ``parse`` which will return a ``Mapfile`` object, which can be treated in a similar manner to a dictionary.

.. code-block:: python

    # a file name can be sent to the parse function
    mappyfile.parse(filename)
    
    # alternatively a string containing Mapfile syntax can be parsed directly
    mappyfile.parse(string)
    
    # if the string contains INCLUDE references then an optional root_folder can
    # be passed to the parse method that can be used for relative paths
    mappyfile.parse(string, root_folder=r"C:\Data")    

This will take a string, or read the contents of a file and attempt to create a valid Mapfile tree or object. If no valid object can be created a parsing exception will be thrown.

*Unsure on how this will be best achieved. Assuming a single grammar at the Mapfile level, would any subclass need to be wrapped in its parent hierarchy keywords to parse correctly?*

E.g. a STYLE is associated with a CLASS associated with a LAYER which in turn is associated with a MAP. 

.. code-block:: python

    style_string = """
    STYLE
        COLOR 107 208 107
        OUTLINECOLOR 2 2 2
        WIDTH 1
    END
    """

    new_class = mappyfile.parse(style_string)

+ *Would mappyfile need to take care of this by wrapping the STYLE string in a CLASS, LAYER, and MAP keywords to parse correctly?*
+ *If so would each need to be a separate method e.g. mappyfile.parse_layer, mappyfile.parse_class etc. ?*

Other hierarchies and relationships can be seen on the http://www.mapserver.org/mapscript/mapscript.html#mapscript-classes page.

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
     
Including Files
+++++++++++++++

The parser will also need to allow for files (containing further Mapfile declarations) referenced in the Mapfile to be loaded and parsed. 

+ Includes may be nested, up to 5 deep.
+ File location can be given as a full path to the file, or as a path relative to the Mapfile
+ If a string is provided to the ``parse`` method, then an optional ``root_folder`` parameter can be used
  to work with relative paths

See http://mapserver.org/mapfile/include.html for further details. 

.. code-block:: mapfile

    MAP
        NAME "include_mapfile"
        EXTENT 0 0 500 500
        SIZE 250 250

        INCLUDE "test_include_symbols.map"
        INCLUDE "C:\Includes\test_include_layer.map"
    END

*Is it easy to have an option to not process the INCLUDEs and leave them as a simple line of text?*

Processing the Parsed File
--------------------------

+ *To allow updates of objects and properties would the best approach may be to use a transformer to change the tree into a OrderedDict type class? 
  STree objects are read-only?*
+ *How can STree collections be turned into a nested dictionary type object?*
  It would then need to be turned back into a tree object to use the STransformer class for pretty printing and creating diagrams. 
  *Alternatively a pretty printing function could be used directly on the dictionary type Mapfile class?* The pydot diagrams however are a nice feature. 
+ Could one approach be to write the dict to a Mapfile string and reparse this for diagrams?

For example taking the Mapfile below:

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
            NAME 'layer1'
            CLASS
                NAME 'class1'
                STYLE
                    COLOR 107 208 107
                    WIDTH 1
                END
            END
            CLASS
                NAME 'class2'
                STYLE
                    COLOR 10 108 207
                    WIDTH 1
                END
            END			
        END
        LAYER
            NAME 'layer2'
            CLASS
                STYLE
                    COLOR 99 231 117
                    WIDTH 1
                END
            END
        END		
    END
	
Would become a nested dictionary similar to below. 

.. code-block:: python

    {
      "map": {
        "web": {
          "metadata": {
            "wms_enable_request": "*"
          }
        },       
        "projection": ["init=epsg:4326"],      
        "layers": {
          "layer1": {
            "name": "layer1",
            "classes": {
              "class1": {
                "name": "class1", 
                "styles": {
                  "0": {
                    "color": "107 208 107", 
                    "width": 1
                  }
                }
              }, 
              "class2": {
                "name": "class2", 
                "styles": {
                  "0": {
                    "color": "10 108 207", 
                    "width": 1
                  }
                }
              }
            }
          }, 
          "layer2": {
            "name": "layer2",
            "classes": {
              "0": {
                "styles": {
                  "0": {
                    "color": "99 231 117", 
                    "width": 1
                  }
                }
              }
            }
          }
        }
      }
    }
    
Notes on the above:

+ Objects that can have multiple instances in a Mapfile will be stored as a OrderedDict of Dicts (as order is important).
  The ``NAME`` value of the object will be used for the key. If this is not present then the index can be used.  These keys ignored when outputting 
  the representation back to a Mapfile. 
+ Most objects have a set of key/value pairs. ``PROJECTION`` however should be treated as a list 
  (see http://www.mapserver.org/mapfile/projection.html).
+ Some keys are already quoted e.g. in the ``METADATA`` object items such as "wms_enable_request" are strings rather than keywords. Maybe values need to be tuples to
  record this e.g. ``"wms_enable_request": ("*", False)`` where ``False`` is to indicate the key is not a keyword. This can be checked when outputting to text so the key is quoted. 
+ Some keys are duplicated within an object. E.g.

  .. code-block:: mapfile
  
        PROCESSING "BANDS=1"
        PROCESSING "CONTOUR_ITEM=elevation"
        PROCESSING "CONTOUR_INTERVAL=20"
        
        # Same for POINTS
        
  Could turn this into a list? E.g.
  
  .. code-block:: python
  
      "layer": {
        "processing": ["BANDS=1", "CONTOUR_ITEM=elevation", "CONTOUR_INTERVAL=20"]
      }
      
      # to update and manipulate then use an API such as below
      layer["processing"][0] = "BANDS=1,2,3"

  
Implementation Notes
++++++++++++++++++++

+ Use iterators for the dicts? See http://stackoverflow.com/a/4391722/179520 for making these iterators. 
+ If iterators are used then they will need to be converted to lists when accessed

  .. code-block:: python

	  # depending on if an iterator approach is used may need to do something like the below
	  layers = list(d.items()) # for Python 3 and iterator approach- http://stackoverflow.com/questions/10058140/accessing-items-in-a-ordereddict

+ Could make use of https://github.com/bcj/AttrDict to allow property-like access to dictionary objects (see proposed API examples below)?
	
API Examples
------------

This section details the proposed use of the ``mappyfile`` library. The API will be similar to Python's `configparser API <https://docs.python.org/3/library/configparser.html#mapping-protocol-access>`_. 

+ all keys will be lower case
+ all values will be returned as strings by default from the parsing (assume this is the case, or could convert integers etc.)

Accessing Values
++++++++++++++++

.. code-block:: python

    import mappyfile

    mf = r"C:\MapFiles\example.map"
    mapfile = mappyfile.parse(mf) # parse will accept a filename or a string

    # print the map name
    print(mapfile["name"]) # would output "MyMap"
       
    # access layers
    layers = mapfile["layers"]
    layer1 = layers[0] # access by index
	
    layer2 = layers["layer2"] # access by layer NAME property
	
    # access classes in a layer
    classes = layer1["classes"]

    for c in classes:
        print(c["name"])

    # if the AttrDict approach is taken then the following could also be used
    # could be added for a more polished version
    
    print(mapfile.name) 
    layer2 = layers.layer2
    print(layer2.classes[0].name)
    
Modifying Values
++++++++++++++++

.. code-block:: python

    import mappyfile

    mf = "ms4w/mapfiles/example.map"
    mapfile = mappyfile.parse(mf)

    # update the map name
    mapfile["name"] = "MyMap"

    # update the error file path in the map config section
    # note key names will always need to be lower case
    mapfile["config"]["ms_errorfile"] = "/ms4w/tmp/ms_error.txt"

    layer = layers[0]
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

    layer = mapfile["layers"]["MyLayer"]

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

Multiple objects can also be parsed and inserted: 

.. code-block:: python

    layer = mapfile["layers"][0]

    new_styles_string = """
    STYLE
            COLOR 107 208 107
            OUTLINECOLOR 2 2 2
            WIDTH 1
    END
    STYLE
            COLOR 99 231 117
            OUTLINECOLOR 2 2 2
            WIDTH 1
    END	
    """

    new_styles = mappyfile.parse(new_styles_string)
    layer["classes"].insert(1, new_styles) # can insert the new class at any index
	
.. _pretty-printing:
    
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
+++++++++

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

Future Development
------------------

+ Enable MapServer to accept a "Mapfile" as a stream: https://github.com/mapserver/mapserver/issues/4031
