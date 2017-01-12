MappyFile Design Notes
======================

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


