from mappyfile.parser import Parser

p = Parser()

# parse will accept a filename or a string
mapfile = p.parse_file("./docs/examples/raster.map")

# print the map name
print(mapfile["name"]) # would output "MyMap"
       
# access layers
layers = mapfile["layers"]
layer1 = layers[0] # access by index
	
layer2 = layers["layer2"] # access by layer NAME property
	
# access classes in a layer
classes = layer1["classes"]

for c in classes:
    print(c["name"])

# if the AttrDict approach is taken then the following could also be used
# could be added for a more polished version
    
print(mapfile.name) 
layer2 = layers.layer2
print(layer2.classes[0].name)