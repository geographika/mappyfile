import os
import pytest
from mappyfile.parser import Parser

def test_parse_style():
    s = """
            STYLE
                COLOR 99 231 117
                WIDTH 1
            END
    """
    p = Parser()
    ast = p.parse(s)
    print(ast)
    #r.to_png_with_pydot(r'style.png')


def test_all_maps():

    sample_dir = os.path.join(os.path.dirname(__file__), "sample_maps")

    p = Parser()

    for fn in os.listdir(sample_dir):
        r = p.parse_file(os.path.join(sample_dir, fn))

def run_tests():        
    pytest.main(["tests/test_parser.py::test_parse_style"])
    #pytest.main(["tests/test_parser.py::test_all_maps"])
    #pytest.main(["tests/test_parser.py"])

if __name__ == '__main__':
    #run_tests()
    test_parse_style()