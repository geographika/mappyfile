import pytest

from mappyfile.ordereddict import DefaultOrderedDict

def test_dict():

    d = DefaultOrderedDict()
    d["key"] = ["value"]

    print d["key"]

def run_tests():        
    #pytest.main(["tests/test_ordereddict.py::test_dict"])
    pytest.main(["tests/test_ordereddict.py"])

if __name__ == '__main__':
    run_tests()
    #test_dict()