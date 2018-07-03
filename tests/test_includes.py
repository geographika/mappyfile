import json
import logging
import pytest
import mappyfile
from mappyfile.parser import Parser
from mappyfile.transformer import MapfileToDict
from mappyfile.pprint import PrettyPrinter


def test_includes():
    p = Parser()

    ast = p.parse_file('./tests/samples/include1.map')
    m = MapfileToDict()

    d = (m.transform(ast))  # works
    print(mappyfile.dumps(d))
    assert d["name"] == "include_test"


def test_include_from_string():
    """
    Check that a file is correctly included when parsing text
    and that the current working directory is used as the root path
    for includes - see https://github.com/geographika/mappyfile/issues/55
    """
    s = """
    MAP
        INCLUDE "tests/samples/include3.map"
    END
    """

    d = mappyfile.loads(s, expand_includes=True)
    pp = PrettyPrinter(indent=0, newlinechar=" ", quote="'")
    output = pp.pprint(d)
    expected = "MAP NAME 'test' END"
    assert(output == expected)


def test_includes_nested_path():
    p = Parser()

    ast = p.parse_file('./tests/samples/include1_nested_path.map')
    m = MapfileToDict()

    d = (m.transform(ast))  # works
    print(mappyfile.dumps(d))


def test_includes_relative_path():
    """
    File location can be given as a full path to the file, or (in MapServer >= 4.10.1) as a
    path relative to the mapfile.
    http://mapserver.org/mapfile/include.html
    """
    p = Parser()

    ast = p.parse_file('./tests/samples/include4.map')
    m = MapfileToDict()

    d = (m.transform(ast))  # works
    print(mappyfile.dumps(d))


def test_includes_max_recursion():
    p = Parser()

    with pytest.raises(Exception) as excinfo:
        p.parse_file('./tests/samples/include1_recursive.map')

    assert('Maximum nested include exceeded' in str(excinfo.value))


def test_includes_no_expand():
    """
    https://github.com/geographika/mappyfile/issues/39
    """
    s = """
    MAP
        INCLUDE "includes/mymapfile.map"
    END
    """

    d = mappyfile.loads(s, expand_includes=False)
    pp = PrettyPrinter(indent=0, newlinechar=" ", quote="'")
    output = pp.pprint(d)

    expected = "MAP INCLUDE 'includes/mymapfile.map' END"
    assert(output == expected)


def test_two_includes():
    s = """
    MAP
        INCLUDE "include1.txt"
        INCLUDE "include2.txt"
    END
    """

    d = mappyfile.loads(s, expand_includes=False)
    logging.debug(json.dumps(d, indent=4))
    pp = PrettyPrinter(indent=0, newlinechar=" ", quote="'")
    output = pp.pprint(d)
    print(output)
    expected = "MAP INCLUDE 'include1.txt' INCLUDE 'include2.txt' END"
    assert(output == expected)


def test_include_from_filehandle():

    fn = './tests/samples/include1.map'

    with open(fn) as f:
        d = mappyfile.load(f)
        assert d["name"] == "include_test"
        print(mappyfile.dumps(d))


def run_tests():
    pytest.main(["tests/test_includes.py"])


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('mappyfile').setLevel(logging.INFO)
    # run_tests()
    test_include_from_filehandle()
    print("Done!")
