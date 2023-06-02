import mappyfile


def test():
    # START OF API EXAMPLE
    # load will accept a filename (loads will accept a string)
    mapfile = mappyfile.open("./docs/examples/raster.map")

    # search for a layer by name
    layer = mappyfile.find(mapfile["layers"], "name", "sea")
    print(layer["name"])  # "sea"

    # search for all layers in a group
    for layer in mappyfile.findall(mapfile["layers"], "group", "my_group"):
        print(layer["name"])

    # END OF API EXAMPLE
    assert layer["name"] == "sea"


if __name__ == "__main__":
    test()
