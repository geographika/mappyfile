Development Notes
=================

Run the following before any of the following tasks:

.. code-block:: bat

    set VIRTUALENV=C:\VirtualEnvs\mappyfile
    echo set VIRTUALENV=C:\VirtualEnvs\mappyfile3

    %VIRTUALENV%\Scripts\activate
    echo set MAPPYFILE_PATH=C:\Code\mappyfile
    set MAPPYFILE_PATH=D:\GitHub\mappyfile
    cd /D %MAPPYFILE_PATH%

Building the Dev Virtual Environment
------------------------------------

Run from the root of the mappyfile project folder:

.. code-block:: bat

    set MAPPYFILE_PATH=D:\GitHub\mappyfile
    set VIRTUALENV=C:\VirtualEnvs\mappyfile3
    cd /D "C:\Python310\Scripts"
    REM cd /D "C:\Python27\Scripts"
    pip install virtualenv
    virtualenv %VIRTUALENV%
    %VIRTUALENV%\Scripts\activate
    cd /D %MAPPYFILE_PATH%
    pip install -r requirements-dev.txt

Testing Locally
---------------

See also https://tox.readthedocs.io/en/latest/ (run with ``tox``).

First install the development code to a virtual environment:

.. code-block:: bat

    pip install -e .

Run from the root of the mappyfile project folder:

.. code-block:: bat

    pytest

To see which tests will run:

.. code-block:: bat

    pytest --collect-only

For a single test file:

    pytest tests/test_snippets.py

Lark Update
-----------

To update from master. https://github.com/erezsh/lark/

.. code-block:: bat

    pip install git+git://github.com/lark-parser/lark@master -U

Linting
-------

.. code-block:: bat

    flake8 --ignore=E501,E121,E122,E123,E126,E127,E128 tests --exclude=*/basemaps/*,*/ms-ogc-workshop/*
    flake8 mappyfile --max-line-length=120
    flake8 docs/scripts --max-line-length=120

Or to export to file:

.. code-block:: bat

    flake8 --ignore=E501,E121,E122,E123,E126,E127,E128 tests > D:\Temp\lint.txt
    flake8 mappyfile --max-line-length=120 > D:\Temp\lint.txt

Prospector
----------

.. code-block:: bat

    prospector > prospector.log

Documentation
-------------

To build the Sphinx documentation:

.. code-block:: bat

    cd /D %MAPPYFILE_PATH%\docs
    pip install sphinx -U
    make.bat html
    "_build/html/index.html"

