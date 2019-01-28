import logging
import json
import pytest
from mappyfile.parser import Parser
from mappyfile.pprint import PrettyPrinter
from mappyfile.transformer import MapfileToDict
from mappyfile.validator import Validator


def output(s, include_position=True, schema_name="map"):
    """
    Parse, transform, validate, and pretty print
    the result
    """
    p = Parser()
    m = MapfileToDict(include_position=include_position)
    ast = p.parse(s)
    logging.debug(ast.pretty())
    d = m.transform(ast)
    logging.debug(json.dumps(d, indent=4))
    v = Validator()
    errors = v.validate(d, schema_name=schema_name)
    logging.error(errors)
    pp = PrettyPrinter(indent=0, newlinechar=" ", quote="'")
    s = pp.pprint(d)
    logging.debug(s)
    assert(len(errors) == 0)
    return s


def test_symbolset_include():
    s = u"""
    MAP
        NAME "Test"
        SYMBOLSET "./symbolset.txt"
        SIZE 200 200
    END
    """

    print(output(s, schema_name="map"))
    exp = "MAP NAME 'Test' SYMBOLSET './symbolset.txt' SIZE 200 200 END"
    assert(output(s, schema_name="map") == exp)


def test_symbolset_file():
    s = u"""
    SYMBOLSET
        SYMBOL
            NAME 'default-circle'
            TYPE ELLIPSE
            FILLED TRUE
            POINTS
                1 1
            END
        END
        SYMBOL
            NAME 'other-circle'
            TYPE ELLIPSE
            FILLED FALSE
            POINTS
                1 1
            END
        END
    END
    """

    print(output(s, schema_name="symbolset"))
    exp = "SYMBOLSET SYMBOL NAME 'default-circle' TYPE ELLIPSE FILLED TRUE POINTS 1 1 END " \
          "END SYMBOL NAME 'other-circle' TYPE ELLIPSE FILLED FALSE POINTS 1 1 END END END"
    assert(output(s, schema_name="symbolset") == exp)


def run_tests():
    pytest.main(["tests/test_symbolset.py"])


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    run_tests()
    print("Done!")
