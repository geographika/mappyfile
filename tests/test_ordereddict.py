import logging
import json
import inspect
import pytest
from mappyfile.parser import Parser
from mappyfile.pprint import PrettyPrinter
from mappyfile.transformer import MapfileToDict
from mappyfile.ordereddict import DefaultOrderedDict, CaseInsensitiveOrderedDict


def get_dict(s):
    """
    Parse, transform, and pretty print
    the result
    """
    p = Parser()
    m = MapfileToDict()
    logging.info(inspect.stack()[1][3])

    ast = p.parse(s)
    logging.debug(ast.pretty())
    d = m.transform(ast)
    logging.debug(json.dumps(d, indent=4))

    return d


def output(d):

    pp = PrettyPrinter(indent=0, newlinechar=" ", quote="'")
    s = pp.pprint(d)
    logging.debug(s)


def test_dict():

    d = DefaultOrderedDict()
    d["key"] = ["value"]

    print(d["key"])


def test_config_directive():

    s = """
    MAP
        NAME 'ConfigMap'
        CONFIG MS_ERRORFILE 'stderr'
        CONFIG 'PROJ_DEBUG' 'OFF'
        CONFIG 'ON_MISSING_DATA' 'IGNORE'
    END
    """

    d = get_dict(s)

    d["name"] = "NewName"

    print(d["name"])
    assert(d["name"] == "NewName")  # "'ConfigMap'")

    print(d["CONFIG"])  # even though this key is now lower-case it will correctly return (as DefaultOrderedDict calls key.lower())
    assert(d["config"]["PROJ_DEBUg"] == "OFF")
    output(d)


def test_debug():

    s = """
    MAP
        DEBUG ON
        DEFRESOLUTION 12
    END
    """

    d = get_dict(s)

    d["name"] = "NewName"
    output(d)


def test_false_value():

    d = DefaultOrderedDict(DefaultOrderedDict)
    d["key"] = False
    print(json.dumps(d, indent=4))
    assert(d["key"] == False)


def test_case_sensitive_ordered_dict():

    d = CaseInsensitiveOrderedDict()
    d["KeY1"] = 1
    d["KEY2"] = 2
    d["key3"] = 3

    print(json.dumps(d, indent=4))
    assert(d["kEy2"] == 2)



def run_tests():
    # pytest.main(["tests/test_ordereddict.py::test_dict"])
    pytest.main(["tests/test_ordereddict.py"])


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # run_tests()
    test_case_sensitive_ordered_dict()
    print("Done!")
