import collections
import json
import logging
import pytest
from mappyfile.pprint import PrettyPrinter
from mappyfile.parser import Parser
from mappyfile.transformer import MapfileToDict, CommentsTransformer


def test_comment():
    d = collections.OrderedDict()
    d["name"] = "Test"
    d["__type__"] = "layer"
    d["__comments__"] = {"name": "Test comment"}
    print(json.dumps(d, indent=4))
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

    print(json.dumps(d, indent=4))

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

    print(json.dumps(d, indent=4))

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
    print(json.dumps(d, indent=4))
    pp = PrettyPrinter(indent=0, quote="'", newlinechar="\n")
    s = pp.pprint(d)
    exp = """# Layer comment 1
# Layer comment 2
LAYER
NAME 'Test'
END"""
    assert(s == exp)


def xtest_comment_parsing():

    s = """
    # Map comment 1
    # Map comment 2
    MAP
    NAME 'Test' # Name comment
    # Layer comment
    LAYER
    TYPE POLYGON # Type comment
    END
    END"""

    p = Parser()
    m = MapfileToDict(include_position=False)
    m2 = CommentsTransformer(m)

    ast = p.parse(s)
    print(ast.pretty())

    ast = m2.transform(ast)   # transform only attr, composite and their descendants
    # print(ast.pretty())
    d = m.transform(ast)      # transform the rest

    print(json.dumps(d, indent=4))

    pp = PrettyPrinter(indent=0, quote="'", newlinechar="\n")
    s = pp.pprint(d)
    print(s)


def run_tests():
    pytest.main(["-s", "tests/test_comments.py"])


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('mappyfile').setLevel(logging.INFO)
    test_comment_parsing()
    # run_tests()
    print("Done!")
