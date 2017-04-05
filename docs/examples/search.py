import mappyfile

# load will accept a filename (loads will accept a string)
mapfile = mappyfile.load("./docs/examples/raster.map")

# Search of a layer by its name
mappyfile.find(mapfile['layers'], 'name', 'my_layer')
       
# Search for all layers of a group
for layer in mappyfile.findall(mapfile['layers'], 'group', 'my_group'):
    print(layer['name'])
