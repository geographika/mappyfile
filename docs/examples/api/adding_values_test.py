import mappyfile

mapfile = mappyfile.open("./docs/examples/raster.map")


def test_layer():
    # START OF ADD LAYER EXAMPLE
    layers = mapfile["layers"]

    new_layer_string = """
    LAYER
        NAME 'land'
        TYPE POLYGON
        DATA '../data/vector/naturalearth/ne_110m_land'
        CLASS
            STYLE
                COLOR 107 208 107
                OUTLINECOLOR 2 2 2
                WIDTH 1
            END
        END
    END
    """

    new_layer = mappyfile.loads(new_layer_string)
    layers.insert(0, new_layer)  # can insert the new layer at any index
    # END OF ADD LAYER EXAMPLE
    assert layers[0]["name"] == "land"


def test_class():
    # START OF ADD CLASS EXAMPLE
    # find a layer using its name
    layer = mappyfile.find(mapfile["layers"], "name", "sea")

    new_class_string = """
    CLASS
        NAME 'highlights'
        STYLE
            COLOR 107 208 107
            OUTLINECOLOR 2 2 2
            WIDTH 1
        END
    END
    """

    new_class = mappyfile.loads(new_class_string)
    layer["classes"].insert(1, new_class)  # can insert the new class at any index
    print(mappyfile.dumps(mapfile))

    # END OF ADD CLASS EXAMPLE
    assert layer["classes"][1]["name"] == "highlights"

    # multiple classes
    # define all classes in a single string TODO - allow on single line
    classes = """
    CLASS
        NAME 'The World'
        STYLE
        OUTLINECOLOR 0 255 0
        END
    END
    CLASS
        NAME 'Roads'
        STYLE
        OUTLINECOLOR 0 0 0
        END
    END
    """
    # parse the string and replace the existing classes for the layer
    layer["classes"] = mappyfile.loads(classes)
    print(mappyfile.dumps(mapfile))


if __name__ == "__main__":
    test_layer()
    test_class()
