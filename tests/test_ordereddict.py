import logging
import json
from copy import deepcopy
import inspect
import tempfile
import pickle
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
    assert(d["key"] is False)


def test_case_sensitive_ordered_dict():

    d = CaseInsensitiveOrderedDict()
    d["KeY1"] = 1
    d["KEY2"] = 2
    d["key3"] = 3

    print(json.dumps(d, indent=4))
    assert(d["kEy2"] == 2)


def test_update_case_sensitive_ordered_dict():

    d = CaseInsensitiveOrderedDict(CaseInsensitiveOrderedDict)

    d["b"] = "hello"
    d["a"] = "goodbye"

    print(json.dumps(d, indent=4))

    d["config"]["ms_errorfile"] = "error.log"
    print(json.dumps(d, indent=4))

    d.update({"c": "hello"})

    print(json.dumps(d, indent=4))

    d.update(red=1, blue=2)

    print(json.dumps(d, indent=4))
    assert(d["a"] == "goodbye")


def test_pickling():
    """
    See issue #68
    """

    s = """
    MAP
        NAME "Test"
        LAYER
            NAME "Layer1"
            CLASS
                NAME "Class1"
            END
        END
    END
    """

    d = get_dict(s)
    tf1 = tempfile.NamedTemporaryFile(delete=False)
    pickle.dump(d, tf1)
    tf1.close()

    with open(tf1.name, "rb") as tf2:
        d2 = pickle.load(tf2)

    assert d2["layers"][0]["classes"][0]["name"] == "Class1"


def test_copy():
    d = CaseInsensitiveOrderedDict()
    d["key1"] = "val1"
    c = d.copy()
    c["key1"] = "val2"
    assert d["key1"] == "val1"


def test_has_key():
    d = CaseInsensitiveOrderedDict()
    d["key1"] = "val1"
    assert "key1" in d
    assert "key2" not in d


def test_pop():
    d = CaseInsensitiveOrderedDict()
    d["key1"] = "val1"
    v = d.pop("key1")
    assert v == "val1"
    assert len(d.keys()) == 0


def test_deepcopy():
    """
    See issue #73
    """
    d = DefaultOrderedDict()
    d['__type__'] = 'layer'

    c = deepcopy(d)
    assert c['__type__'] == 'layer'


def run_tests():
    # pytest.main(["tests/test_ordereddict.py::test_dict"])
    pytest.main(["tests/test_ordereddict.py"])


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # run_tests()
    # test_update_case_sensitive_ordered_dict()
    test_pop()
    print("Done!")
