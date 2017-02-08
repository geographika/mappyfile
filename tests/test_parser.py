import os
import pytest
from mappyfile.parser import Parser
from mappyfile.pprint import PrettyPrinter
import mappyfile
from mappyfile.transformer import MapfileToDict

def output(s):
    p = Parser()
    m = MapfileToDict()
    
    ast = p.parse(s)
    print(ast)
    d = m.transform(ast)
    pp = PrettyPrinter(indent=0, newlinechar=" ")
    return pp.pprint(d)

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
     
def test_layer():

    s = "LAYER NAME 'Test' END"

    assert(output(s) == s)

def test_class():

    s = "CLASS NAME 'Test' END"

    assert(output(s) == s)

def test_style():

    s = "STYLE COLOR 0 0 255 WIDTH 5 LINECAP BUTT END"
    assert(output(s) == s)

def test_style_pattern():

    s = """
    STYLE 
    COLOR 0 0 255 
    WIDTH 5 
    LINECAP BUTT 
    PATTERN 5.0 5.0 END 
    END
    """

    exp = "STYLE COLOR 0 0 255 WIDTH 5 LINECAP BUTT PATTERN 5.0 5.0 END END"
    assert(output(s) == exp)

def test_style_pattern2():

    s = """
    STYLE 
    COLOR 0 0 255 
    WIDTH 5 
    LINECAP BUTT 
    PATTERN 
    5.0 5.0 
    END 
    END
    """

    exp = "STYLE COLOR 0 0 255 WIDTH 5 LINECAP BUTT PATTERN 5.0 5.0 END END"
    assert(output(s) == exp)

def test_style_pattern3():
    """
    This type of string fails
    """
    s = "STYLE COLOR 0 0 255 WIDTH 5 LINECAP BUTT PATTERN 5 5 END END"
    exp = "STYLE COLOR 0 0 255 WIDTH 5 LINECAP BUTT PATTERN 5 5 END END"
    assert(output(s) == exp)

def test_style_pattern4():
    """
    Fails
    A single value on each line
    Need new part to grammar?
    | PATTERN NL+ ((int|float) NL*)* END

    However this causes:
    ParseError: Ambiguous parsing results (1024)

    """
    s = """
    STYLE 
    COLOR 0 0 255 
    WIDTH 5 
    LINECAP BUTT 
    PATTERN 
    5.0 
    5.0 
    END 
    END
    """
    exp = "STYLE COLOR 0 0 255 WIDTH 5 LINECAP BUTT PATTERN 5.0 5.0 END END"
    assert(output(s) == exp)

def xtest_metadata():
    """
    Cannot parse metadata directly
    """
    s = """METADATA 'wms_title' 'Test simple wms' END"""

    assert(output(s) == s)
  
def run_tests():        
    pytest.main(["tests/test_parser.py::test_style_pattern"])
    #pytest.main(["tests/test_parser.py"])

if __name__ == '__main__':

    #run_tests()
    #test_all_maps()
    #test_includes()
    test_style_pattern3()