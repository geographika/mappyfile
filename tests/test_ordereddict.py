import logging
import json
import inspect
import pytest
from mappyfile.parser import Parser
from mappyfile.pprint import PrettyPrinter
from mappyfile.transformer import MapfileToDict
from mappyfile.ordereddict import DefaultOrderedDict


def get_dict(s):
    """
    Parse, transform, and pretty print
    the result
    """
    p = Parser()
    m = MapfileToDict()
    logging.info(inspect.stack()[1][3])

    ast = p.parse(s)
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

    print(d["CONFIG"])  # even though this key is now lowercase it will correctly return (DefaultOrderedDict only)
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


def run_tests():
    # pytest.main(["tests/test_ordereddict.py::test_dict"])
    pytest.main(["tests/test_ordereddict.py"])


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    test_config_directive()
    # test_debug()
    # test_dict()
    print("Done!")
