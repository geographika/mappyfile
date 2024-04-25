import logging
import mappyfile
import pytest


def test_find():
    s = """
    MAP
        LAYER
            NAME "Layer1"
            TYPE POLYGON
        END
        LAYER
            NAME "Layer2"
            TYPE POLYGON
            CLASS
                NAME "Class1"
                COLOR 0 0 -8
            END
        END
    END
    """

    d = mappyfile.loads(s)
    cmp = mappyfile.find(d["layers"], "name", "Layer2")

    assert cmp is not None
    assert cmp["name"] == "Layer2"


def test_findkey():
    s = """
    MAP
        LAYER
            NAME "Layer1"
            TYPE POLYGON
        END
        LAYER
            NAME "Layer2"
            TYPE POLYGON
            CLASS
                NAME "Class1"
                COLOR 0 0 -8
            END
        END
    END
    """

    d = mappyfile.loads(s)

    pth = ["layers", 1]
    cmp = mappyfile.findkey(d, *pth)  # type: ignore
    assert cmp["name"] == "Layer2"

    pth = ["layers", 1, "classes", 0]
    cmp = mappyfile.findkey(d, *pth)  # type: ignore
    assert cmp["name"] == "Class1"


def test_findall():
    s = """
    MAP
        LAYER
            NAME "Layer1"
            TYPE POLYGON
            GROUP "test"
        END
        LAYER
            NAME "Layer2"
            TYPE POLYGON
            GROUP "1test"
        END
        LAYER
            NAME "Layer3"
            TYPE POLYGON
            GROUP "test2"
        END
        LAYER
            NAME "Layer4"
            TYPE POLYGON
            GROUP "test"
        END
    END
    """

    d = mappyfile.loads(s)
    layers = mappyfile.findall(d["layers"], "group", "test")
    assert len(layers) == 2
    assert layers[0]["name"] == "Layer1"


def test_findall_missing_value():
    s = """
    MAP
        LAYER
            NAME "Layer1"
            TYPE POLYGON
            GROUP "test"
        END
        LAYER
            NAME "Layer2"
            TYPE POLYGON
            GROUP "1test"
        END
        LAYER
            NAME "Layer3"
            TYPE POLYGON
            GROUP "test2"
        END
        LAYER
            NAME "Layer4"
            TYPE POLYGON
            # GROUP "test"
        END
    END
    """

    d = mappyfile.loads(s)
    layers = mappyfile.findall(d["layers"], "group", "test")
    assert len(layers) == 1
    assert layers[0]["name"] == "Layer1"


def test_findall_itasca():
    fn = "./tests/mapfiles/itasca2.map"
    d = mappyfile.open(fn)
    layers = mappyfile.findall(d["layers"], "group", "roads")
    assert len(layers) == 4
    assert layers[0]["name"] == "ctyrdln3"


def test_findall_itasca2():
    fn = "./tests/mapfiles/itasca2.map"
    d = mappyfile.open(fn)
    layers = mappyfile.findall(d["layers"], "type", "POINT")
    assert len(layers) == 2
    assert layers[0]["name"] == "airports"


def test_update():
    s1 = """
    MAP
        LAYER
            NAME "Layer1"
            TYPE POLYGON
        END
        LAYER
            NAME "Layer2"
            TYPE POLYGON
            CLASS
                NAME "Class1"
                COLOR 255 255 0
            END
        END
    END
    """

    d1 = mappyfile.loads(s1)

    s2 = """
    MAP
        LAYER
            NAME "Layer1"
            TYPE POLYGON
        END
        LAYER
            NAME "LayerNew"
            TYPE POINT
            CLASS
                NAME "Class1"
                COLOR 0 0 255
            END
            CLASS
                NAME "Class2"
                COLOR 0 0 0
            END
        END
    END
    """

    d2 = mappyfile.loads(s2)
    d = mappyfile.update(d1, d2)

    output = mappyfile.dumps(d)

    expected = """MAP
    LAYER
        NAME "Layer1"
        TYPE POLYGON
    END
    LAYER
        NAME "LayerNew"
        TYPE POINT
        CLASS
            NAME "Class1"
            COLOR 0 0 255
        END
        CLASS
            NAME "Class2"
            COLOR 0 0 0
        END
    END
END"""

    assert output == expected


def test_update_no_overrides():
    s1 = """
    MAP
        LAYER
            NAME "Layer1"
            TYPE POLYGON
        END
        LAYER
            NAME "Layer2"
            TYPE POLYGON
            CLASS
                NAME "Class1"
                COLOR 255 255 0
            END
        END
    END
    """

    d1 = mappyfile.loads(s1)

    s2 = """
    MAP
        LAYER
            NAME "Layer1"
            TYPE POLYGON
        END
        LAYER
            NAME "LayerNew"
            TYPE POINT
            CLASS
                NAME "ClassNew"
                COLOR 0 0 255
                GROUP "group1"
            END
            CLASS
                NAME "Class2"
                COLOR 0 0 0
                GROUP "group2"
            END
        END
    END
    """

    d2 = mappyfile.loads(s2)
    d = mappyfile.update(d1, d2, overwrite=False)

    output = mappyfile.dumps(d)

    expected = """MAP
    LAYER
        NAME "Layer1"
        TYPE POLYGON
    END
    LAYER
        NAME "Layer2"
        TYPE POLYGON
        CLASS
            NAME "Class1"
            COLOR 255 255 0
            GROUP "group1"
        END
        CLASS
            NAME "Class2"
            COLOR 0 0 0
            GROUP "group2"
        END
    END
END"""

    assert output == expected


def test_update_list():
    d1 = {
        "__type__": "layer",
        "name": "Unrated",
        "styles": [{"__type__": "style", "color": "#888888"}],
    }
    d2 = {"name": "Unrated", "styles": [{"color": [255, 255, 0]}]}
    d = mappyfile.update(d1, d2)
    output = mappyfile.dumps(d)
    print(output)
    assert d["styles"][0]["color"] == [255, 255, 0]


def test_update_list_second_item():
    # test that a None type can be passed
    d1 = {
        "__type__": "layer",
        "name": "Unrated",
        "styles": [
            {"__type__": "style", "color": "#888888"},
            {"__type__": "style", "color": "#888888"},
        ],
    }
    d2 = {"name": "Unrated", "styles": [None, {"color": [255, 255, 0]}]}
    d = mappyfile.update(d1, d2)
    output = mappyfile.dumps(d)
    print(output)
    assert d["styles"][1]["color"] == [255, 255, 0]


def test_update_delete():
    d1 = {
        "__type__": "layer",
        "name": "Unrated",
        "styles": [{"__type__": "style", "color": "#888888"}],
    }
    d2 = {"name": "Unrated", "styles": [{"__delete__": True}]}
    d = mappyfile.update(d1, d2)
    output = mappyfile.dumps(d)
    print(output)
    assert len(d["styles"]) == 0


def test_update_delete_dict():
    d1 = {
        "__type__": "layer",
        "name": "Unrated",
        "metadata": {"__type__": "metadata", "key1": "val1"},
    }
    print(mappyfile.dumps(d1))
    d2 = {"metadata": {"__delete__": True}}
    d = mappyfile.update(d1, d2)
    output = mappyfile.dumps(d)
    print(output)
    assert "metadata" not in d.keys()


def test_update_delete_root_object():
    d1 = {
        "__type__": "layer",
        "name": "Unrated",
        "styles": [{"__type__": "style", "color": "#888888"}],
    }
    d2 = {"__delete__": True}
    d = mappyfile.update(d1, d2)
    output = mappyfile.dumps(d)
    assert output == ""


def test_update_add_item():
    d1 = {
        "__type__": "layer",
        "name": "Unrated",
        "styles": [{"__type__": "style", "color": "#888888"}],
    }
    d2 = {
        "name": "Unrated",
        "styles": [None, {"__type__": "style", "color": [0, 0, 255]}],
    }
    d = mappyfile.update(d1, d2)
    output = mappyfile.dumps(d)
    print(output)
    assert d["styles"][1]["color"] == [0, 0, 255]


def test_findunique():
    s = """
    LAYER
        CLASS
            GROUP "group1"
            NAME "Class1"
            COLOR 0 0 -8
        END
        CLASS
            GROUP "group2"
            NAME "Class2"
            COLOR 0 0 0
        END
        CLASS
            GROUP "group1"
            NAME "Class3"
            COLOR 0 0 0
        END
    END
    """

    d = mappyfile.loads(s)
    groups = mappyfile.findunique(d["classes"], "group")
    assert groups == ["group1", "group2"]

    groups = mappyfile.findunique(d["classes"], "non-existent")
    assert groups == []


def run_tests():
    pytest.main(["tests/test_dictutils.py"])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # run_tests()
    test_findall_missing_value()
    test_findall_itasca2()
    print("Done!")
