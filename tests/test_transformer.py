import json
import pytest
from mappyfile.parser import Parser
from mappyfile.transformer import MapfileToDict
from mappyfile.ordereddict import DefaultOrderedDict
# from lark.lexer import Token
# from lark.tree import Tree


def test_processing_directive():

    s = """
    LAYER
        NAME 'ProcessingLayer'
        PROCESSING 'BANDS=1'
        PROCESSING 'CONTOUR_ITEM=elevation'
        PROCESSING 'CONTOUR_INTERVAL=20'
    END
    """

    p = Parser()
    ast = p.parse(s)
    t = MapfileToDict()
    d = t.transform(ast)
    print(json.dumps(d, indent=4))
    assert(len(d["processing"]) == 3)


def test_config_directive():

    s = """
    MAP
        NAME 'ConfigMap'
        CONFIG MS_ERRORFILE "stderr"
        CONFIG "PROJ_DEBUG" "OFF"
        CONFIG "ON_MISSING_DATA" "IGNORE"
    END
    """

    p = Parser()
    ast = p.parse(s)
    t = MapfileToDict()
    d = t.transform(ast)
    print(json.dumps(d, indent=4))
    assert(len(d["config"]) == 3)


def test_metadata():

    s = """
    MAP
        METADATA
            "wms_enable_request" "*"
            "ms_enable_modes" "!*"
        END
    END
    """
    p = Parser()
    ast = p.parse(s)
    t = MapfileToDict()
    d = t.transform(ast)
    print(json.dumps(d, indent=4))
    assert(d["metadata"]["wms_enable_request"] == "*")


def test_metadata_dict():

    vals = [['wms_enable_request', '*'], ['ms_enable_modes', '!*']]
    t = MapfileToDict()
    res = t.metadata(vals)
    assert(res[0] == 'composite')
    assert(res[1] == 'metadata')
    assert(len(res[2].items()) == 2)


def test_scaletoken():

    s = """
    SCALETOKEN
        NAME "%border%"
        VALUES
            "0" "ON"
            "255000000" "OFF"
        END
    END
    """

    p = Parser()
    ast = p.parse(s)
    t = MapfileToDict()
    d = t.transform(ast)
    print(d)
    print(json.dumps(d, indent=4))
    # print(dict(d["metadata"]))
    assert(d["__type__"] == "scaletoken")
    assert(d["values"]["0"] == "ON")


def test_layerlist():

    s = """
    MAP
        LAYER
            NAME "Layer1"
        END
        LAYER
            NAME "Layer2"
        END
    END
    """

    p = Parser()
    ast = p.parse(s)
    t = MapfileToDict()
    d = t.transform(ast)
    print(d)
    print(json.dumps(d, indent=4))
    # print(dict(d["metadata"]))
    assert(len(d["layers"]) == 2)
    assert(d["layers"][0]["name"] == "Layer1")


def test_config_settings():

    d = DefaultOrderedDict(DefaultOrderedDict)
    t = MapfileToDict()
    t.config_settings(d, "config", ["MS_NONSQUARE", "YES"])
    t.config_settings(d, "config", ["ON_MISSING_DATA", "FAIL"])
    print(json.dumps(d, indent=4))
    assert(len(d["config"].items()) == 2)
    assert(d["config"]["on_missing_data"] == "FAIL")


def test_expression():

    s = """
    CLASS
        TEXT ([area])
        EXPRESSION ([area])
    END
    CLASS
        TEXT ("[area]")
        EXPRESSION ("[area]")
    END
    """
    p = Parser()
    ast = p.parse(s)
    t = MapfileToDict()
    d = t.transform(ast)
    print(d)
    print(json.dumps(d, indent=4))
    assert(d[0]["text"] == "([area])")
    assert(d[0]["expression"] == "([area])")
    assert(d[1]["text"] == "(\"[area]\")")
    assert(d[1]["expression"] == "(\"[area]\")")


def test_or_expression():

    s = """
    CLASS
        EXPRESSION (([val] = 'A') OR ([val] = 'B'))
    END
    """
    p = Parser()
    ast = p.parse(s)
    t = MapfileToDict()
    d = t.transform(ast)
    print(d)
    print(json.dumps(d, indent=4))
    assert(d["expression"] == "( ( [val] = 'A' ) or ( [val] = 'B' ) )")


def test_projection():

    s = """
    MAP
        PROJECTION
            "proj=utm"
            "ellps=GRS80"
            "datum=NAD83"
            "zone=15"
            "units=m"
            "north"
            "no_defs"
        END
    END
    """
    p = Parser()
    ast = p.parse(s)
    t = MapfileToDict()
    d = t.transform(ast)
    print(json.dumps(d, indent=4))
    assert(len(d["projection"]) == 7)


def test_auto_projection():

    s = """
    MAP
        PROJECTION
            AUTO
        END
    END
    """
    p = Parser()
    ast = p.parse(s)
    t = MapfileToDict()
    d = t.transform(ast)
    print(json.dumps(d, indent=4))
    assert(len(d["projection"]) == 1)


def test_points():

    s = """
    FEATURE
        POINTS 1 1 50 50 1 50 1 1 END
        POINTS 100 100 50 50 100 50 100 100 END
    END
    """
    p = Parser()
    ast = p.parse(s)
    t = MapfileToDict()
    d = t.transform(ast)
    print(json.dumps(d, indent=4))
    assert(len(d["points"]) == 2)
    assert(len(d["points"][0]) == 4)
    assert(len(d["points"][0][0]) == 2)
    assert(d["points"][0][0][0] == 1)


def test_pattern():

    s = """
    STYLE
        PATTERN 10 1 50 50 1 50 1 1 END
    END
    """
    p = Parser()
    ast = p.parse(s)
    t = MapfileToDict()
    d = t.transform(ast)
    print(json.dumps(d, indent=4))
    assert(len(d["pattern"]) == 4)
    assert(len(d["pattern"][0]) == 2)
    assert(d["pattern"][0][0] == 10)


@pytest.mark.xfail
def test_oneline_label():

    s = """
    label
      type truetype size 8 font "default"
    end
    """
    p = Parser(use_lalr=True)
    ast = p.parse(s)
    t = MapfileToDict()
    d = t.transform(ast)
    print(json.dumps(d, indent=4))
    assert(d["type"] == "truetype")
    assert(d["size"] == 8)
    assert(d["font"] == "default")
    assert(d["__type__"] == "label")


def test_boolean():

    s = """
    LAYER
        TRANSFORM TRUE
    END
    """
    p = Parser()
    ast = p.parse(s)
    t = MapfileToDict()
    d = t.transform(ast)
    print(json.dumps(d, indent=4))
    assert(d["transform"])


@pytest.mark.xfail
def test_multiple_layer_projection():
    """
    TODO add validation for this case
    """

    s = """
    MAP
    LAYER
        PROJECTION
            "init=epsg:4326"
            "init=epsg:4326"
        END
        PROJECTION
            "init=epsg:4326"
            "init=epsg:4326"
        END
    END
    END
    """
    p = Parser()
    ast = p.parse(s)
    t = MapfileToDict()
    d = t.transform(ast)
    print(json.dumps(d, indent=4))
    assert(len(d["projection"]) == 1)

    p = Parser()
    m = MapfileToDict()

    ast = p.parse(s)
    d = m.transform(ast)

    print(json.dumps(d, indent=4))

    from mappyfile.validator import Validator
    v = Validator()
    return v.validate(d)


def run_tests():
    # pytest.main(["tests/test_transformer.py::test_config_directive"])
    pytest.main(["tests/test_transformer.py"])


if __name__ == '__main__':
    run_tests()
    # test_multiple_layer_projection()
    print("Done!")
