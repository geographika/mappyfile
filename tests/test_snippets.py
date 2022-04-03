# -*- coding: utf-8 -*-

import logging
import json
import inspect
import pytest
import mappyfile
from mappyfile.parser import Parser
from mappyfile.pprint import PrettyPrinter
from mappyfile.transformer import MapfileToDict
from mappyfile.validator import Validator


def output(s, include_position=True, schema_name="map"):
    """
    Parse, transform, validate, and pretty print
    the result
    """
    p = Parser()
    m = MapfileToDict(include_position=include_position)

    # https://stackoverflow.com/questions/900392/getting-the-caller-function-name-inside-another-function-in-python
    logging.info(inspect.stack()[1][3])

    ast = p.parse(s)
    logging.debug(ast.pretty())
    d = m.transform(ast)
    logging.debug(json.dumps(d, indent=4))
    v = Validator()
    errors = v.validate(d, schema_name=schema_name)
    logging.error(errors)
    pp = PrettyPrinter(indent=0, newlinechar=" ", quote="'")
    s = pp.pprint(d)
    logging.debug(s)
    assert(len(errors) == 0)
    return s


def check_result(s, schema_name="map"):
    s2 = output(s, schema_name=schema_name)
    try:
        assert(s == s2)
    except AssertionError:
        logging.info(s)
        logging.info(s2)
        raise


def test_layer():
    s = "LAYER NAME 'Test' TYPE POINT END"
    check_result(s, schema_name="layer")


def test_class():

    s = "CLASS NAME 'Test' END"
    check_result(s, schema_name="class")


def test_map_size():

    s = """
    MAP
    SIZE 256 256
    END"""

    exp = "MAP SIZE 256 256 END"
    assert(output(s) == exp)


def test_style_color():

    s = """
    STYLE
    COLOR 0 0 255
    END"""

    exp = "STYLE COLOR 0 0 255 END"
    assert(output(s, schema_name="style") == exp)


def test_style():

    s = """
    STYLE
    COLOR 0 0 255
    WIDTH 5
    LINECAP BUTT
    END"""

    exp = "STYLE COLOR 0 0 255 WIDTH 5 LINECAP BUTT END"
    assert(output(s, schema_name="style") == exp)


def test_style_oneline():

    s = "STYLE COLOR 0 0 255 WIDTH 5 LINECAP BUTT END"
    check_result(s, schema_name="style")


def test_style_pattern():

    s = """
    STYLE
        PATTERN 5 5 END
    END
    """

    exp = "STYLE PATTERN 5 5 END END"
    assert(output(s, schema_name="style") == exp)


def test_style_pattern2():

    s = """
    STYLE
        PATTERN
            5 5
        END
    END
    """

    exp = "STYLE PATTERN 5 5 END END"
    assert(output(s, schema_name="style") == exp)


def test_style_pattern3():
    """
    Test a STYLE on one line can be parsed
    """
    s = "STYLE PATTERN 5 5 END END"
    exp = "STYLE PATTERN 5 5 END END"
    assert(output(s, schema_name="style") == exp)


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
    assert(output(s, schema_name="style") == exp)


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
    assert(output(s, schema_name="style") == exp)


def test_style_offset_mixed():
    """
    Test an attribute and numerical pair for a STYLE OFFSET
    See https://github.com/geographika/mappyfile/issues/114
    """
    s = """
    STYLE
        OFFSET [attribute] -999
    END
    """
    exp = "STYLE OFFSET [attribute] -999 END"
    assert(output(s, schema_name="style") == exp)


def test_style_offset_mixed2():
    """
    As above but reversed
    """
    s = """
    STYLE
        OFFSET -999 [attribute]
    END
    """
    exp = "STYLE OFFSET -999 [attribute] END"
    assert(output(s, schema_name="style") == exp)


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
    assert(output(s, schema_name="metadata") == exp)


def test_metadata_uppercase():

    s = """
    METADATA
        'WMS_TITLE' 'Test simple wms'
    END
    """
    exp = """METADATA 'wms_title' 'Test simple wms' END"""
    assert(output(s, schema_name="metadata") == exp)


def test_duplicated_metadata_keys():
    """
    The second key will be used
    """

    s = """
    METADATA
        'wms_title' 'Test simple wms'
        'wms_title' 'Test simple wms2'
    END
    """
    exp = """METADATA 'wms_title' 'Test simple wms2' END"""
    assert(output(s, schema_name="metadata") == exp)


def test_metadata_unquoted():
    """
    The METADATA block doesn't need quotes
    (as long as values don't have spaces)
    The printer will add quotes automatically
    """
    s = """
    METADATA
        wms_title my_title
    END
    """
    exp = "METADATA 'wms_title' 'my_title' END"
    assert(output(s, schema_name="metadata") == exp)


def test_validation():
    """
    Parse validation block directly
    """
    s = """
    VALIDATION
        "field1" "^[0-9,]+$"
        "field2" "-1"
        qstring '.'
    END
    """
    exp = """VALIDATION 'field1' '^[0-9,]+$' 'field2' '-1' 'qstring' '.' END"""
    assert(output(s, schema_name="validation") == exp)


def test_layer_text_query():
    s = """
    CLASS
        TEXT (tostring([area],"%.2f"))
    END
    """
    exp = """CLASS TEXT (tostring([area],"%.2f")) END"""
    assert(output(s, schema_name="class") == exp)


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
    exp = "LABEL COLOR 0 0 0 FONT 'Vera' TYPE TRUETYPE SIZE 8 POSITION AUTO PARTIALS FALSE OUTLINECOLOR 255 255 255 END"
    assert(output(s, schema_name="label") == exp)


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
    exp = "MAP IMAGETYPE 'grid' OUTPUTFORMAT NAME 'grid2' DRIVER 'GDAL/AAIGRID' IMAGEMODE INT16 FORMATOPTION 'NULLVALUE=-99' END END"
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
    assert(output(s, schema_name="class") == exp)


def test_filter():
    s = """
    LAYER
        TYPE POINT
        NAME 'filters_test002'
        FILTER 'aitkin'i
    END
    """

    exp = "LAYER TYPE POINT NAME 'filters_test002' FILTER 'aitkin'i END"
    assert(output(s, schema_name="layer") == exp)


def test_like_filter():
    s = """
    LAYER
        TYPE POINT
        NAME 'filters_test003'
        FILTER ("blpu_classification_code" LIKE 'RI%')
    END
    """

    exp = r"""LAYER TYPE POINT NAME 'filters_test003' FILTER ( "blpu_classification_code" LIKE 'RI%' ) END"""
    assert(output(s, schema_name="layer") == exp)


def test_regex():
    s = r"""
    LAYER
        TYPE POINT
        NAME 'regexp-example'
        FILTERITEM 'placename'
        FILTER /hotel/
    END
    """
    exp = r"LAYER TYPE POINT NAME 'regexp-example' FILTERITEM 'placename' FILTER /hotel/ END"
    assert(output(s, schema_name="layer") == exp)


def test_feature():
    """
    With multiple points
    """

    s = """
    FEATURE
        POINTS
            0 10
        END
    END
    """

    exp = "FEATURE POINTS 0 10 END END"
    assert(output(s, schema_name="feature") == exp)


def test_multi_feature():
    """
    With multiple points
    """

    s = """
        LAYER
            TYPE LINE
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

    exp = "LAYER TYPE LINE FEATURE POINTS 0 10 END POINTS -20 20 20 20 -20 -20 0 -30 20 -20 -20 20 -20 20 30 30 END END END"
    assert(output(s, schema_name="layer") == exp)


def test_triple_feature():
    """
    With multiple points
    """

    s = """
    FEATURE
        POINTS
            0 10
            5 2
        END
        POINTS
            0 10
            3 3
        END
        POINTS
            0 10
            7 7
        END
    END
    """

    exp = "FEATURE POINTS 0 10 5 2 END POINTS 0 10 3 3 END POINTS 0 10 7 7 END END"
    assert(output(s, schema_name="feature") == exp)


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
    exp = "SYMBOL NAME 'triangle' TYPE VECTOR POINTS 0 4 2 0 4 4 0 4 END FILLED TRUE END"
    assert(output(s, schema_name="symbol") == exp)


def test_processing_directive():

    s = """
    LAYER
        NAME 'ProcessingLayer'
        TYPE RASTER
        PROCESSING 'BANDS=1'
        PROCESSING 'CONTOUR_ITEM=elevation'
        PROCESSING 'CONTOUR_INTERVAL=20'
    END
    """

    exp = "LAYER NAME 'ProcessingLayer' TYPE RASTER PROCESSING 'BANDS=1' PROCESSING 'CONTOUR_ITEM=elevation' PROCESSING 'CONTOUR_INTERVAL=20' END"
    assert(output(s, schema_name="layer") == exp)


def test_config_directive():

    s = """
    MAP
        NAME 'ConfigMap'
        CONFIG MS_ERRORFILE 'stderr'
        CONFIG 'PROJ_DEBUG' 'OFF'
        CONFIG 'ON_MISSING_DATA' 'IGNORE'
    END
    """

    exp = "MAP NAME 'ConfigMap' CONFIG 'MS_ERRORFILE' 'stderr' CONFIG 'PROJ_DEBUG' 'OFF' CONFIG 'ON_MISSING_DATA' 'IGNORE' END"
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
    assert(output(s, schema_name="class") == exp)


def test_map():
    s = """
    MAP
        LAYER
            TYPE POINT
            NAME 'test'
        END
    END
    """

    exp = "MAP LAYER TYPE POINT NAME 'test' END END"
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
    # print(output(s))
    exp = "MAP QUERYMAP COLOR 255 255 0 SIZE -1 -1 STATUS OFF STYLE HILITE END END"
    assert(output(s) == exp)


def test_output_format_esri():

    s = """
    OUTPUTFORMAT
        NAME "shapezip"
        DRIVER "OGR/ESRI Shapefile"
        TRANSPARENT ON
        IMAGEMODE FEATURE
    END
    """
    exp = "OUTPUTFORMAT NAME 'shapezip' DRIVER 'OGR/ESRI Shapefile' TRANSPARENT ON IMAGEMODE FEATURE END"
    assert(output(s, schema_name="outputformat") == exp)


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


def test_multiple_output_formats():
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
    assert(output(s, schema_name="outputformat") == exp)


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


def test_no_linebreaks():
    """
    Check that classes can be nested on a single line
    Uses Earley
    """
    s = "CLASS NAME 'Test' STYLE OUTLINECOLOR 0 0 0 END END"
    exp = "CLASS NAME 'Test' STYLE OUTLINECOLOR 0 0 0 END END"
    assert(output(s, schema_name="class") == exp)


def test_hexcolorrange():
    """
    {"colorrange": ["\"#0000ffff\"", "\"#ff0000ff\""], "datarange": [32, 255], "__type__": "style"}
    heat.map(77) - extra hex characters to account for optional alpha values
    COLORRANGE "#0000ffff" "#ff0000ff"
    """
    s = """
    STYLE
        COLORRANGE "#0000ffff" "#ff0000ff"
        DATARANGE 32 255
    END
    """
    exp = "STYLE COLORRANGE '#0000ffff' '#ff0000ff' DATARANGE 32 255 END"
    assert(output(s, schema_name="style") == exp)


def test_hexcolorrange2():
    """
    Check different hex color formats and results are in lower-case
    """

    s = """
    STYLE
        DATARANGE 32 255
        COLORRANGE '#FfF' '#Aaa'
    END
    """
    exp = "STYLE DATARANGE 32 255 COLORRANGE '#fff' '#aaa' END"
    assert(output(s, schema_name="style") == exp)


def test_colorrange():

    s = """
    STYLE
      COLORRANGE 255 0 0  0 255 0
      DATARANGE 0.01 0.05
    END"""

    exp = "STYLE COLORRANGE 255 0 0 0 255 0 DATARANGE 0.01 0.05 END"
    print(output(s, schema_name="style"))
    assert(output(s, schema_name="style") == exp)


def test_path_numeric():
    """
    Make sure any folder ending with a number is not
    split into a NAME and PATH token
    """
    s = """
    LAYER
        DATA folder123/file
        TYPE POINT
    END
    """
    exp = "LAYER DATA 'folder123/file' TYPE POINT END"
    assert(output(s, schema_name="layer") == exp)


def test_class_symbol_style():
    """
    barb_warm is not in quotes
    """
    s = """
    CLASS
        STYLE
            INITIALGAP 15
            SYMBOL "barb_warm"
            GAP -45
        END
    END
    """
    exp = "CLASS STYLE INITIALGAP 15 SYMBOL 'barb_warm' GAP -45 END END"
    assert(output(s, schema_name="class") == exp)


def test_symbol_style():
    """
    barb_warm is not in quotes
    """
    s = """
    STYLE
        SYMBOL barb_warm
    END
    """
    exp = "STYLE SYMBOL 'barb_warm' END"
    assert(output(s, schema_name="style") == exp)


@pytest.mark.xfail
def test_symbol_style2():
    """
    barb_warm is not in quotes
    any attributes after this cause the parser to fail
    """
    s = """
    STYLE
        SYMBOL barb_warm
        GAP -45
        SIZE 8
    END
    """
    exp = "STYLE SYMBOL 'barb_warm' END"
    assert(output(s, schema_name="style") == exp)


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


def test_ogr_connection():

    s = r'''
    LAYER
        CONNECTION '<OGRVRTDataSource><OGRVRTLayer name="poly"><SrcLayer>poly</SrcLayer></OGRVRTLayer></OGRVRTDataSource>'
        TYPE POLYGON
    END
    '''
    exp = r"""LAYER CONNECTION '<OGRVRTDataSource><OGRVRTLayer name="poly"><SrcLayer>poly</SrcLayer></OGRVRTLayer></OGRVRTDataSource>' TYPE POLYGON END"""
    assert(output(s, schema_name="layer") == exp)


def test_quoted_data():
    """
    Make sure a raw string is used
    """

    s = r"""
    LAYER
        DATA "the_geom from (select * from road where \"lpoly_\"=3 order by gid) as foo using unique gid using srid=3978"
        TYPE POLYGON
    END
    """
    exp = r"""LAYER DATA 'the_geom from (select * from road where \"lpoly_\"=3 order by gid) as foo using unique gid using srid=3978' TYPE POLYGON END"""
    assert(output(s, schema_name="layer") == exp)


def test_name_hypens():

    s = """
    MAP
        NAME ms-ogc-workshop
    END
    """
    exp = "MAP NAME 'ms-ogc-workshop' END"
    assert(output(s) == exp)


def test_multiline_metadata():

    s = """
    METADATA
    "ows_title" "layer_0"
    "gml_include_items"
    "all"
    END
    """
    exp = "METADATA 'ows_title' 'layer_0' 'gml_include_items' 'all' END"
    print(output(s, schema_name="metadata"))
    assert(output(s, schema_name="metadata") == exp)


def test_polaroffset():

    s = """
    STYLE  # polaroffset
        SYMBOL "arrowhead"
        COLOR 0 0 0
        ANGLE [rotation]
        POLAROFFSET [length_2] [rotation]
    END"""

    exp = "STYLE SYMBOL 'arrowhead' COLOR 0 0 0 ANGLE [rotation] POLAROFFSET [length_2] [rotation] END"
    print(output(s, schema_name="style"))
    assert(output(s, schema_name="style") == exp)


def test_style_hexcolor():

    s = """
    style
      color "#888888"
      outlinecolor "#000000"
    end
    """

    exp = "STYLE COLOR '#888888' OUTLINECOLOR '#000000' END"
    print(output(s, schema_name="style"))
    assert(output(s, schema_name="style") == exp)


def test_escaped_string():

    s = """
    LAYER
        FILTER (`[LASTMOD]` > `2010-12-01`)
        TYPE POINT
    END
    """
    exp = "LAYER FILTER ( `[LASTMOD]` > `2010-12-01` ) TYPE POINT END"
    print(output(s, schema_name="layer"))
    assert(output(s, schema_name="layer") == exp)


def test_filename():

    s = """
    WEB
        IMAGEURL "/tmp/"
        TEMPLATE example3.html
    END
    """
    exp = "WEB IMAGEURL '/tmp/' TEMPLATE 'example3.html' END"
    print(output(s, schema_name="web"))
    assert(output(s, schema_name="web") == exp)


def test_label_position_uc():

    s = """
    LABEL
      COLOR  0 0 0
      FONT Vera
      TYPE truetype
      SIZE 8
      POSITION UC
      PARTIALS FALSE
      OUTLINECOLOR 255 255 255
    END
    """
    exp = "LABEL COLOR 0 0 0 FONT 'Vera' TYPE TRUETYPE SIZE 8 POSITION UC PARTIALS FALSE OUTLINECOLOR 255 255 255 END"
    assert(output(s, schema_name="label") == exp)


def test_label_attribute_properties():
    """
    See https://github.com/geographika/mappyfile/issues/118
    Required allowing [property] names to be added for FONT, POSITION
    """

    s = """
    LABEL
        FONT [FONTNAME]
        TYPE truetype
        COLOR [TXTCLR]
        SIZE [FONTSIZE]
        ANGLE [TRIKT]
        POSITION [MSPOS]
        OUTLINECOLOR [OLNCLR]
    END
    """
    exp = "LABEL FONT [FONTNAME] TYPE TRUETYPE COLOR [TXTCLR] SIZE [FONTSIZE] ANGLE [TRIKT] POSITION [MSPOS] OUTLINECOLOR [OLNCLR] END"
    assert(output(s, schema_name="label") == exp)


def test_style_geotransform():
    """
    GEOMTRANSFORM "end" (since END is used to end objects in the map file, end must be embedded in quotes)
    http://mapserver.org/mapfile/geomtransform.html#end-and-start
    """
    s = """
    STYLE
        SIZE 0
        GEOMTRANSFORM "end"
    END
    """

    print(output(s, schema_name="style"))
    exp = "STYLE SIZE 0 GEOMTRANSFORM 'end' END"
    assert(output(s, schema_name="style") == exp)


def test_font_symbol():
    """
    GEOMTRANSFORM "end" (since END is used to end objects in the map file, end must be embedded in quotes)
    http://mapserver.org/mapfile/geomtransform.html#end-and-start
    """
    s = u"""
    LABEL
        TEXT "►"
        ANGLE FOLLOW
        FONT "arial"
        TYPE TRUETYPE
    END
    """

    print(output(s, schema_name="label"))
    exp = u"LABEL TEXT '►' ANGLE FOLLOW FONT 'arial' TYPE TRUETYPE END"
    assert(output(s, schema_name="label") == exp)


def test_buffer_expression():

    s = u"""
    STYLE
        GEOMTRANSFORM (buffer([shape], 20))
    END
    """

    print(output(s, schema_name="style"))
    exp = u"STYLE GEOMTRANSFORM (buffer([shape],20)) END"
    assert(output(s, schema_name="style") == exp)


def test_multiple_layer_data():

    s = u"""
    LAYER
        TYPE POINT
        DATA "dataset1"
        DATA "dataset2"
    END
    """

    print(output(s, schema_name="layer"))
    exp = u"LAYER TYPE POINT DATA 'dataset1' DATA 'dataset2' END"
    assert(output(s, schema_name="layer") == exp)


def test_single_layer_data():

    s = u"""
    LAYER
        TYPE POINT
        DATA "dataset1"
    END
    """
    jsn = mappyfile.loads(s)
    print(json.dumps(jsn, indent=4))
    jsn["data"][0] = "dataset1"
    print(mappyfile.dumps(jsn))

    print(output(s, schema_name="layer"))
    exp = u"LAYER TYPE POINT DATA 'dataset1' END"
    assert(output(s, schema_name="layer") == exp)


def test_cluster():

    s = u"""
    LAYER
        TYPE POINT
        CLUSTER
            MAXDISTANCE 50
            REGION "ELLIPSE"
        END
    END
    """
    print(output(s, schema_name="layer"))
    exp = u"LAYER TYPE POINT CLUSTER MAXDISTANCE 50 REGION 'ELLIPSE' END END"
    assert(output(s, schema_name="layer") == exp)


def test_cluster2():
    """
    Technically this is not correct and should not parse as the region
    type should be in quotes. MapServer will throw an
    a Symbol definition error. Parsing error near (ELLIPSE)
    """
    s = u"""
    LAYER
        TYPE POINT
        CLUSTER
            MAXDISTANCE 50
            REGION ELLIPSE
        END
    END
    """
    print(output(s, schema_name="layer"))
    exp = u"LAYER TYPE POINT CLUSTER MAXDISTANCE 50 REGION 'ELLIPSE' END END"
    assert(output(s, schema_name="layer") == exp)


@pytest.mark.xfail
def test_outputformat_unquoted_keyword():

    s = u"""
    MAP
        OUTPUTFORMAT
          NAME grid
          IMAGEMODE INT16
        END
    END
    """

    print(output(s, schema_name="map"))
    exp = u"MAP OUTPUTFORMAT NAME 'grid' IMAGEMODE INT16 END END"
    assert(output(s, schema_name="map") == exp)


def test_multiple_compfilters():
    """
    See https://github.com/geographika/mappyfile/issues/150
    """

    s = u"""
    LAYER
        NAME "point-symbol-test"
        TYPE POINT
        COMPOSITE
            COMPFILTER "blacken()"
            COMPFILTER "translate(-6,-5)"
            COMPFILTER "blur(7)"
            COMPOP "soft-light"
            OPACITY 50
        END
        COMPOSITE
            OPACITY 100
        END
    END
    """

    print(output(s, schema_name="layer"))
    exp = u"LAYER NAME 'point-symbol-test' TYPE POINT COMPOSITE COMPFILTER 'blacken()' " \
    "COMPFILTER 'translate(-6,-5)' COMPFILTER 'blur(7)' COMPOP 'soft-light' OPACITY 50 END COMPOSITE OPACITY 100 END END"
    assert(output(s, schema_name="layer") == exp)


def run_tests():
    r"""
    Need to comment out the following line in C:\VirtualEnvs\mappyfile\Lib\site-packages\pep8.py
    #stdin_get_value = sys.stdin.read
    Or get AttributeError: '_ReplInput' object has no attribute 'read'
    """
    # pytest.main(["tests/test_snippets.py::test_style_pattern"])
    pytest.main(["tests/test_snippets.py"])


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    test_multiple_compfilters()
    # run_tests()
    print("Done!")
