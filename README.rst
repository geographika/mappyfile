mappyfile
=========

| |Version| |Docs| |Build Status| |Coveralls| |Appveyor Build Status| |Downloads|

A pure Python parser for working with `MapServer <https://mapserver.org>`_ MapFiles, built using `Lark <https://github.com/lark-parser/lark>`__.
mappyfile is an official `OSGeo Community Project <https://www.osgeo.org/projects/mappyfile/>`_.

.. image:: https://raw.githubusercontent.com/geographika/mappyfile/master/docs/images/OSGeo_community_small.png
    :align: right

mappyfile is used for formatting and validation in https://app.mapserverstudio.net/, and can be tested for free on any
of your Mapfiles. If you find mappyfile useful please consider signing up for a professional account at 
https://mapserverstudio.net/. This will help to fund maintenance and further development of both mappyfile and MapServer.

Requirements
------------

* Python 3.8 or higher

Installation
------------

mappyfile is available on `PyPI <https://pypi.org/project/mappyfile/>`_ (the Python Package Index), and can be installed using pip:

.. code-block:: console

    pip install mappyfile

This will also install its required dependencies - `Lark <https://github.com/lark-parser/lark>`__, and 
`jsonschema <https://github.com/python-jsonschema/jsonschema>`_. 

To install the optional `lark-cython <https://github.com/lark-parser/lark_cython>`_ library
for better performance on CPython you can run the following command:

.. code-block:: console

    pip install mappyfile[lark_cython]

mappyfile is also available on `conda <https://anaconda.org/conda-forge/mappyfile>`_. Install as
follows:

.. code-block:: console

    conda install -c conda-forge mappyfile

Documentation
-------------

Full documentation is available at http://mappyfile.readthedocs.io/en/latest/

.. image:: https://raw.githubusercontent.com/geographika/mappyfile/master/docs/images/class_parsed_small.png

Usage
-----

From within Python scripts:

.. code-block:: python

    import mappyfile

    mapfile = mappyfile.open("./docs/examples/raster.map")
    
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

    layers = mapfile["layers"]

    new_layer = mappyfile.loads(new_layer_string)

    layers.insert(0, new_layer) # insert the new layer at any index in the Mapfile

    for l in layers:
        print("{} {}".format(l["name"], l["type"]))

    print(mappyfile.dumps(mapfile, indent=1, spacer="\t"))

Three command line tools are available - ``format``, ``validate``, and ``schema``:

.. code-block:: bat

    mappyfile format raster.map formatted_raster.map
    mappyfile validate D:\ms-ogc-workshop\ms4w\apps\ms-ogc-workshop\**\*.map
    mappyfile schema mapfile-schema-8-0.json --version=8.0

Authors
-------

* Seth Girvin `@geographika <https://github.com/geographika>`_
* Erez Shinan `@erezsh <https://github.com/erezsh>`_

Contributors
------------

* Julien Enselme `@jenselme <https://github.com/jenselme>`_
* Loïc Gasser `@loicgasser <https://github.com/loicgasser>`_
* Ian Turton `@ianturton <https://github.com/ianturton>`_
* `@thorag76 <https://github.com/thorag76>`_
* `@DonQueso89 <https://github.com/DonQueso89>`_
* TC Haddad `@tchaddad <https://github.com/tchaddad>`_ (Conda support)

.. |Version| image:: https://img.shields.io/pypi/v/mappyfile.svg
   :target: https://pypi.python.org/pypi/mappyfile

.. |Docs| image:: https://img.shields.io/badge/docs-latest-brightgreen.svg?style=flat
   :target: http://mappyfile.readthedocs.io/en/latest/

.. |Build Status| image:: https://github.com/geographika/mappyfile/actions/workflows/main.yml/badge.svg
   :target: https://github.com/geographika/mappyfile/actions/workflows/main.yml

.. |Appveyor Build Status| image:: https://ci.appveyor.com/api/projects/status/mk33l07478gfytwh?svg=true
   :target: https://ci.appveyor.com/project/SethG/mappyfile

.. |Coveralls| image:: https://coveralls.io/repos/github/geographika/mappyfile/badge.svg?branch=master
    :target: https://coveralls.io/github/geographika/mappyfile?branch=master

.. |Downloads| image:: https://static.pepy.tech/badge/mappyfile
    :target: https://www.pepy.tech/projects/mappyfile
    