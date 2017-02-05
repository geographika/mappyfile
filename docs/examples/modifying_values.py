import mappyfile

mapfile = mappyfile.load("./docs/examples/raster.map")

# START OF API EXAMPLE
# update the map name
mapfile["name"] = "MyNewMap"
print type(mapfile)
# update the error file path in the map config section
# note key names will always need to be lower case
#mapfile["config"]["ms_errorfile"] = "/ms4w/tmp/ms_error.txt"

#mapfile["config"] = mappyfile.loads('CONFIG "PROJ_LIB" "projections"')
#mapfile["config"]["ms_errorfile"] = "/ms4w/tmp/ms_error.txt"
#mapfile["config"]["ms_errorfile"] = "/ms4w/tmp/ms_error.txt"

layers = mapfile["layers"]
layer = layers[0]
layer["name"] = "MyLayer"

print(mappyfile.dumps(mapfile))

# END OF API EXAMPLE