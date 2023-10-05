Releases
--------

1.0.0 28/09/2023
++++++++++++++++

In celebration of becoming an official `OSGeo Community Project <https://www.osgeo.org/projects/mappyfile/>`_, 
a version ``1.0.0`` release is now out!

+ **Support for Python 2.7 has now been dropped.**
  See `#166 <https://github.com/geographika/mappyfile/issues/166>`_ - Drop Python 2.7 support. The codebase has had all Python2 specific
  code removed - see `#188 <https://github.com/geographika/mappyfile/issues/188>`_.

+ **Breaking Change** - in the ``MapfileToDict`` class the parameter ``transformerClass`` has been renamed ``transformer_class``.
  An example of how to fix this is shown below:

  .. code-block:: python

    from mappyfile.transformer import MapfileToDict
    from mappyfile_colors import ColorsTransformer

    m = MapfileToDict(
        include_position=True,
        include_comments=True,
        # replace the following parameter
        # transformerClass=ColorsTransformer,
        transformer_class=ColorsTransformer,
        conversion_type=None,
        include_color_names=True,
    )

+ **Breaking Change** - ``LAYER`` ``DATA`` has been changed in the schema from a list to a simple string.

  .. code-block:: python

      layer = {
          '__type__': 'layer',
          // pre v1 the data clause had to be in a list
          // 'data': ['/path/to/data']
          // in v1 this should now be a string
          'data': '/path/to/data'
      }

      mappyfile.dumps(layer)

+ Support added for `lark_cython <https://github.com/lark-parser/lark_cython>`_ - see `#178 <https://github.com/geographika/mappyfile/issues/178>`_ - thanks @erezsh.
  To use ``lark_cython`` is as simple as installing the option with ``pip``:

  .. code-block:: bash

      pip install mappyfile[lark_cython]

+ All mappyfile dicts now have human readable output when displayed as a string:

  .. code-block:: python

    mf = mappyfile.open("./docs/examples/before.map")
    print(mf)

    # previous output
    # DefaultOrderedDict(<class 'mappyfile.ordereddict.CaseInsensitiveOrderedDict'>, CaseInsensitiveOrderedDict([('__type__', 'map'),..

    # new output
    {
        "__type__": "map",
        "layers": [
            {
                "__type__": "layer",
                "name": "Layer1",
                "type": "POLYGON"
            },

+ Approach to resolving JSON references updated due to the deprecated ``jsonschema.RefResolver`` - see 
  `this link <https://python-jsonschema.readthedocs.io/en/v4.18.4/referencing/#resolving-references-from-the-file-system>`_,
  the associated JSONSchema `pull request <https://github.com/python-jsonschema/jsonschema/pull/1049>`_
  and the `migration approach <https://python-jsonschema.readthedocs.io/en/stable/referencing/#migrating-from-refresolver>`_.

Other improvements and fixes in the v1.0.0 release:

+ `#196 <https://github.com/geographika/mappyfile/pull/196>`_ - Code base fixes for ``Prospector`` warnings
+ `#195 <https://github.com/geographika/mappyfile/pull/195>`_ - Update test suite from latest msautotests
+ `#194 <https://github.com/geographika/mappyfile/pull/194>`_ - Docs overhaul in preparation for v1 release
+ `#193 <https://github.com/geographika/mappyfile/pull/193>`_ - Update to ``jsonschema`` v4 and replace deprecated ``RefResolver``
+ `#191 <https://github.com/geographika/mappyfile/pull/191>`_ - Simplify processing of comments
+ `#189 <https://github.com/geographika/mappyfile/pull/189>`_ - Add type hints to the code base
+ `#153 <https://github.com/geographika/mappyfile/pull/153>`_ - Support querying items without the given key in 
  ``utils.findunique()``- thanks @DonQueso89 for fix
+ Schema fixes for ``grid``, ``label``, ``style``, ``leader``, add ``flatgeobuf``
+ Code reformatted using `black <https://pypi.org/project/black/>`_

Resolution of long-standing parsing issues, and all msautotest examples now pass successfully:

+ `#48 <https://github.com/geographika/mappyfile/issues/48>`_ - SYMBOL ambiguity
+ `#98 <https://github.com/geographika/mappyfile/issues/98>`_ - Unquoted attribute names fail to parse


0.9.7 03/04/2022
++++++++++++++++

+ Fix ""ResourceWarning: unclosed"" when reading mapfile.lark in Python 3.10
+ `#151 <https://github.com/geographika/mappyfile/pull/151>`_ - Updates for COMPOSITE blocks
+ `#150 <https://github.com/geographika/mappyfile/issues/150>`_ - Unknown COMPOP "SOFT-LIGHT" and error with several
   lines with COMPFILTER with validate

0.9.6 29/03/2022
++++++++++++++++

+ Schema fixes for GRID LABELFORMAT and set max versions for MAP DATAPATTERN and TEMPLATEPATTERN
+ Allow TRUE/FALSE values for OUTPUTFORMAT TRANSPARENT

0.9.5 01/03/2022
++++++++++++++++

+ `#147 <https://github.com/geographika/mappyfile/pull/147>`_ - Create list objects for containers when modifying dicts
+ `#146 <https://github.com/geographika/mappyfile/pull/146>`_ - Add COMPOSITE validation
+ `#145 <https://github.com/geographika/mappyfile/issues/145>`_ - layers.insert fails with dict error
+ `#144 <https://github.com/geographika/mappyfile/issues/144>`_ - Invalid value in COMPOSITE - 'compfilter'
+ `#140 <https://github.com/geographika/mappyfile/pull/140>`_ - New feature: group complex types at the end

0.9.4 22/02/2022
++++++++++++++++

+ `#137 <https://github.com/geographika/mappyfile/issues/137>`_ - Checking mapfile dict properties creates invalid empty dictionaries
+ `#119 <https://github.com/geographika/mappyfile/issues/119>`_ - STYLE GEOMTRANSFORM 'labelcenter'
+ `#143 <https://github.com/geographika/mappyfile/pull/143>`_ - Automate schema building
+ `#142 <https://github.com/geographika/mappyfile/pull/142>`_ - Allow newer versions of jsonschema for py3
+ `#141 <https://github.com/geographika/mappyfile/pull/141>`_ - Update and fix Continuous Integration
+ `#139 <https://github.com/geographika/mappyfile/pull/139>`_ - Feature: align values in column
+ `#138 <https://github.com/geographika/mappyfile/pull/138>`_ - Update schema based on new Mapfile validation rules

0.9.3 13/12/2021
++++++++++++++++

+ Adds a new ``mappyfile.create`` function to allow creation of Mapfile objects with default values
+ Update the Mapfile schema to include ``default`` values for keywords

0.9.2 28/08/2021
++++++++++++++++

+ Add the "idw" to ``LAYER`` ``CONNECIONTYPE``
+ Correct "minVersion" of ``LABEL`` ``EXPRESSION``
+ Add validation to ``LEGEND`` ``LABELS``
+ Add correct validation for ``MAP`` ``LEGEND`` and ``OUTPUTFORMAT``
+ Add "byte" to ``OUTPUTFORMAT`` ``IMAGEMODE``
+ Add "maxVersion" to ``WEB`` ``LOG``
+ `#120 <https://github.com/geographika/mappyfile/issues/120>`_ - Expression list element with apostrophe throws error
+ `#118 <https://github.com/geographika/mappyfile/issues/118>`_ - LABEL -> FONT and LABEL -> POSITION gives errors in validate when attributes are used

0.9.1 23/12/2020
++++++++++++++++

+ Allow any version of lark-parser > 0.9 to be used
+ Fixes for requirements for Python 2.7
+ `#115 <https://github.com/geographika/mappyfile/pull/115>`_ - Fix for issue #109 (OFFSET numeric and attribute pairs)
+ `#114 <https://github.com/geographika/mappyfile/isses/114>`_ - Style OFFSET: mixed attribute and numerical value fail to parse

0.9.0 14/07/2020
++++++++++++++++

+ Schemas updated to include ``minVersion`` and ``maxVersion`` metadata to define which Mapfile keywords are valid
  for different versions of MapServer
+ A new ``schema`` command line tool to export Mapfile schemas for different versions of MapServer
+ Allow Mapfile validation based on a specific version of MapServer
+ Add better error message when incorrect dicts are passed to printer
+ Add py38 to continuous integration testing
+ Add command line scripts to continuous integration testing
+ Fix ``CONNECTIONOPTIONS`` formatted output
+ Update to lark-parser 0.9.0
+ `#109 <https://github.com/geographika/mappyfile/pull/109>`_ - Add validation based on MapServer version
+ `#96 <https://github.com/geographika/mappyfile/issues/96>`_ - Unquoted Unicode strings cause parsing errors
+ `#102 <https://github.com/geographika/mappyfile/pull/102>`_ - Added support for accented-latin in unquoted strings (Issue #96) - thanks @erezsh
+ `#97 <https://github.com/geographika/mappyfile/issues/97>`_ - Allow for negative expressions
+ `#101 <https://github.com/geographika/mappyfile/pull/101>`_ - Fix for issue #97 (unary negation) - thanks @erezsh
+ `#85 <https://github.com/geographika/mappyfile/issues/85>`_ - Coding of NOT logical expression
+ `#100 <https://github.com/geographika/mappyfile/pull/100>`_ - Allowing non-bracketed NOT expression (Issue #85) - thanks @erezsh

0.8.4 11/01/2020
++++++++++++++++

+ Update to lark-parser 0.7.8
+ `#95 <https://github.com/geographika/mappyfile/pull/95>`_ - Allow Mapfile input from ``io.StringIO`` as well 
  as from a file - thanks @ianturton for pull request
+ `#93 <https://github.com/geographika/mappyfile/issues/93>`_ - fix to ensure Mapfiles are closed after reading
+ `#89 <https://github.com/geographika/mappyfile/issues/89>`_ - List expressions with spaces in the attributes fail to 
  parse - thanks @ianturton for fix

0.8.3 06/10/2019
++++++++++++++++

+ Update to lark-parser 0.7.7
+ Update to jsonref 0.2
+ Add automated releases to GitHub using Appveyor
+ Add automated releases to PyPI using Appveyor
+ Add missing CLASS properties to JSON schema
+ Additional tests for CaseInsensitiveOrderedDict and EXPRESSIONs
+ `#37 <https://github.com/geographika/mappyfile/issues/37>`_ - LIKE not recognised in FILTER - thanks @ianturton for fix
+ `#87 <https://github.com/geographika/mappyfile/pull/87>`_ - JSON schema add join tag- thanks @hugbe8 for fix

0.8.2 29/03/2019
++++++++++++++++

+ `#74 <https://github.com/geographika/mappyfile/issues/74>`_ - Map files containing Unicode can fail in mappyfile.load with 
  python2.7 thanks @ianturton
+ `#73 <https://github.com/geographika/mappyfile/issues/73>`_ - Deepcopy not working (Python3 >=3.5) - thanks @guardeivid
+ Add support for CLUSTER keyword along with schema changes and tests

0.8.1 27/02/2019
++++++++++++++++

+ Fix comments on root objects in a MapFile
+ Fix issues with duplicated METADATA keys and comments
+ Fix ReadTheDocs build
+ Add more sample MapFiles for testing to the project

0.8.0 24/02/2019
++++++++++++++++

+ Update code to work with Lark 0.6.6 (see #71)
+ New end_comment option for pprint - Add a comment with the block type at each closing END statement e.g. END # MAP 
  (see request `#69 <https://github.com/geographika/mappyfile/issues/69>`_)
+ Add ``**kwargs`` to main API to allow greater flexibility with plugins
+ Fix DeprecationWarnings relating to Python 3.7.2 (thanks @tigerfoot for the report)
+ Tested use with new jsonschema 3.0.0 release

0.7.6 (13/10/2018)
++++++++++++++++++

+ Deprecated ``write`` function removed from the API and codebase
+ Update OFFSET validation to allow attribute bindings - see https://github.com/mapserver/docs/pull/256
+ `#68 <https://github.com/geographika/mappyfile/issues/68>`_ - Support pickling of DefaultOrderedDict in Python3
+ `#67 <https://github.com/geographika/mappyfile/issues/67>`_ - Fix deprecation warnings for grammar regular expressions in Python 3.6
+ `#65 <https://github.com/geographika/mappyfile/issues/65>`_ - Handle hexadecimal color translucence

0.7.5 (14/09/2018)
++++++++++++++++++

+ Save tokens for value lists
+ Update README and fix example code

0.7.4 (07/09/2018)
++++++++++++++++++

+ Support for modulus operator
+ Allow custom transformers to be used with kwargs

0.7.3 (23/08/2018)
++++++++++++++++++

+ Two new CLI programs - ``format`` and ``validate``
+ Update of Lark parser to 0.6.4 (fixes some validation line number issues)
+ Improvements to validation log messages
+ Normalise include paths

0.7.2 (24/07/2018)
++++++++++++++++++

+ Update of Lark parser to 0.6.2 and associated changes - thanks @erezsh
+ ``mappyfile.findall`` returns a list rather than a generator
+ ``SYMBOLSET`` files now supported (both parsing and transforming)
+ `#63 <https://github.com/geographika/mappyfile/issues/63>`_ - Set the PROJECTION value correctly for single strings
+ `#61 <https://github.com/geographika/mappyfile/issues/61>`_ - Remove quotes in mappyfile.findall()

0.7.1 (10/07/2018)
++++++++++++++++++

+ **Breaking Change** ``utils.dictfind`` renamed ``utils.findkey``
+ new dictionary update function - allowing for easier creation of Mapfiles using YAML
+ allow any custom hidden metadata tags of the form ``__property__`` to be used in dicts for custom processing
+ Schema validation updates including RANGEITEM and CLUSTER
+ Appveyor builds added
+ `#56 <https://github.com/geographika/mappyfile/issues/56>`_ Can't parse expressions with a : in them
+ `#54 <https://github.com/geographika/mappyfile/issues/54>`_ fix windows cwd name issue in includes - thanks @ianturton

0.7.0 (04/04/2018)
++++++++++++++++++

+ Finalise validation API
+ Finalised Mapfile comments API
+ New ``dictfind`` function
+ Allow non-string function parameters in expressions
+ Use of CaseInsensitiveOrderedDict throughout transformer
+ UTF comments
+ JSONSchema updates and fixes

0.6.2 (24/02/2018)
++++++++++++++++++

+ **Breaking Change** - the ``mappyfile.load`` method now accepts a file-like object rather than a 
  filename to match the usage in other Python libraries. A new ``mappyfile.open`` method allows opening 
  directly with a filename. 
+ New preserve comments feature - *experimental*
+ Add basic plugin system
+ Updates to schema docs (fixes for POSITION, AUTO, and added new default values)
+ Fix issue with comments on INCLUDE lines
+ `#50 <https://github.com/geographika/mappyfile/issues/50>`_ Allow END keyword for GEOTRANSFORM parameter
+ `#49 <https://github.com/geographika/mappyfile/issues/45>`_ Allow non-ASCII characters in parser
+ `#47 <https://github.com/geographika/mappyfile/issues/47>`_ Add in missing expression operators - 
  divide, multiply, and power. 

0.6.1 (06/02/2018)
++++++++++++++++++

+ Fixes to setup.py

0.6.0 (17/01/2018)
++++++++++++++++++

+ Extensive refactoring of grammar and transformer
+ Removal of Earley grammar
+ Whitespace ignored when parsing
+ JSON schema fixes
+ `#45 <https://github.com/geographika/mappyfile/issues/45>`_ Set fixed dependency ranges
+ *Experimental* - inclusion of token positions
+ *Experimental* - inclusion of validation comments

0.5.1 (05/01/2018)
++++++++++++++++++

+ `#45 <https://github.com/geographika/mappyfile/issues/45>`_ Remove unnecessary parser keyword

0.5.0 (01/11/2017)
++++++++++++++++++

+ Add in jsonschema and validation class
+ `#44 <https://github.com/geographika/mappyfile/issues/44>`_ Includes should be relative to Mapfile

0.4.3 (28/08/2017)
++++++++++++++++++

+ `#36 <https://github.com/geographika/mappyfile/pull/36>`_ Create a unique logger for mappyfile logger
+ `#35 <https://github.com/geographika/mappyfile/pull/35>`_ Add support for missing arithmetic expressions and run flake8 within tox
  - thanks @loicgrasser
+ `#33 <https://github.com/geographika/mappyfile/pull/33>`_ Fix max recursion limit count - thanks @loicgrasser


0.4.0 (18/08/2017)
++++++++++++++++++

+ Add a LALR grammar and parser, now a 8k line Mapfile is now parsed 12x faster
+ Add a experimental validator module using jsonschema
+ `#30 <https://github.com/geographika/mappyfile/pull/30>`_ Flake8 support - thanks @loicgrasser
+ `#28 <https://github.com/geographika/mappyfile/pull/28>`_ Add support for relative path for nested include - thanks @loicgrasser
+ `#25 <https://github.com/geographika/mappyfile/issues/25>`_ Expression grammar not allowing ``!``
 
0.3.2
+++++

+ Revert back to a single grammar, but add linebreaks before all ``END`` keywords to keep acceptable performance

0.3.1
+++++

+ Add in alternative grammar that allows for no line breaks between composites, and fall back to this
  if parsing fails (otherwise most use cases suffer a 3x performance hit)

0.3.0
+++++

+ Allow multiple composites to be parsed directly (e.g. ``CLASS..END CLASS..END``)
+ Allow direct parsing of the ``METADATA`` and ``VALIDATION`` blocks
+ UTF-8 checks when opening a Mapfile
+ `#23 <https://github.com/geographika/mappyfile/issues/23>`_ Alternative NE and EQ comparisons not defined
+ `#22 <https://github.com/geographika/mappyfile/issues/22>`_ Handle AUTO Projection setting
+ `#21 <https://github.com/geographika/mappyfile/issues/21>`_ INCLUDES throw error when no cwd set
+ `#20 <https://github.com/geographika/mappyfile/issues/20>`_ Only the first FORMATOPTION is kept after transform
+ `#19 <https://github.com/geographika/mappyfile/issues/19>`_ IMAGEMODE FEATURE throws parsing error
+ `#18 <https://github.com/geographika/mappyfile/issues/18>`_ CONFIG keyword not capitalised

Older Releases
++++++++++++++

+ 0.2.2 - various fixes to grammar, and allow for alternate comparison operators
+ 0.2.1 - new ``findall`` function, see https://github.com/geographika/mappyfile/pull/12 - thanks @Jenselme
+ 0.2.0 - switch to Lark parser
+ 0.1.0 - initial release