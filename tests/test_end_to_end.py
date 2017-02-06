import pytest
from mappyfile.parser import Parser
from mappyfile.transformer import MapfileToDict
from mappyfile.pprint import PrettyPrinter

def process(s):
    p = Parser()
    ast = p.parse(s)
    t = MapfileToDict()
    d = t.transform(ast)
    pp = PrettyPrinter()
    res = pp.pprint(d)
    print res
    return res

def test_processing_directive():

    s = """LAYER
    NAME 'ProcessingLayer'
    PROCESSING 'BANDS=1'
    PROCESSING 'CONTOUR_ITEM=elevation'
    PROCESSING 'CONTOUR_INTERVAL=20'
END"""

    res = process(s)
    assert(res == s)

def test_config_directive():

    s = """MAP
    NAME "ConfigMap"
    CONFIG MS_ERRORFILE "stderr"
    CONFIG "PROJ_DEBUG" "OFF"
    CONFIG "ON_MISSING_DATA" "IGNORE"
END"""

    res = process(s)
    assert(res == s)

def run_tests():        
    #pytest.main(["tests/test_end_to_end.py::test_config_directive"])
    pytest.main(["tests/test_end_to_end.py"])

if __name__ == '__main__':

    run_tests()
    #test_config_directive()