import os
import pytest
from mappyfile.parser import Parser
import mappyfile
from mappyfile.transformer import MapfileToDict


def test_all_maps():

    sample_dir = os.path.join(os.path.dirname(__file__), "sample_maps")

    p = Parser()

    for fn in os.listdir(sample_dir):
        ast = p.parse_file(os.path.join(sample_dir, fn))
        ast.to_png_with_pydot(r'C:\Temp\Trees\%s.png' % os.path.basename(fn))

def test_includes():
    p = Parser()
   
    ast = p.parse_file('./tests/samples/include1.map')
    m = MapfileToDict()

    d = (m.transform(ast)) # works
    print(mappyfile.dumps(d))
     

def run_tests():        
    pytest.main(["tests/test_parser.py::test_parse_style"])
    #pytest.main(["tests/test_parser.py::test_all_maps"])
    #pytest.main(["tests/test_parser.py"])

if __name__ == '__main__':

    #run_tests()
    #test_parse_style()
    #test_all_maps()
    test_includes()