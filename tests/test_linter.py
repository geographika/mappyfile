import logging
import pytest
from mappyfile.validator import Validator


def validate(d):
    v = Validator()
    return v.validate(d)


def get_from_dict(d, keys):
    for k in keys:
        if isinstance(k, int):
            d = d[0]
        else:
            d = d[k]
    return d


def run_tests():
    pytest.main(["tests/test_linter.py"])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # run_tests()
    print("Done!")
