Releases
--------

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

+ `#45 <https://github.com/geographika/mappyfile/issues/45>`_ Remove unnecessary parser keyword`

0.5.0 (01/11/2017)
++++++++++++++++++

+ Add in jsonschema and validation class
+ `#44 <https://github.com/geographika/mappyfile/issues/44>`_ Includes should be relative to Mapfile`

0.4.3 (28/08/2017)
++++++++++++++++++

+ `#36 <https://github.com/geographika/mappyfile/pull/36>`_ Create a unique logger for mappyfile logger` 
+ `#35 <https://github.com/geographika/mappyfile/pull/35>`_ Add support for missing arithmetic expressions and run flake8 within tox` 
  - thanks @loicgrasser
+ `#33 <https://github.com/geographika/mappyfile/pull/33>`_ Fix max recursion limit count` - thanks @loicgrasser


0.4.0 (18/08/2017)
++++++++++++++++++

+ Add a LALR grammar and parser, now a 8k line Mapfile is now parsed 12x faster
+ Add a experimental validator module using jsonschema
+ `#30 <https://github.com/geographika/mappyfile/pull/30>`_ Flake8 support` - thanks @loicgrasser
+ `#28 <https://github.com/geographika/mappyfile/pull/28>`_ Add support for relative path for nested include` - thanks @loicgrasser
+ `#25 <https://github.com/geographika/mappyfile/issues/25>`_ Expression grammar not allowing !`
 
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
+ `#23 <https://github.com/geographika/mappyfile/issues/23>`_ Alternative NE and EQ comparisons not defined`
+ `#22 <https://github.com/geographika/mappyfile/issues/22>`_ Handle AUTO Projection setting`
+ `#21 <https://github.com/geographika/mappyfile/issues/21>`_ INCLUDES throw error when no cwd set`
+ `#20 <https://github.com/geographika/mappyfile/issues/20>`_ Only the first FORMATOPTION is kept after transform`
+ `#19 <https://github.com/geographika/mappyfile/issues/19>`_ IMAGEMODE FEATURE throws parsing error`
+ `#18 <https://github.com/geographika/mappyfile/issues/18>`_ CONFIG keyword not capitalised`

Older Releases
++++++++++++++

+ 0.2.2 - various fixes to grammar, and allow for alternate comparison operators
+ 0.2.1 - new ``findall`` function, see https://github.com/geographika/mappyfile/pull/12 - thanks @Jenselme
+ 0.2.0 - switch to Lark parser
+ 0.1.0 - initial release