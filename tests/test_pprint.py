# -*- coding: utf-8 -*-
import pytest
from mappyfile.pprint import PrettyPrinter
import mappyfile

def test_nested_quotes():
    """
    If values contain quotes then make sure they are escaped
    shp2img -m C:\Temp\msautotest\misc\ogr_vrtconnect.tmp.map    
    """
    s = """
    LAYER
        NAME shppoly
        TYPE polygon
        CONNECTIONTYPE OGR
        CONNECTION '<OGRVRTDataSource><OGRVRTLayer name="poly"><SrcDataSource relativeToVRT="0">data/shppoly</SrcDataSource><SrcLayer>poly</SrcLayer></OGRVRTLayer></OGRVRTDataSource>'
    END"""

    ast = mappyfile.loads(s)
    pp = PrettyPrinter(indent=0, quote='"', newlinechar=" ") # expected
    res = pp.pprint(ast)
    exp = r'LAYER NAME shppoly TYPE polygon CONNECTIONTYPE OGR CONNECTION "<OGRVRTDataSource><OGRVRTLayer name=\"poly\">' \
        r'<SrcDataSource relativeToVRT=\"0\">data/shppoly</SrcDataSource><SrcLayer>poly</SrcLayer></OGRVRTLayer></OGRVRTDataSource>" END'
    assert(res == exp)

def test_standardise_quotes():

    v = '"the_geom from (select * from road where "name_e"=\'Trans-Canada Highway\' order by gid) as foo using unique gid using srid=3978"'

    pp = PrettyPrinter(indent=0, quote='"', newlinechar=" ") # expected
    v2 = pp.standardise_quotes(v)
    exp = r'''"the_geom from (select * from road where \"name_e\"='Trans-Canada Highway' order by gid) as foo using unique gid using srid=3978"'''
    assert(v2 == exp)

    pp = PrettyPrinter(indent=0, quote="'", newlinechar=" ") # expected
    v2 = pp.standardise_quotes(v)
    exp = r"""'the_geom from (select * from road where "name_e"=\'Trans-Canada Highway\' order by gid) as foo using unique gid using srid=3978'"""
    assert(v2 == exp)

def test_double_attributes():

    s = 'MAP CONFIG "MS_ERRORFILE" "stderr" END'
    ast = mappyfile.loads(s)
    pp = PrettyPrinter(indent=0, quote='"', newlinechar=" ")
    res = pp.pprint(ast)
    assert(res == 'MAP CONFIG "MS_ERRORFILE" "stderr" END')

    s = 'MAP CONFIG "MS_ERRORFILE" "stderr" END'
    ast = mappyfile.loads(s)
    pp = PrettyPrinter(indent=0, quote="'", newlinechar=" ") # expected
    res = pp.pprint(ast)
    assert(res == "MAP CONFIG 'MS_ERRORFILE' 'stderr' END")
        
def test_already_escaped():
    """
    Don't escape an already escaped quote
    """
    s = r'CLASS EXPRESSION "\"Tignish" END'
    ast = mappyfile.loads(s)
    pp = PrettyPrinter(indent=0, quote='"', newlinechar=" ")
    res = pp.pprint(ast)
    exp = r'CLASS EXPRESSION "\"Tignish" END'
    assert(res == exp)

    s = r"CLASS EXPRESSION '\'Tignish' END"
    ast = mappyfile.loads(s)
    pp = PrettyPrinter(indent=0, quote="'", newlinechar=" ")
    res = pp.pprint(ast)
    exp = r"CLASS EXPRESSION '\'Tignish' END"
    assert(res == exp)

def test_format_list():

    s = """
        CLASS
            STYLE
                COLOR 173 216 230
            END
            STYLE
                OUTLINECOLOR 2 2 2
                WIDTH 1
                LINECAP BUTT
                PATTERN
                    5 5
                    10 10
                END
            END
        END
    """

    ast = mappyfile.loads(s)
    pp = PrettyPrinter(indent=0) # expected

    k = "pattern"
    lst = [[5, 5, 10, 10]]

    assert(pp.is_paired_list(k))
    r = pp.process_list(k, lst, 0)
    exp = [u'PATTERN', '5 5\n10 10', u'END']
    assert(r == exp)

def test_unicode():

    s = u"""
    MAP
        METADATA
          "ows_title" "éúáí"
        END
    END
    """
    ast = mappyfile.loads(s)
    pp = PrettyPrinter(indent=0, quote="'", newlinechar=" ")
    res = pp.pprint(ast)
    exp = u"MAP METADATA 'ows_title' 'éúáí' END END"
    assert(res == exp)

def test_config():

    s = """
    MAP
        config "MS_ERRORFILE" "my.log"
    END
    """
    ast = mappyfile.loads(s)
    pp = PrettyPrinter(indent=0, quote="'", newlinechar=" ")
    res = pp.pprint(ast)
    print res
    exp = u"MAP CONFIG 'MS_ERRORFILE' 'my.log' END"
    assert(res == exp)

def run_tests():        
    #pytest.main(["tests/test_pprint.py::test_format_list"])
    pytest.main(["tests/test_pprint.py"])

if __name__ == "__main__":
    run_tests()
    #test_config()
    print("Done!")
