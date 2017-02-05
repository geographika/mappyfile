import mappyfile

# load will accept a filename (loads will accept a string)
mapfile = mappyfile.load("./docs/examples/raster.map")

# print the map name
print(mapfile["name"]) # outputs "MyMap"
       
# access layers
layers = mapfile["layers"]
layer2 = layers[1] # access by index
	
# access classes in a layer
classes = layer2["classes"]

for c in classes:
    print(c["name"])