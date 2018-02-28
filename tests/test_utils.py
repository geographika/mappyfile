import logging
import tempfile
import mappyfile
import pytest


def test_open():

    fn = './tests/sample_maps/256_overlay_res.map'
    d = mappyfile.open(fn)
    assert d["name"] == "TEST"

    d = mappyfile.open(fn, expand_includes=False)
    assert d["name"] == "TEST"

    d = mappyfile.open(fn, include_position=True)
    assert d["name"] == "TEST"

    d = mappyfile.open(fn, include_comments=True)
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
    d = mappyfile.open(fn)
    assert d["name"] == "TEST"

    mappyfile.write(d, fn, indent=2, spacer="\t", quote="'", newlinechar="")
    d = mappyfile.open(fn)
    assert d["name"] == "TEST"


def test_dump():

    s = """MAP NAME "TEST" END"""
    d = mappyfile.loads(s)
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as fp:
        mappyfile.dump(d, fp)

    with open(fp.name) as fp:
        d = mappyfile.load(fp)

    assert d["name"] == "TEST"


def run_tests():
    pytest.main(["tests/test_utils.py"])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # run_tests()
    test_dump()
    print("Done!")
