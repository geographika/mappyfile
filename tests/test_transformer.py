import json
import pytest
from mappyfile.parser import Parser
from mappyfile.transformer import MapfileToDict, MapfileTransformer


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


def test_empty_config_directive():
    """
    Check that a config dict can be added directly without
    needing to create a new dict separately
    """

    s = """
    MAP
        NAME 'ConfigMap'
    END
    """

    p = Parser()
    ast = p.parse(s)
    t = MapfileToDict()
    d = t.transform(ast)
    d["config"]["ms_errorfile"] = "stderr"
    print(json.dumps(d, indent=4))
    assert(d["config"]["ms_errorfile"] == "stderr")
    assert(d["config"]["MS_ERRORFILE"] == "stderr")


def test_metadata():

    s = """
    MAP
        METADATA
            "wms_enable_request" "*"
            "MS_ENABLE_MODES" "!*"
        END
    END
    """
    p = Parser()
    ast = p.parse(s)
    t = MapfileToDict()
    d = t.transform(ast)
    print(json.dumps(d, indent=4))
    assert(d["metadata"]["wms_enable_request"] == "*")
    assert(d["metadata"]["MS_ENABLE_MODES"] == "!*")
    assert(d["metadata"]["wms_ENABLE_request"] == "*")
    assert(d["metadata"]["MS_enable_MODES"] == "!*")


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
    print(ast.pretty())
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
            TYPE LINE
        END
        LAYER
            NAME "Layer2"
            TYPE LINE
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
    assert(d["expression"] == "( ( [val] = 'A' ) OR ( [val] = 'B' ) )")


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
    t = MapfileToDict(include_position=True)
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


def test_oneline_label():

    s = """
    label
      type truetype size 8 font "default"
    end
    """
    p = Parser()
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
        TYPE POINT
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
    t = MapfileToDict(include_position=True)
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


def test_token_positions():

    s = """
    MAP
        SIZE 600 600
        LAYER
            NAME "Test"
            TYPE POLYGON
        END
    END
    """
    p = Parser()
    ast = p.parse(s)
    t = MapfileToDict()
    d = t.transform(ast)
    print(json.dumps(d, indent=4))

    p = Parser()
    m = MapfileToDict()

    ast = p.parse(s)
    d = m.transform(ast)

    print(json.dumps(d, indent=4))


def test_kwargs():

    m = MapfileToDict(custom_param="custom")
    assert "custom_param" in m.kwargs


def test_custom_transformer():
    """
    Check a custom transformer can be used with MapfileToDict, and any custom
    parameters can be passed on to this transformer (useful for plugins)
    """

    class CustomTransformer(MapfileTransformer):

        def __init__(self, include_position=False, include_comments=False, **kwargs):
            self.custom_param = kwargs["custom_param"]
            super(CustomTransformer, self).__init__(include_position, include_comments)

    m = MapfileToDict(transformerClass=CustomTransformer, custom_param="custom")

    s = """
    MAP
        SIZE 600 600
        LAYER
            NAME "Test"
            TYPE POLYGON
        END
    END
    """
    p = Parser()
    ast = p.parse(s)

    d = m.transform(ast)
    print(d)
    assert m.mapfile_transformer.__class__.__name__ == "CustomTransformer"
    assert m.mapfile_transformer.custom_param == "custom"


def run_tests():
    # pytest.main(["tests/test_transformer.py::test_config_directive"])
    pytest.main(["tests/test_transformer.py"])


if __name__ == '__main__':
    # test_custom_transformer()
    run_tests()
    print("Done!")
