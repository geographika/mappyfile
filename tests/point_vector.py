from mappyfile.types import *

def create_layer1():
    """
    LAYER
        NAME "anchors"
        TYPE POINT
        STATUS on
        CLASS
            STYLE
                COLOR 255 0 0
                SIZE 8
                WIDTH 1
                SYMBOL "circle"
            END
        END
        FEATURE POINTS 50 50 END END
        FEATURE POINTS 200 200 END END
    END
    """

    layer1 = Container()
    layer1[MAPFILE_TYPE] = "layer"
    layer1["name"] = QuotedString("anchors")
    layer1["type"] = "point"
    layer1["status"] = "on"

    style1 = Container()
    style1[MAPFILE_TYPE] = "style"
    style1["color"] = "255 0 0"
    style1["size"] = "8"
    style1["width"] = "1"
    style1["symbol"] = QuotedString("circle")

    class1 = Container()
    class1[MAPFILE_TYPE] = "class"    
    class1["styles"] = HiddenContainer([style1])

    layer1["classes"] = HiddenContainer([class1])

    feature1 = Container()
    feature1[MAPFILE_TYPE] = "feature"
    points1 = ["50 50"]
    feature1["points"] = points1

    feature2 = Container()
    feature2[MAPFILE_TYPE] = "feature"
    points2 = ["200 200 "]
    feature2["points"] = points2

    layer1["features"] = HiddenContainer([feature1, feature2]) 
    return layer1

def create_map():

    layer1 = create_layer1()
    #layer2 = create_layer2()
    #layer3 = create_layer3()

    #layers = HiddenContainer([layer1, layer2, layer3])
    layers = HiddenContainer([layer1])


    """
    STATUS ON
    EXTENT 0 0 400 300
    SIZE 200 150
    FONTSET "../misc/fonts.lst"
    IMAGETYPE png24
    symbolset "symbolset"
    """
    map_ = Container()
    map_[MAPFILE_TYPE] = "map"

    map_["status"] = "ON"
    map_["extent"] = "0 0 400 300"
    map_["size"] = "200 150"
    #map_["fontset"] = QuotedString("../misc/fonts.lst")
    map_["imagetype"] = "png24"
    map_["symbolset"] = QuotedString("symbolset")


    map_["layers"] = layers

    return map_