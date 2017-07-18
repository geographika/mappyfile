import mappyfile
import json
mf = mappyfile.load("./docs/examples/after.map")

with open("./docs/examples/sample.json", "w") as f:
    json.dump(mf, f, indent=4)

s = """
MAP
    NAME "sample"
    STATUS ON
    SIZE 600 400
    SYMBOLSET "../etc/symbols.txt"
    EXTENT -180 -90 180 90
    UNITS DD
    SHAPEPATH "../data"
    IMAGECOLOR 255 255 255
    FONTSET "../etc/fonts.txt"

    #
    # Start of web interface definition
    #
    WEB
        IMAGEPATH "/ms4w/tmp/ms_tmp/"
        IMAGEURL "/ms_tmp/"
    END # WEB

    #
    # Start of layer definitions
    #
    LAYER
        NAME 'global-raster'
        TYPE RASTER
        STATUS DEFAULT
        DATA bluemarble.gif
    END # LAYER
END # MAP
"""
mf = mappyfile.loads(s)
jsn = json.dumps(mf, indent=4)
print(jsn)