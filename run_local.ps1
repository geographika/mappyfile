# C:\Python310\python -m venv C:\VirtualEnvs\mappyfile3
C:\VirtualEnvs\mappyfile313\Scripts\activate.ps1
cd D:\GitHub\mappyfile

# the following installs mappyfile with the optional lark_cython extension
# pip install .[lark_cython]
# pip install -r requirements-dev.txt

black .
flake8 .

# mypy --install-types
# to check within functions missing types
# mypy mappyfile tests --check-untyped-defs
mypy mappyfile tests

pytest --doctest-modules
# pytest ./tests