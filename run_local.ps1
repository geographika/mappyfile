C:\VirtualEnvs\mappyfile3\Scripts\activate.ps1
cd D:\GitHub\mappyfile

black .
flake8 .

# mypy --install-types
mypy mappyfile tests

# pytest
pytest --doctest-modules