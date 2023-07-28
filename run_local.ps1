C:\VirtualEnvs\mappyfile3\Scripts\activate.ps1
cd D:\GitHub\mappyfile

black .
flake8 .

# mypy --install-types
# to find functions missing types
# mypy --check-untyped-defs mappyfile
mypy mappyfile tests

# pytest
pytest --doctest-modules --ignore=./docs/examples/pretty_printing.py