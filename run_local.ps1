C:\VirtualEnvs\mappyfile3\Scripts\activate.ps1
cd D:\GitHub\mappyfile

black .
flake8 .

# mypy --install-types
# to check within functions missing types
# mypy mappyfile tests --check-untyped-defs
mypy mappyfile tests

# pytest
pytest --doctest-modules --ignore=./docs/examples/pretty_printing.py