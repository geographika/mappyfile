import logging
import json
import inspect
import pytest
from mappyfile.parser import Parser
from mappyfile.pprint import PrettyPrinter
from mappyfile.transformer import MapfileToDict


def output(s):
    """
    Parse, transform, and pretty print
    the result
    """
    p = Parser()
    m = MapfileToDict()

    # https://stackoverflow.com/questions/900392/getting-the-caller-function-name-inside-another-function-in-python
    logging.info(inspect.stack()[1][3])

    ast = p.parse(s)
    logging.debug(ast)
    d = m.transform(ast)
    logging.debug(json.dumps(d, indent=4))
    pp = PrettyPrinter(indent=0, newlinechar=" ", quote="'")
    s = pp.pprint(d)
    logging.debug(s)
    return s


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


def test_style_pattern5():
    """
    Test pattern with decimal places
    """
    s = """
    STYLE
        PATTERN
            5.0 5.0
        END
    END
    """
    exp = "STYLE PATTERN 5.0 5.0 END END"
    assert(output(s) == exp)


@pytest.mark.xfail
def test_style_pattern_fail():
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
    # print output(s)
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
    # print output(s)
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
    # print output(s)
    exp = "MAP QUERYMAP COLOR 255 255 0 SIZE -1 -1 STATUS OFF STYLE HILITE END END"
    assert(output(s) == exp)


def test_output_format_esri():

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
    # print(output(s))
    assert(output(s) == exp)


def test_runtime_expression():
    s = """
    CLASS
      EXPRESSION ( [EPPL_Q100_] = %eppl% )
    END
    """
    exp = "CLASS EXPRESSION (( [EPPL_Q100_] = %eppl% )) END"
    # print(output(s))
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
    Uses Earley
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
    Uses Earley
    """
    s = """
    CLASS
        EXPRESSION ( "[building]" eq NULL)
    END
    """
    exp = 'CLASS EXPRESSION (( "[building]" eq NULL )) END'
    # print(output(s))
    assert(output(s) == exp)


def test_no_linebreaks():
    """
    Check that classes can be nested on a single line
    Uses Earley
    """
    s = "CLASS NAME 'Test' STYLE OUTLINECOLOR 0 0 0 END END"
    exp = "CLASS NAME 'Test' STYLE OUTLINECOLOR 0 0 0 END END"
    assert(output(s) == exp)


def test_colorrange():
    """
    {"colorrange": ["\"#0000ffff\"", "\"#ff0000ff\""], "datarange": [32, 255], "__type__": "style"}
    """
    s = """
    STYLE
        COLORRANGE "#0000ffff" "#ff0000ff"
        DATARANGE 32 255
    END
    """
    exp = "STYLE COLORRANGE '#0000ffff' '#ff0000ff' DATARANGE 32 255 END"
    assert(output(s) == exp)


def test_path_numeric():
    """
    Make sure any folder ending with a number is not
    split into a NAME and PATH token
    """
    s = """
    LAYER
        DATA folder123/file
    END
    """
    exp = "LAYER DATA folder123/file END"
    assert(output(s) == exp)


@pytest.mark.xfail
def test_symbol_style():
    """
    This works if barb_warm is in quotes
    It parses successfully but raisesan error in:

    .\mappyfile\pprint.py", line 262, in _format
    assert(len(composite.keys()) == 1)
    AttributeError: 'Token' object has no attribute 'keys'
    """
    s = """
    CLASS
        STYLE
            INITIALGAP 15
            SYMBOL barb_warm
            GAP -45
        END
    END
    """
    exp = "CLASS STYLE INITIALGAP 15 SYMBOL barb_warm GAP -45 END END"
    assert(output(s) == exp)


def test_extent():
    """
    Make sure any folder ending with a number is not
    split into a NAME and PATH token
    """
    s = """
    MAP
        EXTENT -903661.3649 6426848.5209 201564.4067 8586384.8116
    END
    """
    exp = "MAP EXTENT -903661.3649 6426848.5209 201564.4067 8586384.8116 END"
    assert(output(s) == exp)


def test_expression():
    """
    Addressed in issue #27, now parses successfully.
    """
    s = """
    CLASS
        EXPRESSION ('[construct]' ~* /Br.*$/)
        STYLE
            ANGLE 360
        END
    END
    """
    exp = "CLASS EXPRESSION (( '[construct]' ~* /Br.*$/ )) STYLE ANGLE 360 END END"
    assert(output(s) == exp)


def test_list_expression():
    """
    See issue #27
    """
    s = """
    CLASS
        EXPRESSION /NS_Bahn|NS_BahnAuto/
    END
    """
    exp = "CLASS EXPRESSION /NS_Bahn|NS_BahnAuto/ END"
    assert(output(s) == exp)


@pytest.mark.xfail
def test_escaped_string():
    """
    http://mapserver.org/mapfile/expressions.html#quotes-escaping-in-strings
    Extra spaces currently added
    Starting with MapServer 6.0 you don't need to escape single quotes within double quoted strings
    and you don't need to escape double quotes within single quoted strings
    """
    s = """
    CLASS
        EXPRESSION "National \"hero\" statue"
    END
    """
    exp = "CLASS EXPRESSION 'National 'hero' statue' END"
    assert(output(s) == exp)


def run_tests():
    """
    Need to comment out the following line in C:\VirtualEnvs\mappyfile\Lib\site-packages\pep8.py
    #stdin_get_value = sys.stdin.read
    Or get AttributeError: '_ReplInput' object has no attribute 'read'
    """
    # pytest.main(["tests/test_snippets.py::test_style_pattern"])
    pytest.main(["tests/test_snippets.py"])


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # test_escaped_string()
    # test_style_pattern5()
    run_tests()
    print("Done!")
