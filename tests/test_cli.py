import logging
import os
import tempfile
from mappyfile import cli
import pytest


def test_get_mapfiles():

    tf = tempfile.NamedTemporaryFile(suffix=".map")
    print(tf.name)

    mapfiles = [tf.name]
    found_mapfiles = cli.get_mapfiles(mapfiles)
    print(found_mapfiles)
    os.remove(tf.name)


def run_tests():
    pytest.main(["tests/test_cli.py"])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # run_tests()
    test_get_mapfiles()
    print("Done!")
