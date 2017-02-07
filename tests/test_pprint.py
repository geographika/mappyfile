import pytest
from mappyfile.pprint import PrettyPrinter

def test_print_map():
    mf = {}
    pp = PrettyPrinter() # expected
    txt = pp.pprint(mf)
    assert(expected == txt)

def run_tests():        
    #pytest.main(["tests/test_pprint.py::test_print_map"])
    pytest.main(["tests/test_pprint.py"])

if __name__ == "__main__":
    run_tests()

