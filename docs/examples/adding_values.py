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
assert(layers[0]['name'] == 'land')
# END OF ADD LAYER EXAMPLE
# START OF ADD CLASS EXAMPLE
# find a layer using its name
layer = mappyfile.find(mapfile["layers"], "name", "highlighted")

new_class_string = """
CLASS
    NAME "highlights"
    STYLE
        COLOR 107 208 107
        OUTLINECOLOR 2 2 2
        WIDTH 1
    END
END
"""

new_class = mappyfile.loads(new_class_string)
layer["classes"].insert(1, new_class) # can insert the new class at any index
assert(layer['classes'][1]['name'] == 'land')

print(mappyfile.dumps(mapfile))
# END OF ADD CLASS EXAMPLE