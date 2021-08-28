# -*- coding: utf-8 -*-
"""
To check

+ styleitem auto - should be capitalised (layer)
+ Each of the units is different - [pixels|feet|inches|kilometers|meters|miles|nauticalmiles|dd] - standardise
"""
import logging
import json
import collections
import pytest
from mappyfile.parser import Parser
from mappyfile.pprint import PrettyPrinter, Quoter
from mappyfile.transformer import MapfileToDict
import mappyfile


def test_nested_quotes():
    r"""
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
    pp = PrettyPrinter(indent=0, quote='"', newlinechar=" ")  # expected
    res = pp.pprint(ast)
    print(res)
    exp = 'LAYER NAME "shppoly" TYPE POLYGON CONNECTIONTYPE OGR CONNECTION "<OGRVRTDataSource><OGRVRTLayer name="poly">' \
    '<SrcDataSource relativeToVRT="0">data/shppoly</SrcDataSource><SrcLayer>poly</SrcLayer></OGRVRTLayer></OGRVRTDataSource>" END'
    assert(res == exp)


def test_standardise_quotes():

    v = '"the_geom from (select * from road where "name_e"=\'Trans-Canada Highway\' order by gid) as foo using unique gid using srid=3978"'

    q = Quoter(quote='"')
    v2 = q.standardise_quotes(v)
    exp = r'''"the_geom from (select * from road where \"name_e\"='Trans-Canada Highway' order by gid) as foo using unique gid using srid=3978"'''
    assert(v2 == exp)

    q = Quoter(quote="'")
    v2 = q.standardise_quotes(v)
    exp = r"""'the_geom from (select * from road where "name_e"=\'Trans-Canada Highway\' order by gid) as foo using unique gid using srid=3978'"""
    assert(v2 == exp)


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


def test_enumeration():
    s = """
    MAP
        EXTENT 0 0 100 100
        DEBUG on
        NAME Test
        shapepath "test/path"
        LAYER
            CLASSITEM "Test"
            CLASS
                EXPRESSION "Field"
                STYLE
                    SIZE [sizefield]
                END
            END
        END
    END
    """
    p = Parser()
    m = MapfileToDict()
    ast = p.parse(s)
    d = m.transform(ast)
    print(d)
    logging.debug(json.dumps(d, indent=4))
    pp = PrettyPrinter(indent=4, quote="'", newlinechar="\n")
    res = pp.pprint(d)
    print(res)


def test_points():

    d = {
    "points": [[[1,
                1],
            [50,
                50],
            [1,
                50],
            [1,
                1]],
            [[100,
                100],
            [50,
                50],
            [100,
                50],
            [100,
                100]]],
    "__type__": "feature"
    }

    pp = PrettyPrinter(indent=0, quote="'", newlinechar=" ")
    s = pp.pprint(d)
    print(s)
    assert(s == "FEATURE POINTS 1 1 50 50 1 50 1 1 END POINTS 100 100 50 50 100 50 100 100 END END")


def test_style_pattern():

    d = {
        "pattern": [[10,
                1],
            [50,
                50],
            [1,
                50],
            [1,
                1]],
        "__type__": "style"
    }

    pp = PrettyPrinter(indent=0, quote="'", newlinechar=" ")
    s = pp.pprint(d)
    assert(s == "STYLE PATTERN 10 1 50 50 1 50 1 1 END END")


def test_scaletoken():

    sd = {
        "0": "ON",
        "255000000": "OFF"
    }

    sd = collections.OrderedDict(sorted(sd.items()))

    d = {
    "name": "%border%",
    "values": sd,
    "__type__": "scaletoken"
    }

    d = collections.OrderedDict(sorted(d.items()))

    pp = PrettyPrinter(indent=0, quote="'", newlinechar=" ")
    s = pp.pprint(d)
    print(s)
    assert(s == "SCALETOKEN NAME '%border%' VALUES '0' 'ON' '255000000' 'OFF' END END")


def test_metadata():

    md = {
            "MS_ENABLE_MODES": "!*",
            "WMS_ENABLE_REQUEST": "*"
        }

    md = collections.OrderedDict(sorted(md.items()))

    d = {
        "metadata": md,
        "__type__": "map"
    }

    d = collections.OrderedDict(sorted(d.items()))

    pp = PrettyPrinter(indent=0, quote="'", newlinechar=" ")
    s = pp.pprint(d)
    print(s)
    assert(s == "MAP METADATA 'MS_ENABLE_MODES' '!*' 'WMS_ENABLE_REQUEST' '*' END END")


def test_connectionoptions():

    values = {
            "FLATTEN_NESTED_ATTRIBUTES": "YES"
        }

    d = {
        "connectionoptions": values,
        "__type__": "layer"
    }

    d = collections.OrderedDict(sorted(d.items()))

    pp = PrettyPrinter(indent=0, quote="'", newlinechar=" ")
    s = pp.pprint(d)
    print(s)
    assert(s == "LAYER CONNECTIONOPTIONS 'FLATTEN_NESTED_ATTRIBUTES' 'YES' END END")


def test_config():

    cd = {
            "ms_nonsquare": "YES",
            "on_missing_data": "FAIL"
          }

    cd = collections.OrderedDict(sorted(cd.items()))

    d = {
        "config": cd,
        "__type__": "map"
    }

    d = collections.OrderedDict(sorted(d.items()))

    pp = PrettyPrinter(indent=0, quote="'", newlinechar=" ")
    s = pp.pprint(d)
    print(s)
    assert(s == "MAP CONFIG 'MS_NONSQUARE' 'YES' CONFIG 'ON_MISSING_DATA' 'FAIL' END")


def test_processing():
    d = {
    "name": "ProcessingLayer",
    "processing": ["BANDS=1",
        "CONTOUR_ITEM=elevation",
        "CONTOUR_INTERVAL=20"],
    "__type__": "layer"
    }

    d = collections.OrderedDict(sorted(d.items()))

    pp = PrettyPrinter(indent=0, quote="'", newlinechar=" ")
    s = pp.pprint(d)
    print(s)
    assert(s == "LAYER NAME 'ProcessingLayer' PROCESSING 'BANDS=1' PROCESSING 'CONTOUR_ITEM=elevation' PROCESSING 'CONTOUR_INTERVAL=20' END")


def test_multiple_layers():
    d = {
    "layers": [{
            "name": "Layer1",
            "__type__": "layer"
        },
        {
            "name": "Layer2",
            "__type__": "layer"
        }],
    "__type__": "map"
    }

    pp = PrettyPrinter(indent=0, quote="'", newlinechar=" ")
    s = pp.pprint(d)
    print(s)
    assert(s == "MAP LAYER NAME 'Layer1' END LAYER NAME 'Layer2' END END")


def test_projection():
    d = {
    "projection": ["proj=utm",
        "ellps=GRS80",
        "datum=NAD83",
        "zone=15",
        "units=m",
        "north",
        "no_defs"],
    "__type__": "map"
    }

    pp = PrettyPrinter(indent=0, quote="'", newlinechar=" ")
    s = pp.pprint(d)
    print(s)
    assert(s == "MAP PROJECTION 'proj=utm' 'ellps=GRS80' 'datum=NAD83' 'zone=15' 'units=m' 'north' 'no_defs' END END")


def test_auto_projection():
    d = {
    "projection": ["auto"],
    "__type__": "map"
    }

    pp = PrettyPrinter(indent=0, quote="'", newlinechar=" ")
    s = pp.pprint(d)
    print(s)
    assert(s == "MAP PROJECTION AUTO END END")


def test_single_string_projection():
    d = {
    "projection": "init=epsg:4326",
    "__type__": "map"
    }

    pp = PrettyPrinter(indent=0, quote="'", newlinechar=" ")
    s = pp.pprint(d)
    print(s)
    assert(s == "MAP PROJECTION 'init=epsg:4326' END END")


def test_print_boolean():
    d = {
        "transform": True,
        "__type__": "layer"
    }

    pp = PrettyPrinter(indent=0, quote="'", newlinechar=" ")
    s = pp.pprint(d)
    print(s)
    assert(s == "LAYER TRANSFORM TRUE END")


def test_join():
    d = {
        "__type__": "layer",
        "name": "Joined",
        "joins": [{
            "__type__": "join",
            "name": "table_join"
        }]
        }

    pp = PrettyPrinter(indent=0, quote="'", newlinechar=" ")
    d = collections.OrderedDict(sorted(d.items()))
    s = pp.pprint(d)
    assert(s == "LAYER JOIN NAME 'table_join' END NAME 'Joined' END")


def test_class_list():

    d1 = {
            "text": "([area])",
            "expression": "([area])",
            "__type__": "class"
         }
    d2 = {
            "text": "(\"[area]\")",
            "expression": "(\"[area]\")",
            "__type__": "class"
         }

    d1 = collections.OrderedDict(sorted(d1.items()))
    d2 = collections.OrderedDict(sorted(d2.items()))

    classes = [d1, d2]

    pp = PrettyPrinter(indent=0, quote="'", newlinechar=" ")
    s = pp.pprint(classes)
    print(s)
    assert(s == 'CLASS EXPRESSION ([area]) TEXT ([area]) END CLASS EXPRESSION ("[area]") TEXT ("[area]") END')


def test_get_attribute_properties():
    pp = PrettyPrinter()
    props = pp.get_attribute_properties("layer", "connectiontype")
    print(props)
    assert(len(props["enum"]) == 14)


def test_get_ref_attribute_properties():
    pp = PrettyPrinter()
    props = pp.get_attribute_properties("layer", "labelcache")
    print(props)
    assert(len(props["enum"]) == 2)


def test_get_label_shadowcolor_properties():
    # check a single ref is resolved
    pp = PrettyPrinter()
    props = pp.get_attribute_properties("label", "shadowcolor")
    print(props)
    assert(len(props["oneOf"]) == 2)


def test_get_label_position_properties():
    pp = PrettyPrinter()
    props = pp.get_attribute_properties("label", "position")
    assert(props["oneOf"][1]["enum"] == [u'ul', u'uc', u'ur', u'cl', u'cc', u'cr', u'll', u'lc', u'lr'])


def test_map_layers_props():
    pp = PrettyPrinter()
    props = pp.get_attribute_properties("map", "layers")
    print(props)
    # assert(props["type"] == "object")
    assert(props["type"] == "array")


def test_end_comment():
    s = "MAP LAYER TYPE POINT NAME 'Test' END END"
    ast = mappyfile.loads(s)
    pp = PrettyPrinter(indent=4, quote='"', newlinechar="\n", end_comment=True)
    res = pp.pprint(ast)
    print(res)
    exp = """MAP
    LAYER
        TYPE POINT
        NAME "Test"
    END # LAYER
END # MAP"""
    assert res == exp


def run_tests():
    # pytest.main(["tests/test_pprint.py::test_format_list"])
    pytest.main(["tests/test_pprint.py"])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_connectionoptions()
    # run_tests()
    print("Done!")
