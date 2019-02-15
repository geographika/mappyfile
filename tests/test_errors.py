import logging
import json
import inspect
import pytest
from mappyfile.parser import Parser
from mappyfile.pprint import PrettyPrinter
from mappyfile.transformer import MapfileToDict
from lark import UnexpectedToken  # inherits from ParseError


def output(s):
    """
    Parse, transform, and pretty print
    the result
    """
    p = Parser()
    m = MapfileToDict()

    # https://stackoverflow.com/questions/900392/getting-the-caller-function-name-inside-another-function-in-python
    logging.info(inspect.stack()[1][3])

    ast = p.parse(s)
    logging.debug(ast)
    d = m.transform(ast)
    logging.debug(json.dumps(d, indent=4))
    pp = PrettyPrinter(indent=0, newlinechar=" ", quote="'")
    s = pp.pprint(d)
    logging.debug(s)
    return s


def test_invalid_keyword():
    """
    Check an invalid keyword throws a schema validation
    error
    """
    s = """
    MAP
        INVALID "setting"
    END
    """
    output(s)


def test_extra_end():
    """
    Check an extra end keyword throws an error
    """
    s = """MAP
NAME "test"
END
END"""

    p = Parser()
    try:
        p.parse(s)
    except UnexpectedToken as ex:
        print(ex.__dict__)
        assert(ex.line == 4)
        assert(ex.column == 1)
        assert(str(ex.token) == 'END')


def test_missing_end():
    """
    Check an invalid keyword throws a schema validation
    error
    """
    s = """MAP
LAYER
NAME "Test"
LAYER
NAME "Test2"
END
END"""

    p = Parser()
    try:
        p.parse(s)
    except UnexpectedToken as ex:
        assert(ex.line == 7)
        assert(ex.column == 1)
        assert(ex.token.type == "$END")


@pytest.mark.xfail
def test_style_pattern_fail():
    """
    Test pattern with odd number of values
    This should fail with the following error message
    UnexpectedToken: Unexpected token Token(_END, 'END') at line 3, column 27.
    """
    s = """
    STYLE
        PATTERN 6 4 2 4 6 END
    END
    """
    exp = "STYLE PATTERN 6 4 2 4 6 END END"
    assert(output(s, schema_name="style") == exp)


def run_tests():
    r"""
    Need to comment out the following line in C:\VirtualEnvs\mappyfile\Lib\site-packages\pep8.py
    #stdin_get_value = sys.stdin.read
    Or get AttributeError: '_ReplInput' object has no attribute 'read'
    """
    # pytest.main(["tests/test_snippets.py::test_style_pattern"])
    pytest.main(["tests/test_errors.py"])


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run_tests()
    print("Done!")
