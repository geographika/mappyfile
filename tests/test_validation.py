import os
import logging
import mappyfile
# from mappyfile import validator
from mappyfile.parser import Parser
from mappyfile.transformer import MapfileToDict
from subprocess import Popen, PIPE, STDOUT

DLL_LOCATION = r"C:\MapServer\bin"


def create_image(name, mapfile, output_folder, format="png"):

    out_map = os.path.join(output_folder, "%s.map" % name)
    mappyfile.write(mapfile, out_map)

    out_img = os.path.join(output_folder, name)

    return _create_image_from_map(out_map, out_img, format=format)


def _create_image_from_map(map_file, out_img, format):

    out_img += ".%s" % format

    params = [
        "shp2img",
        "-m",
        map_file,
        "-i",
        format,
        "-o",
        out_img,
        "-s",
        256,
        256]  # ,  # "-e", "0 0 5 5"
    params = [str(p) for p in params]
    logging.info(" ".join(params))

    os.environ['PATH'] = DLL_LOCATION + ';' + os.environ['PATH']

    p = Popen(params, stdout=PIPE, stderr=STDOUT)

    errors = []

    with p.stdout:
        for line in iter(p.stdout.readline, b''):
            errors.append(line)

    p.wait()  # wait for the subprocess to exit

    if errors:
        logging.error("\n".join(errors))
        return None
    else:
        logging.info("Created %s", out_img)
        os.startfile(out_img)

    return out_img


def main():
    s = """
    MAP
        NAME 'blah'
        ANGLE 100
        DEBUG on
        CONFIG "ON_MISSING_DATA" FAIL # can be quoted or non-quoted
        STATUS on # need to enforce lowercase
        EXTENT -100 -100 100 100
        SIZE 400 400
        PROJECTION
            AUTO
        END
        LAYER
            PROJECTION
                AUTO
            END
            STATUS ON
            NAME "hi"
            TYPE polygon

            FEATURE
              POINTS 1 1 50 50 1 50 1 1 END
            END
            CLASS
                STYLE
                    COLOR 255 0 0
                END
            END

        END
        #LAYER
        #    NAME "hi2"
        #    TYPE point
        #END
    END
    """

    p = Parser()
    m = MapfileToDict()

    ast = p.parse(s)
    d = m.transform(ast)

    # test a value passed in from the editor
    d["status"] = "OFF"  # need to convert to uppercase if not already?

    # d["layers"][0]["type"] = "POINTX"

    print(d)
    # s = schema["definitions"]["map"]["properties"]["status"]

    """
    if validator.validate(d):
        name = "test"
        output_folder = r"D:\Temp"
        create_image(name, d, output_folder=output_folder)
    """


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
    print("Done!")
