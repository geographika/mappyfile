import mappyfile

mapfile = mappyfile.load("./docs/examples/raster.map")

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
layers.insert(0, new_layer) # can insert the new layer at any index

# END OF ADD LAYER EXAMPLE
# START OF ADD CLASS EXAMPLE
layer = mappyfile.find(mapfile["layers"], "name", "highlighted")

new_class_string = """
CLASS
    STYLE
        COLOR 107 208 107
        OUTLINECOLOR 2 2 2
        WIDTH 1
    END
END
"""

new_class = mappyfile.loads(new_class_string)
layer["classes"].insert(1, new_class) # can insert the new class at any index
# END OF ADD CLASS EXAMPLE

# START OF MULTIPLE ADD EXAMPLE
layer = mapfile["layers"][1]

# multiple objects cannot be parsed
new_class_string = """
CLASS
    STYLE
            COLOR 107 208 107
            OUTLINECOLOR 2 2 2
            WIDTH 1
    END
    STYLE
            COLOR 99 231 117
            OUTLINECOLOR 2 2 2
            WIDTH 1
    END	
END
"""

new_class = mappyfile.loads(new_class_string)
#layer["classes"].insert(1, new_styles) # can insert the new class at any index
layer["classes"] = new_class # can insert the new class at any index

# END OF MULTIPLE ADD EXAMPLE