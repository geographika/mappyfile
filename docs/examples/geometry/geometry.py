import os
from copy import deepcopy
from shapely.geometry import LineString
import mappyfile
import sys
from helper import create_image


sys.path.append(os.path.abspath("./docs/examples"))


def dilation(mapfile):
    line = LineString([(0, 0), (1, 1), (0, 2), (2, 2), (3, 1), (1, 0)])
    ll = mappyfile.find(mapfile["layers"], "name", "line")
    ll["features"][0]["wkt"] = line.wkt

    dilated = line.buffer(0.5, cap_style=3)
    pl = mappyfile.find(mapfile["layers"], "name", "polygon")
    pl["features"][0]["wkt"] = dilated.wkt

    mapfile["extent"] = " ".join(map(str, dilated.buffer(0.8).bounds))
    return dilated


def erosion(mapfile, dilated):
    """
    We will continue to work with the modified Mapfile
    If we wanted to start from scratch we could simply reread it
    """
    ll = mappyfile.find(mapfile["layers"], "name", "line")
    ll["status"] = "OFF"

    pl = mappyfile.find(mapfile["layers"], "name", "polygon")

    # make a deep copy of the polygon layer in the Map
    # so any modification are made to this layer only
    pl2 = deepcopy(pl)

    pl2["name"] = "newpolygon"
    mapfile["layers"].append(pl2)

    dilated = dilated.buffer(-0.3)
    pl2["features"][0]["wkt"] = dilated.wkt

    style = pl["classes"][0]["styles"][0]
    style["color"] = "#999999"
    style["outlinecolor"] = "#b2b2b2"


def main():
    mf = "./docs/examples/geometry/geometry.map"
    mapfile = mappyfile.open(mf)

    mapfile["size"] = [600, 600]
    output_folder = os.path.join(os.getcwd(), "docs/images")

    dilated = dilation(mapfile)
    create_image("dilated", mapfile, output_folder=output_folder)

    erosion(mapfile, dilated)
    create_image("erosion", mapfile, output_folder=output_folder)


if __name__ == "__main__":
    main()
    print("Done!")
