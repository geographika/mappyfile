Parsing
=======

mappyfile uses Lark as the parsing engine. 

#. A new ``mapfile.g`` grammar file will be created.
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


Benchmarking
------------

I chose to use the Earley algorithm due to unexpected flexibility in the syntax of the mapfiles. (I can expand on that subject if you wish )
However, many of the files can still be parsed using PLY.
You may notice that the test script tries parsing with PLY first and only falls back to Earley if it fails. 
It's not necessary but it's about 3 times faster under CPython. Or you may choose to use Pypy, which is the 
fastest just with the Earley parser.

Here are some benchmarks from my PC for parsing all 301 files (2MB):

* Pypy: 3.5 seconds
* CPython: 15 seconds
* CPython with fallback