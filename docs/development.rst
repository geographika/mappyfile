Development Tasks
=================

Building the Dev Virtual Environment
------------------------------------

Run from the root of the mappyfile project folder:

.. code-block:: bat

    set PYTHON=C:\Python27
    set VIRTUALENV=C:\VirtualEnvs\mappyfile
    %PYTHON%\Scripts\virtualenv %VIRTUALENV%
    %VIRTUALENV%\Scripts\activate
    pip install -r requirements-dev.txt

Run Tests
---------

Run from the root of the mappyfile project folder:

.. code-block:: bat

    set VIRTUALENV=C:\VirtualEnvs\mappyfile
    %VIRTUALENV%\Scripts\activate
    pytest

For a single test file:

    pytest tests/test_snippets.py