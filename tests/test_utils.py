import os
import logging
import tempfile
import mappyfile
import pytest

def test_load():

    fn = './tests/sample_maps/256_overlay_res.map'
    d = mappyfile.load(fn)
    assert d["name"] == "TEST"

    d = mappyfile.load(fn, expand_includes=False)
    assert d["name"] == "TEST"

    d = mappyfile.load(fn, include_position=True)
    assert d["name"] == "TEST"

    d = mappyfile.load(fn, include_comments=True)
    assert d["name"] == "TEST"


def test_loads():

    s = """MAP NAME "TEST" END"""

    d = mappyfile.loads(s)
    assert d["name"] == "TEST"

    d = mappyfile.loads(s, expand_includes=False)
    assert d["name"] == "TEST"

    d = mappyfile.loads(s, include_position=True)
    assert d["name"] == "TEST"

    d = mappyfile.loads(s, include_comments=True)
    assert d["name"] == "TEST"


def test_write():

    s = """MAP NAME "TEST" END"""
    fn = tempfile.mktemp()
    d = mappyfile.loads(s)
    mappyfile.write(d, fn)
    m = mappyfile.load(fn)
    assert d["name"] == "TEST"

    mappyfile.write(d, fn, indent=2, spacer="\t", quote="'", newlinechar="")
    m = mappyfile.load(fn)
    assert d["name"] == "TEST"


def test_dump():

    s = """MAP NAME "TEST" END"""
    fp = tempfile.TemporaryFile()
    d = mappyfile.loads(s)
    mappyfile.dump(d, fp)

    m = mappyfile.load(fn)
    assert d["name"] == "TEST"

    mappyfile.write(d, fn, indent=2, spacer="\t", quote="'", newlinechar="")
    m = mappyfile.load(fp)
    assert d["name"] == "TEST"


def run_tests():
    pytest.main(["tests/test_utils.py"])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # run_tests()
    test_dump()
    print("Done!")
