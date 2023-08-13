Parsing
=======

This page documents the parsing process used by mappyfile to parse Mapfiles. 
mappyfile uses `lark <https://github.com/lark-parser/lark>`_ as the parsing engine. 

MapFile Keywords
++++++++++++++++

Links to the keywords that are used within Mapfiles:

+ All the tokens used by MapServer are listed in the following file: https://github.com/mapserver/mapserver/blob/main/maplexer.l
+ Keywords are also listed at: https://mapserver.org/mapfile/index.html
+ There is a Sphinx RegexLexer for code formatting at https://github.com/mapserver/docs/blob/main/conf.py (see bottom of file)

MapFiles
++++++++

Details on the structure of the Mapfile can be found at https://mapserver.org/mapfile/#notes:

+ The Mapfile is NOT case-sensitive
+ Strings containing non-alphanumeric characters or a MapServer keyword MUST be quoted. It is recommended to put ALL strings in double-quotes.
+ The Mapfile has a hierarchical structure, with the MAP object being the root All other objects fall under this one.
+ Comments are designated with a #.
+ C-style comments were added in 2017: https://github.com/mapserver/mapserver/pull/5362 - both single line (e.g. ``/* foo */``) and multi-line comments work.

Hierarchy
+++++++++

A summary of all the main Mapfile components is shown below. These are directives that are in the form ``TYPE..END``. 

.. image:: images/map_classes.png

The ``LAYER`` type has been split out into its own diagram due to its more complex nature:

.. image:: images/layer_classes.png

Mapfile Notes
+++++++++++++

This section details the various declaration types found in a Mapfile. 

* Quoted strings. Used for quoted property values e.g.

  .. code-block:: mapfile

     NAME "Layer1"
     DATA "lakes.shp"

* Non-quoted lists. E.g. a POINTS block can be defined as follows:

  .. code-block:: mapfile
  
      POINTS
          0 100
          100 200
          40 90
      END

* Quoted lists. Used for property lists that should be quoted. E.g. the PROJECTION block can be defined as follows:

  .. code-block:: mapfile

      PROJECTION
          'proj=utm'
          'ellps=GRS80'
          'datum=NAD83'
          'zone=15'
          'units=m'
          'north'
          'no_defs'
      END

* Key-value lists:

  .. code-block:: mapfile

      PROCESSING "BANDS=1"
      PROCESSING "CONTOUR_ITEM=elevation"
      PROCESSING "CONTOUR_INTERVAL=20"

* Key-double-value lists. As above but there are two strings for each directive:

  .. code-block:: mapfile
  
        CONFIG MS_ERRORFILE "stderr"
        CONFIG "PROJ_DEBUG" "OFF"
        CONFIG "ON_MISSING_DATA" "IGNORE"

* Composite types- container declarations which finish with the
  keyword END. Examples:
    
  .. code-block:: mapfile

     MAP ... END
     LAYER ... END
     CLASS ... END
     STYLE ... END


Including Files
+++++++++++++++

The parser allows for files (containing further Mapfile declarations) referenced in the Mapfile to be loaded and parsed. Notes on the ``INCLUDE`` 
directive can be found at https://mapserver.org/mapfile/include.html:

+ Includes may be nested, up to 5 deep.
+ File locations can be given as a full path to the file, or as a path relative to the Mapfile
+ If a string is provided to the ``parse`` method, then an optional ``root_folder`` parameter can be used
  to work with relative paths

.. code-block:: mapfile

    MAP
        NAME "include_mapfile"
        EXTENT 0 0 500 500
        SIZE 250 250

        INCLUDE "test_include_symbols.map"
        INCLUDE "C:\Includes\test_include_layer.map"
    END

Parsing Notes
+++++++++++++

The Mapfile has a very flexible syntax, this section points out some of those syntax features, 
explains their significance to parsing, and detail the solution to accommodate them.

Unquoted Strings
----------------

Most programming languages insist that all strings are quoted. Unquoted strings can lead to a lot of ambiguity, as it does in the Mapfile format.
For example, in the line:

.. code-block:: mapfile

    TYPE LINE

It is unclear to the lexer (short for "lexical analyzer" that is responsible for converting a Mapfile into tokens)
if ``LINE`` is a command like ``TYPE``, or a string. In this case of course it's a string, but it's left to the parser to disambiguate it. This
is not always simple process.

In our parser, we simply allowed for attribute names as a value. In post-processing, we treat them the same as strings.

Composite and Attribute Ambiguity
---------------------------------

Two composite names - ``STYLE`` and ``SYMBOL``, are also attribute names. For example:

.. code-block:: mapfile

    # a style block
    STYLE
        OUTLINECOLOR 0 255 0 
    END

    QUERYMAP
        # a style attribute
        STYLE SELECTED
        COLOR 255 0 0
    END

This above example is not a problem to parse, but it becomes very tricky when compounded by the next issue - line-breaks.

Resolving the `SYMBOL ambiguity <https://github.com/geographika/mappyfile/issues/48>`_ issue required the use of an interactive LALR
parser. See `this commit <https://github.com/geographika/mappyfile/commit/96ca51720c6275ae1979dc6391be72fa3b0c72af>`_ for details.


Line-Break Fluidity
-------------------

On its surface, the Mapfile format appears very consistent in its line-break usage. But actually, there is a lot of variance allowed. For example:

.. code-block:: mapfile

    STYLE  COLOR 255 0 0  END

Containers can be placed completely on one line, but also partially:

.. code-block:: mapfile

    LAYER DEBUG 5
    GROUP "default"
    ...
    END

In this example, both attributes belong to ``LAYER``, but only one of them is on the same line.

In this last example, we see a culmination of all 3 issues to create a high-level of ambiguity.
It's impossible to know if ``LAYER`` here is a composite or an attribute. Only after looking much further ahead, could a smart parser figure it out.

..
    https://news.ycombinator.com/item?id=10222681
    http://loup-vaillant.fr/tutorials/earley-parsing/what-and-why
    http://loup-vaillant.fr/tutorials/earley-parsing/right-recursion
    https://www.reddit.com/r/programming/comments/3j0zfu/fast_handy_languages_an_article_about_fast_marpa/