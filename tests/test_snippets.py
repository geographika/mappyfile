import os, logging
import pytest
from mappyfile.parser import Parser
from mappyfile.pprint import PrettyPrinter
import mappyfile
from mappyfile.transformer import MapfileToDict

def output(s):
    """
    Parse, transform, and pretty print 
    the result
    """
    p = Parser()
    m = MapfileToDict()
    
    ast = p.parse(s)
    #print(ast)
    d = m.transform(ast)
    #print(d)
    pp = PrettyPrinter(indent=0, newlinechar=" ", quote="'")
    return pp.pprint(d)


def check_result(s):
    try:
        s2 = output(s)
        assert(s == s2)
    except AssertionError:
        logging.info(s)
        logging.info(s2)
        raise


def test_layer():
    s = "LAYER NAME 'Test' END"
    check_result(s)


def test_class():

    s = "CLASS NAME 'Test' END"
    check_result(s)


def test_style():

    s = "STYLE COLOR 0 0 255 WIDTH 5 LINECAP BUTT END"
    check_result(s)


def test_style_pattern():

    s = """
    STYLE
        PATTERN 5 5 END 
    END
    """

    exp = "STYLE PATTERN 5 5 END END"
    assert(output(s) == exp)


def test_style_pattern2():

    s = """
    STYLE 
        PATTERN 
            5 5
        END 
    END
    """

    exp = "STYLE PATTERN 5 5 END END"
    assert(output(s) == exp)


def test_style_pattern3():
    """
    Test a STYLE on one line can be parsed
    """
    s = "STYLE PATTERN 5 5 END END"
    exp = "STYLE PATTERN 5 5 END END"
    assert(output(s) == exp)


def test_style_pattern4():
    """
    Test pattern values on separate lines are valid
    """
    s = """
    STYLE 
        PATTERN 
            5
            5 
        END 
    END
    """
    exp = "STYLE PATTERN 5 5 END END"
    assert(output(s) == exp)

@pytest.mark.xfail
def test_style_pattern5():
    """
    Test pattern with odd number of values
    This should fail with the following error message
    UnexpectedToken: Unexpected token Token(_END, 'END') at line 3, column 27.
    """
    s = """
    STYLE 
        PATTERN 6 4 2 4 6 END
    END
    """
    exp = "STYLE PATTERN 6 4 2 4 6 END END"
    assert(output(s) == exp)

def test_metadata():
    """
    Parse metadata directly
    """
    s = """
    METADATA 
        'wms_title' 'Test simple wms'
    END
    """
    exp = """METADATA 'wms_title' 'Test simple wms' END"""
    assert(output(s) == exp)

def test_metadata_unquoted():
    """
    The METADATA block doesn't need quotes 
    (as long as values don't have spaces)
    """
    s = """
    METADATA 
        wms_title my_title
    END
    """
    exp = """METADATA wms_title my_title END"""
    #print output(s)
    assert(output(s) == exp)

def test_validation():
    """
    Parse validation block directly
    """
    s = """
    VALIDATION
        "field1" "^[0-9,]+$"
        "field2" "-1"
    END
    """
    #print output(s)
    exp = """VALIDATION 'field1' '^[0-9,]+$' 'field2' '-1' END"""
    assert(output(s) == exp)

def test_layer_text_query():
    s = """
    CLASS
        TEXT (tostring([area],"%.2f"))
    END
    """
    exp = """CLASS TEXT ((tostring([area],"%.2f"))) END"""
    assert(output(s) == exp)


def test_label():
    s = """
    LABEL
      COLOR  0 0 0
      FONT Vera
      TYPE truetype
      SIZE 8
      POSITION AUTO
      PARTIALS FALSE
      OUTLINECOLOR 255 255 255			
    END 
    """
    exp = "LABEL COLOR 0 0 0 FONT Vera TYPE truetype SIZE 8 POSITION AUTO PARTIALS FALSE OUTLINECOLOR 255 255 255 END"
    assert(output(s) == exp)


def test_output_format():

    s = """
    MAP
        IMAGETYPE grid
        OUTPUTFORMAT
          NAME grid2
          DRIVER "GDAL/AAIGRID"
          IMAGEMODE INT16
          FORMATOPTION 'NULLVALUE=-99'
        END
    END
    """
    exp = "MAP IMAGETYPE grid OUTPUTFORMAT NAME grid2 DRIVER 'GDAL/AAIGRID' IMAGEMODE INT16 FORMATOPTION 'NULLVALUE=-99' END END"
    assert(output(s) == exp)


def test_class_symbol():
    s = """
    CLASS
        STYLE # a shadow
            COLOR 151 151 151
            SYMBOL [symbol]
            OFFSET 2 2
            SIZE [size]
        END
    END
    """
    exp = "CLASS STYLE COLOR 151 151 151 SYMBOL [symbol] OFFSET 2 2 SIZE [size] END END"
    assert(output(s) == exp)


def test_filter():
    s = """
    LAYER
        NAME 'filters_test002'
        FILTER 'aitkin'i
    END
    """

    exp = "LAYER NAME 'filters_test002' FILTER 'aitkin'i END"
    assert(output(s) == exp)


def test_regex():
    s = r"""
    LAYER
        NAME 'regexp-example'
        FILTERITEM 'placename'
        FILTER \hotel\
    END
    """
    exp = r"LAYER NAME 'regexp-example' FILTERITEM 'placename' FILTER \hotel\ END"
    assert(output(s) == exp)


def test_feature():
    """
    With multiple points
    """

    s = """
        LAYER        
            FEATURE
                POINTS
                    0 10
                END
                POINTS
                    -20 20
                    20 20
                    -20 -20
                    0 -30
                    20 -20
                    -20 20
                    -20 20
                    30 30
                END
            END
        END
    """

    exp = "LAYER FEATURE POINTS 0 10 END POINTS -20 20 20 20 -20 -20 0 -30 20 -20 -20 20 -20 20 30 30 END END END"
    assert(output(s) == exp)


def test_symbol():

    s = '''
    SYMBOL
        NAME 'triangle'
        TYPE VECTOR
        POINTS
            0 4
            2 0
            4 4
            0 4
        END
        FILLED TRUE
    END
    '''
    exp = "SYMBOL NAME 'triangle' TYPE VECTOR FILLED TRUE POINTS 0 4 2 0 4 4 0 4 END END"
    assert(output(s) == exp)


def test_class_expression1():
    s = '''
    CLASS
      TEXT ([area])
    END
    '''
    exp = "CLASS TEXT ([area]) END"
    assert(output(s) == exp)


def test_class_expression2():
    """
    shp2img -m C:\Temp\msautotest\query\text.tmp.map  -l text_test002 -o c:\temp\tmp_onl0lk.png
    """
    s = '''
    CLASS
      TEXT ("[area]")
    END
    '''
    exp = 'CLASS TEXT ("[area]") END'
    assert(output(s) == exp)


def test_complex_class_expression():
    s = '''
    CLASS
      TEXT ("Area is: " + tostring([area],"%.2f"))
    END
    '''         
    exp = '''CLASS TEXT ("Area is: " + (tostring([area],"%.2f"))) END'''
    assert(output(s) == exp)


def test_or_expressions():
    """
    See http://www.mapserver.org/mapfile/expressions.html#expressions
    """

    s = '''
    CLASS
        EXPRESSION ("[style_class]" = "10" OR "[style_class]" = "20")
    END
    '''

    exp = 'CLASS EXPRESSION (( ( "[style_class]" = "10" ) or ( "[style_class]" = "20" ) )) END'
    assert(output(s) == exp)

    s = '''
    CLASS
        EXPRESSION ("[style_class]" = "10" || "[style_class]" = "20")
    END
    '''

    exp = 'CLASS EXPRESSION (( ( "[style_class]" = "10" ) or ( "[style_class]" = "20" ) )) END'
    assert(output(s) == exp)


def test_and_expressions():
    s = '''
    CLASS
        EXPRESSION ("[style_class]" = "10" AND "[style_class]" = "20")
    END
    '''

    exp = 'CLASS EXPRESSION (( ( "[style_class]" = "10" ) and ( "[style_class]" = "20" ) )) END'
    assert(output(s) == exp)

    s = '''
    CLASS
        EXPRESSION ("[style_class]" = "10" && "[style_class]" = "20")
    END
    '''

    exp = 'CLASS EXPRESSION (( ( "[style_class]" = "10" ) and ( "[style_class]" = "20" ) )) END'
    assert(output(s) == exp)


def test_not_expressions():
    s = '''
    CLASS
        EXPRESSION NOT("[style_class]" = "20")
    END
    '''

    exp = 'CLASS EXPRESSION not (( "[style_class]" = "20" )) END'
    assert(output(s) == exp)

    s = '''
    CLASS
        EXPRESSION !("[style_class]" = "20")
    END
    '''

    exp = 'CLASS EXPRESSION not (( "[style_class]" = "20" )) END'
    assert(output(s) == exp)


def test_processing_directive():

    s = """
    LAYER
        NAME 'ProcessingLayer'
        PROCESSING 'BANDS=1'
        PROCESSING 'CONTOUR_ITEM=elevation'
        PROCESSING 'CONTOUR_INTERVAL=20'
    END
    """

    #print(output(s))
    exp = "LAYER NAME 'ProcessingLayer' PROCESSING 'BANDS=1' PROCESSING 'CONTOUR_ITEM=elevation' PROCESSING 'CONTOUR_INTERVAL=20' END"
    assert(output(s) == exp)


def test_config_directive():

    s = """
    MAP
        NAME 'ConfigMap'
        CONFIG MS_ERRORFILE 'stderr'
        CONFIG 'PROJ_DEBUG' 'OFF'
        CONFIG 'ON_MISSING_DATA' 'IGNORE'
    END
    """

    exp = "MAP NAME 'ConfigMap' CONFIG MS_ERRORFILE 'stderr' CONFIG 'PROJ_DEBUG' 'OFF' CONFIG 'ON_MISSING_DATA' 'IGNORE' END"
    assert(output(s) == exp)

def test_multiple_composites():
    """
    Allow for multiple root composites
    This allows for easier addition of CLASSES and STYLES
    """

    s = """
    CLASS
        Name "Name1"
    END
    CLASS
        Name "Name2"
    END
    """
    exp = "CLASS NAME 'Name1' END CLASS NAME 'Name2' END"
    assert(output(s) == exp)

def test_map():
    s = """
    MAP
        LAYER
            NAME 'test'
        END
    END
    """

    exp = "MAP LAYER NAME 'test' END END"
    assert(output(s) == exp)


def test_oneline_composites():
    """
    Test a composite on one line is parsed correctly
    """

    s = """
    CLASS
    PROJECTION "init=epsg:2056"
    END
    END
    """

    # put on one line
    exp = ' '.join(s.split())
    assert(output(s) == exp)

def test_querymap():

    s = """
    MAP
        QUERYMAP
           COLOR 255 255 0
           SIZE -1 -1
           STATUS OFF
           STYLE HILITE
         END
    END
    """
    #print output(s)
    exp = "MAP QUERYMAP COLOR 255 255 0 SIZE -1 -1 STATUS OFF STYLE HILITE END END"
    assert(output(s) == exp)

def test_output_format():

    s = """
    OUTPUTFORMAT
        NAME "shapezip"
        DRIVER "OGR/ESRI Shapefile"
        TRANSPARENT FALSE
        IMAGEMODE FEATURE
    END
    """
    exp = "OUTPUTFORMAT NAME 'shapezip' DRIVER 'OGR/ESRI Shapefile' TRANSPARENT FALSE IMAGEMODE FEATURE END"
    assert(output(s) == exp)

def test_auto_projection():
    """
    Test an AUTO projection
    """

    s = """
    MAP
        PROJECTION
            AUTO
        END
    END
    """
    exp = "MAP PROJECTION AUTO END END"
    #print(output(s))
    assert(output(s) == exp)

def test_runtime_expression():
    s = """
    CLASS
      EXPRESSION ( [EPPL_Q100_] = %eppl% )		   
    END
    """
    exp = "CLASS EXPRESSION (( [EPPL_Q100_] = %eppl% )) END"
    #print(output(s))
    assert(output(s) == exp)

def test_mutliple_output_formats():
    """
    https://github.com/geographika/mappyfile/issues/20
    """
    s = """
    OUTPUTFORMAT
        FORMATOPTION "FORM=zip"
        FORMATOPTION "SPATIAL_INDEX=YES"
    END
    """
    exp = "OUTPUTFORMAT FORMATOPTION 'FORM=zip' FORMATOPTION 'SPATIAL_INDEX=YES' END"
    assert(output(s) == exp)

def test_config_case():
    """
    https://github.com/geographika/mappyfile/issues/18
    """

    s = """
    MAP
	    CONFIG "PROJ_LIB" "projections"
    END
    """
    exp = "MAP CONFIG 'PROJ_LIB' 'projections' END"
    assert(output(s) == exp)

def test_ne_comparison():
    """
    IS NOT is not valid
    NE (Not Equals) should be used instead 
    """
    s = """
    CLASS
        # EXPRESSION ( "[building]" IS NOT NULL) # incorrect syntax
        EXPRESSION ( "[building]" NE NULL)
    END
    """
    exp = 'CLASS EXPRESSION (( "[building]" NE NULL )) END'
    assert(output(s) == exp)

def test_eq_comparison():
    """
    Case is not changed for comparison (EQ/eq stay the same)
    """
    s = """
    CLASS
        EXPRESSION ( "[building]" eq NULL)
    END
    """
    exp = 'CLASS EXPRESSION (( "[building]" eq NULL )) END'
    #print(output(s))
    assert(output(s) == exp)

@pytest.mark.xfail
def test_no_linebreaks():
    """
    Check that classes can be nested on a single line
    """
    s = """CLASS NAME 'Test' STYLE OUTLINECOLOR 0 0 0 END END"""
    exp = "CLASS NAME 'Test' STYLE OUTLINECOLOR 0 0 0 END END"
    assert(output(s) == exp)

def run_tests():        
    #pytest.main(["tests/test_snippets.py::test_style_pattern"])
    pytest.main(["tests/test_snippets.py"])

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    #test_no_linebreaks()
    run_tests()
    print("Done!")
