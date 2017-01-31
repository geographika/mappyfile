from mappyfile.parser import Parser

p = Parser()

# parse will accept a filename or a string
mapfile = p.parse_file("./docs/examples/raster.map")

# START OF API EXAMPLE
# update the map name
mapfile["name"] = "MyMap"

# update the error file path in the map config section
# note key names will always need to be lower case
mapfile["config"]["ms_errorfile"] = "/ms4w/tmp/ms_error.txt"

layer = layers[0]
layer["name"] = "MyLayer"
# END OF API EXAMPLE