import os
import pytest
from mappyfile.parser import Parser
import mappyfile
from mappyfile.transformer import MapFile2Dict__Transformer

def graphviz_setup():

    gviz = r"C:\Program Files (x86)\Graphviz2.38\bin"
    os.environ['PATH'] = gviz + ';' + os.environ['PATH']

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


    ast.to_png_with_pydot(r'style.png')


def test_all_maps():

    sample_dir = os.path.join(os.path.dirname(__file__), "sample_maps")

    p = Parser()

    for fn in os.listdir(sample_dir):
        ast = p.parse_file(os.path.join(sample_dir, fn))
        ast.to_png_with_pydot(r'C:\Temp\Trees\%s.png' % os.path.basename(fn))

def test_includes():
    p = Parser()
   
    ast = p.parse_file('./tests/samples/include1.map')
    m = MapFile2Dict__Transformer()

    d = (m.transform(ast)) # works
    print(mappyfile.dumps(d))
     

def run_tests():        
    pytest.main(["tests/test_parser.py::test_parse_style"])
    #pytest.main(["tests/test_parser.py::test_all_maps"])
    #pytest.main(["tests/test_parser.py"])

if __name__ == '__main__':
    graphviz_setup()
    #run_tests()
    #test_parse_style()
    #test_all_maps()
    test_includes()