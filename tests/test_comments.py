import collections
import json
import logging
import pytest
import mappyfile
from mappyfile.pprint import PrettyPrinter
from mappyfile.transformer import MapfileToDict
from mappyfile.parser import Parser


def test_comment():
    d = collections.OrderedDict()
    d["name"] = "Test"
    d["__type__"] = "layer"
    d["__comments__"] = {"name": "# Test comment"}
    print(json.dumps(d, indent=4))
    pp = PrettyPrinter(indent=0, quote="'", newlinechar="\n")
    s = pp.pprint(d)
    exp = """LAYER
NAME 'Test' # Test comment
END"""
    print(s)
    assert(s == exp)


def test_double_comment():
    d = collections.OrderedDict()
    d["name"] = "Test"
    d["__type__"] = "layer"
    d["__comments__"] = {"name": "# Name comment", "type": "# Type comment"}

    d["type"] = "polygon"

    print(json.dumps(d, indent=4))

    pp = PrettyPrinter(indent=0, quote="'", newlinechar="\n")
    s = pp.pprint(d)
    exp = """LAYER
NAME 'Test' # Name comment
TYPE POLYGON # Type comment
END"""
    print(s)
    assert(s == exp)


def test_header_comment():
    """
    __type__ is used as the key for any object-level comments
    """
    d = collections.OrderedDict()
    d["name"] = "Test"
    d["__type__"] = "layer"
    d["__comments__"] = {"__type__": "# Layer comment"}

    print(json.dumps(d, indent=4))

    pp = PrettyPrinter(indent=0, quote="'", newlinechar="\n")
    s = pp.pprint(d)
    print(s)
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
    d["__comments__"] = {"__type__": ["# Layer comment 1", "# Layer comment 2"]}
    print(json.dumps(d, indent=4))
    pp = PrettyPrinter(indent=0, quote="'", newlinechar="\n")
    s = pp.pprint(d)
    exp = """# Layer comment 1
# Layer comment 2
LAYER
NAME 'Test'
END"""
    assert(s == exp)


def test_example_comment_dict():

    d = {
    "__type__": "map",
    "__comments__": {
        "__type__": ["# Map comment 1",
        "# Map comment 2"]
        },
    "name": "Test",
    "layers": [{
            "__type__": "layer",
            "__comments__": {
                "__type__": "# Layer comment",
                "type": ["# This is a polygon!", "# Another comment"]
            },
            "type": "POLYGON"
        }]
}
    pp = PrettyPrinter(indent=4, quote="'", newlinechar="\n")
    s = pp.pprint(d)
    print(s)


def test_header_comment2():
    s = """
    # Map comment 1
    # Map comment 2
    MAP
        # comment 2
        NAME "Test" # name comment
        # post name comment
    END"""

    p = Parser(include_comments=True)
    ast = p.parse(s)
    print(p._comments)
    print(ast.pretty())
    m = MapfileToDict(include_position=True, include_comments=True)
    d = m.transform(ast)
    print(json.dumps(d, indent=4))

    pp = PrettyPrinter(indent=4, quote="'", newlinechar="\n")
    s = pp.pprint(d)
    print(s)


def test_comment_parsing():

    s = """
    # Map comment 1
    # Map comment 2
    MAP
    NAME 'Test' # Name comment
    # Layer comment
    LAYER
    TYPE POLYGON # This is a polygon!
    END
    END"""

    p = Parser(include_comments=True)
    m = MapfileToDict(include_position=False, include_comments=True)
    ast = p.parse(s)
    print(p._comments)
    print(ast.pretty())
    d = m.transform(ast)      # transform the rest
    print(json.dumps(d, indent=4))

    pp = PrettyPrinter(indent=0, quote="'", newlinechar="\n")
    s = pp.pprint(d)
    print(s)


def test_metadata_comment():

    txt = """MAP
    # metadata comment
    # on two lines
    METADATA
        # another comment
        'wms_title' 'Test simple wms' # prop comment
    END
    END"""
    d = mappyfile.loads(txt, include_comments=True, include_position=False)
    # print(json.dumps(d, indent=4))
    s = mappyfile.dumps(d, indent=0, quote="'", newlinechar="\n")
    # print(s)
    expected = """MAP
# metadata comment
# on two lines
METADATA
'wms_title' 'Test simple wms' # prop comment # another comment
END
END"""
    assert s == expected


def run_tests():
    pytest.main(["-s", "tests/test_comments.py"])


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('mappyfile').setLevel(logging.DEBUG)
    # test_metadata_comment()
    run_tests()
    print("Done!")
