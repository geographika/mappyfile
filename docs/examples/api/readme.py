import mappyfile

mapfile = mappyfile.open("./docs/examples/raster.map")

# update the map name
mapfile["name"] = "MyNewMap"

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

layers = mapfile["layers"]

new_layer = mappyfile.loads(new_layer_string)

layers.insert(0, new_layer)  # insert the new layer at any index in the Mapfile

for lyr in layers:
    print("{} {}".format(lyr["name"], lyr["type"]))

print(mappyfile.dumps(mapfile, indent=1, spacer="\t"))
