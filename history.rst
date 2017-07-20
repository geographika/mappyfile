Releases
--------

0.3.1
+++++

+ Add in alternative grammar that allows for no line breaks between composites, and fall back to this
  if parsing fails (otherwise most use cases suffer a 3x performance hit)

0.3.0
+++++

+ Allow multiple composites to be parsed directly (e.g. ``CLASS..END CLASS..END``)
+ Allow direct parsing of the ``METADATA`` and ``VALIDATION`` blocks
+ UTF-8 checks when opening a Mapfile

Resolved Issues
***************

* `#23 <https://github.com/geographika/mappyfile/issues/23>`_ Alternative NE and EQ comparisons not defined`
* `#22 <https://github.com/geographika/mappyfile/issues/22>`_ Handle AUTO Projection setting`
* `#21 <https://github.com/geographika/mappyfile/issues/21>`_ INCLUDES throw error when no cwd set`
* `#20 <https://github.com/geographika/mappyfile/issues/20>`_ Only the first FORMATOPTION is kept after transform`
* `#19 <https://github.com/geographika/mappyfile/issues/19>`_ IMAGEMODE FEATURE throws parsing error`
* `#18 <https://github.com/geographika/mappyfile/issues/18>`_ CONFIG keyword not capitalised`

Older Releases
++++++++++++++

+ 0.2.2 - various fixes to grammar, and allow for alternate comparison operators
+ 0.2.1 - new ``findall`` function, see https://github.com/geographika/mappyfile/pull/12
+ 0.2.0 - switch to Lark parser
+ 0.1.0 - initial release