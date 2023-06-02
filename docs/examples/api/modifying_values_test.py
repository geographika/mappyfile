import mappyfile


def test():
    mapfile = mappyfile.open("./docs/examples/raster.map")
    # START OF API EXAMPLE
    # update the map name
    mapfile["name"] = "MyNewMap"

    # update a layer name
    layers = mapfile["layers"]
    layer = layers[0]
    layer["name"] = "MyLayer"

    # update the error file path in the map config section
    # note key names can be lower or upper case

    mapfile["config"]["ms_errorfile"] = "/ms4w/tmp/ms_error.txt"

    # update the web metadata settings

    mapfile["web"]["metadata"]["wms_format"] = "image/png"
    print(mappyfile.dumps(mapfile["web"]))  # print out just the WEB section

    # alternatively we can parse the Mapfile syntax and load it directly

    s = """
        METADATA
            'wms_enable_request' '*'
            'wms_feature_info_mime_type' 'text/html'
            'wms_format' 'image/jpg'
        END"""

    metadata = mappyfile.loads(s)
    mapfile["web"]["metadata"] = metadata
    print(mappyfile.dumps(mapfile))

    # END OF API EXAMPLE
    assert layer["name"] == "MyLayer"
    assert mapfile["web"]["metadata"]["wms_format"] == "image/jpg"


if __name__ == "__main__":
    test()
