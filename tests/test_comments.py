import collections
import logging
import pytest
from mappyfile.pprint import PrettyPrinter


def test_comment():
    d = collections.OrderedDict()
    d["name"] = "Test"
    d["__type__"] = "layer"
    d["__comments__"] = {"name": "Test comment"}

    pp = PrettyPrinter(indent=0, quote="'", newlinechar="\n")
    s = pp.pprint(d)
    exp = """LAYER
NAME 'Test' # Test comment
END"""
    assert(s == exp)


def test_double_comment():
    d = collections.OrderedDict()
    d["name"] = "Test"
    d["__type__"] = "layer"
    d["__comments__"] = {"name": "Name comment", "type": "Type comment"}

    d["type"] = "polygon"

    pp = PrettyPrinter(indent=0, quote="'", newlinechar="\n")
    s = pp.pprint(d)
    exp = """LAYER
NAME 'Test' # Name comment
TYPE POLYGON # Type comment
END"""
    assert(s == exp)


def test_header_comment():
    """
    __type__ is used as the key for any object-level comments
    """
    d = collections.OrderedDict()
    d["name"] = "Test"
    d["__type__"] = "layer"
    d["__comments__"] = {"__type__": "Layer comment"}

    pp = PrettyPrinter(indent=0, quote="'", newlinechar="\n")
    s = pp.pprint(d)
    exp = """# Layer comment
LAYER
NAME 'Test'
END"""
    assert(s == exp)


def test_header_list_comments():
    """
    __type__ is used as the key for any object-level comments
    """
    d = collections.OrderedDict()
    d["name"] = "Test"
    d["__type__"] = "layer"
    d["__comments__"] = {"__type__": ["Layer comment 1", "Layer comment 2"]}

    pp = PrettyPrinter(indent=0, quote="'", newlinechar="\n")
    s = pp.pprint(d)
    exp = """# Layer comment 1
# Layer comment 2
LAYER
NAME 'Test'
END"""
    assert(s == exp)


def run_tests():
    pytest.main(["tests/test_comments.py"])


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('mappyfile').setLevel(logging.INFO)
    run_tests()
    print("Done!")
