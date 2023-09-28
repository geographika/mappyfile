Development Notes
=================

The development notes below assume a PowerShell prompt is being used on a Windows machine.

Run the following before any of the following tasks (once the virtual environment itself has been built):

.. code-block:: ps1

    # update the following to your local paths
    $VIRTUALENV="C:\VirtualEnvs\mappyfile3"
    $MAPPYFILE_PATH="D:\GitHub\mappyfile"

    .$VIRTUALENV\Scripts\activate.ps1
    cd $MAPPYFILE_PATH

Building the Dev Virtual Environment
------------------------------------

Run from the root of the mappyfile project folder:

.. code-block:: ps1

    $VIRTUALENV="C:\VirtualEnvs\mappyfile"
    $MAPPYFILE_PATH="D:\GitHub\mappyfile"

    cd "C:\Python310\Scripts"
    .\pip install virtualenv
    .\virtualenv $VIRTUALENV
    .$VIRTUALENV\Scripts\activate.ps1
    cd $MAPPYFILE_PATH
    pip install -e .
    pip install -r requirements-dev.txt
    # optionally install lark_cython
    pip install -e .[lark_cython]

Testing Locally
---------------

Ensure the development code has been deployed to a virtual environment as in the
step above.

Then run from the root of the mappyfile project folder:

.. code-block:: ps1

    pytest

To see a list of which tests will run, without actually running them:

.. code-block:: ps1

    pytest --collect-only

To run a single test file:

.. code-block:: ps1

    pytest tests/test_snippets.py

To also include doctests:

.. code-block:: ps1

    pytest --doctest-modules --ignore=./docs/examples/pretty_printing.py

Linting
-------

.. code-block:: ps1

    flake8 .

Or to export to file:

.. code-block:: ps1

    flake8 . > D:\Temp\lint.txt

Prospector
----------

.. code-block:: ps1

    pip install prospector
    prospector
    # or just the main source code folder
    prospector ./mappyfile

Mypy
----

To run static type checking:

.. code-block:: ps1

    mypy mappyfile tests


Documentation
-------------

To build the Sphinx documentation:

.. code-block:: ps1

    sphinx-build -b html "$MAPPYFILE_PATH\docs" "$MAPPYFILE_PATH\_build"
    # to force a rebuild of all files
    sphinx-build -a -E -b html "$MAPPYFILE_PATH\docs" "$MAPPYFILE_PATH\_build"

To run in a local browser:

.. code-block:: ps1

    .$VIRTUALENV\Scripts\activate.ps1
    C:\Python310\python -m http.server --directory="$MAPPYFILE_PATH\_build" 57921

    # open browser and go to http://localhost:57921

To automatically rebuild docs using `watchdog <https://pypi.org/project/watchdog/>`_:

.. code-block:: ps1

    # run the following to automatically rebuild the project
    # python -m pip install -U "watchdog[watchmedo]"
    cd $MAPPYFILE_PATH
    watchmedo shell-command --patterns="*.rst;*.txt" --recursive --command='sphinx-build -b html "./docs" "./_build"' ./docs
