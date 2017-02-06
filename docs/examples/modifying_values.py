import mappyfile

mapfile = mappyfile.load("./docs/examples/raster.map")

# START OF API EXAMPLE
# update the map name
mapfile["name"] = "MyNewMap"

# update the error file path in the map config section
# note key names will always need to be lower case

mapfile["config"]["ms_errorfile"] = "/ms4w/tmp/ms_error.txt"
mapfile["config"]["ON_MISSING_DATA"] = "IGNORE"

# currently will need to double-quote non-keyword properties
mapfile["web"]["metadata"]["wms_format"] = "'image/png'"

layers = mapfile["layers"]
layer = layers[0]
layer["name"] = "MyLayer"

print(mappyfile.dumps(mapfile))

# alternatively we can use the Mapfile syntax
# not currently working for CONFIG or METADATA

web = """WEB
        METADATA
            'wms_enable_request' '*'
            'wms_feature_info_mime_type' 'text/html'
            'wms_format' 'image/jpg'
        END
    END"""

web = mappyfile.loads(web)

mapfile["web"] = web
print(mappyfile.dumps(mapfile))

# END OF API EXAMPLE

'''
cfg = """
  CONFIG "PROJ_LIB" "../../bin/proj/SHARE"
  CONFIG "PROJ_DEBUG" "OFF"
  CONFIG "ON_MISSING_DATA" "IGNORE"
"""

cfg = mappyfile.loads(cfg)


md = """METADATA
            'wms_enable_request' '*'
            'wms_feature_info_mime_type' 'text/html'
            'wms_format' 'image/png'
        END"""

md = mappyfile.loads(md)
'''


