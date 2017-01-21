from mappyfile.pprint import QuotedList, NonQuotedList, QuotedString, NonQuotedString, Container, HiddenContainer
from mappyfile.pprint import PrettyPrinter, MAPFILE_TYPE
import json

def create_sample_dict():
    style1 = Container()
    style1[MAPFILE_TYPE] = "style"
    style1["color"] = NonQuotedString("99 231 117")
    style1["width"] = NonQuotedString("1")

    style2 = Container()
    style2[MAPFILE_TYPE] = "style"
    style2["name"] = QuotedString("MyStyle")
    style2["color"] = NonQuotedString("108 201 187")
    style2["width"] = NonQuotedString("2")

    styles = HiddenContainer([style1, style2])

    class1 = Container()
    class1[MAPFILE_TYPE] = "class"
    class1["name"] = QuotedString("Class1")
    class1["styles"] = styles

    classes = HiddenContainer([class1])

    points = NonQuotedList(["0 100", "100 200", "40 90"])
    feature1 = Container()
    feature1[MAPFILE_TYPE] = "feature"
    feature1["points"] = points
    features = HiddenContainer([feature1])  

    layer1 = Container()
    layer1[MAPFILE_TYPE] = "layer"
    layer1["name"] = QuotedString("Layer1")
    layer1["classes"] = classes
    layer1["features"] = features

    layer2 = Container()
    layer2[MAPFILE_TYPE] = "layer"
    layer2["name"] = QuotedString("Layer2")

    layers = HiddenContainer([layer1, layer2])

    map_ = Container()
    map_[MAPFILE_TYPE] = "map"

    projection = QuotedList(["proj=utm", "ellps=GRS80", "datum=NAD83", "zone=15", "units=m", "north", "no_defs"])

    map_["projection"] = projection
    map_["layers"] = layers

    return map_

def print_dict_structure(d):
    # http://stackoverflow.com/questions/3229419/pretty-printing-nested-dictionaries-in-python
    print json.dumps(d, indent=4)

def add_layer(d):
    layer = Container()
    layer[MAPFILE_TYPE] = "layer"
    layer["name"] = QuotedString("Layer1.5")
    d["layers"].insert(1, layer)

map_ = create_sample_dict()
print_dict_structure(map_)

pp = PrettyPrinter()
print(pp.pprint(map_))

add_layer(map_)
print(pp.pprint(map_))

# print a partial part of the map
print(pp.pprint(map_["layers"][0]["classes"][0]))
print(pp.pprint(map_["layers"][0]["classes"]))




