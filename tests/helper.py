from mappyfile.types import *

def create_style1():
    style1 = Container()
    style1[MAPFILE_TYPE] = "style"
    style1["color"] = "99 231 117"
    style1["width"] = "1"
    return style1

def create_style2():
    style2 = Container()
    style2[MAPFILE_TYPE] = "style"
    style2["name"] = QuotedString("MyStyle")
    style2["color"] = "108 201 187"
    style2["width"] = "2"
    return style2

def create_styles():
    style1 = create_style1()
    style2 = create_style2()

    return HiddenContainer([style1, style2])

def create_web_metdata():

    metadata = Container()
    metadata[MAPFILE_TYPE] = "metadata"
    metadata[QuotedString("wms_enable_request")] = QuotedString("*")

    web = Container()
    web[MAPFILE_TYPE] = "web"
    web["metadata"] = metadata

    return web

def create_class1():
    class1 = Container()
    class1[MAPFILE_TYPE] = "class"
    class1["name"] = QuotedString("Class1")
    class1["styles"] = create_styles()
    return class1

def create_features():
    points = ["0 100", "100 200", "40 90"]
    feature1 = Container()
    feature1[MAPFILE_TYPE] = "feature"
    feature1["points"] = points
    return feature1

def create_layer2():

    layer2 = Container()
    layer2[MAPFILE_TYPE] = "layer"
    layer2["name"] = QuotedString("Layer2")

    layer2["processing"] = KeyValueList([QuotedString("BANDS=1"), 
                                         QuotedString("CONTOUR_ITEM=elevation"), 
                                         QuotedString("CONTOUR_INTERVAL=20")])

    return layer2

def create_sample_map():

    layer1 = Container()
    layer1[MAPFILE_TYPE] = "layer"
    layer1["name"] = QuotedString("Layer1")
    layer1["classes"] = HiddenContainer([create_class1()])
    layer1["features"] = HiddenContainer([create_features()])  

    layer2 = create_layer2()

    layers = HiddenContainer([layer1, layer2])

    map_ = Container()
    map_[MAPFILE_TYPE] = "map"

    projection = QuotedList(["proj=utm", "ellps=GRS80", "datum=NAD83", "zone=15", "units=m", "north", "no_defs"])

    map_["web"] = create_web_metdata()
    map_["projection"] = projection
    map_["layers"] = layers

    return map_