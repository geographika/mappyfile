mappyfile
=========

| |Version| |Docs| |Build Status| |Coveralls| |Appveyor Build Status| 

A pure Python MapFile parser for working with MapServer, built using `Lark <https://github.com/erezsh/lark>`_

An online formatter demonstrating the libraries capabilities can be found at: http://mappyfile.geographika.net/

A presentation on mappyfile was given at `FOSS4G Europe 2017 <https://europe.foss4g.org/2017/Home>`_ - slides are available 
`for download here </docs/_static/foss4ge2017_mappyfile_sgirvin.pdf>`_.

.. image:: https://raw.githubusercontent.com/geographika/mappyfile/master/docs/images/class_parsed_small.png

Requirements
------------

* Python 2.7 or Python 3.x

Installation
------------

mappyfile is available on PyPI (Python Package Index), and can be installed using pip:

.. code-block:: console

    pip install mappyfile

This will also install its required dependences Lark (lark-parser), and jsonschema. 

Documentation
-------------

Documentation at http://mappyfile.readthedocs.io/en/latest/

Usage
-----

.. code-block:: python

    import mappyfile

    mapfile = mappyfile.load("./docs/examples/raster.map")
    
    # update the map name
    mapfile["name"] = "MyNewMap"

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

    new_layer = mappyfile.loads(new_layer_string)
    layers.insert(0, new_layer) # can insert the new layer at any index

    print(mappyfile.dumps(mapfile))

Authors
-------

* Seth Girvin `@geographika <https://github.com/geographika>`_
* Erez Shinan `@erezsh <https://github.com/erezsh>`_

Contributors
------------

* Julien Enselme `@jenselme <https://github.com/jenselme>`_
* Loïc Gasser `@loicgasser <https://github.com/loicgasser>`_
* Ian Turton `@ianturton <https://github.com/ianturton>`_

..
    .. include:: docs/HISTORY.rst

.. |Version| image:: https://img.shields.io/pypi/v/mappyfile.svg
   :target: https://pypi.python.org/pypi/mappyfile

.. |Docs| image:: https://img.shields.io/badge/docs-latest-brightgreen.svg?style=flat
   :target: http://mappyfile.readthedocs.io/en/latest/

.. |Build Status| image:: https://travis-ci.org/geographika/mappyfile.svg?branch=master
   :target: https://travis-ci.org/geographika/mappyfile

.. |Appveyor Build Status| image:: https://ci.appveyor.com/api/projects/status/mk33l07478gfytwh?svg=true
   :target: https://ci.appveyor.com/project/SethG/mappyfile

.. |Coveralls| image:: https://coveralls.io/repos/github/geographika/mappyfile/badge.svg?branch=master
    :target: https://coveralls.io/github/geographika/mappyfile?branch=master