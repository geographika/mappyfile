import os
import logging
import json
import mappyfile
from mappyfile.validator import Validator
from mappyfile.parser import Parser
from mappyfile.transformer import MapfileToDict
from mappyfile.pprint import PrettyPrinter
from subprocess import Popen, PIPE, STDOUT
import pytest

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


def to_dict(s):
    p = Parser()
    m = MapfileToDict()
    ast = p.parse(s)
    d = m.transform(ast)
    print(json.dumps(d, indent=4))
    return d


def validate(s):
    d = to_dict(s)
    v = Validator()
    return v.validate(d)


def test_config_validation():
    """
    Any key are allowed, but the ones in the docs can be validated
    These need to be made lower-case as JSON is case sensitive
    """

    s = """
    MAP
        NAME 'ConfigMap'
        CONFIG MS_ERRORFILE 'stderr'
        CONFIG 'PROJ_DEBUG' 'OFF'
        CONFIG ON_MISSING_DATA IGNORE
    END
    """
    assert(validate(s))


def test_color_validation():
    s = """
    MAP
        IMAGECOLOR 255 255 255
    END
    """
    assert(validate(s))


def test_color_validation_fail():
    s = """
    MAP
        IMAGECOLOR 255 255 256
    END
    """
    assert(not validate(s))


def test_hexcolor_validation():
    s = """
    MAP
        IMAGECOLOR '#FF00FF'
    END
    """
    assert(validate(s))


def test_hexcolor_validation_fail():
    s = """
    MAP
        IMAGECOLOR 'FF00FF'
    END
    """
    assert(not validate(s))


def test_lowercase():

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

    print(json.dumps(d, indent=4))
    # deepcopy crashes on (u'config', OrderedDict([('ON_MISSING_DATA', Token(NAME, 'FAIL'))]))


def test_ref_path():
    from jsonschema.compat import urlsplit
    url = "file:////home/user/mappyfile/mappyfile/schemas/"
    scheme, netloc, path, query, fragment = urlsplit(url)
    print(scheme, netloc, path, query, fragment)
    assert(scheme == "file")

    url = "file:///D:/GitHub/mappyfile/mappyfile/schemas/"

    scheme, netloc, path, query, fragment = urlsplit(url)
    print(scheme, netloc, path, query, fragment)
    assert(scheme == "file")


def test_add_messages():
    s = """
    MAP
        IMAGECOLOR 'FF00FF'
        LAYER
            EXTENT 0 0 0
        END
    END
    """
    d = to_dict(s)
    v = Validator()
    errors = v.validate(d, add_messages=True)

    print(len(errors))

    for error in errors:
        print(error.__dict__)

    pp = PrettyPrinter(indent=4, quote='"')  # expected
    res = pp.pprint(d)
    print(res)


def run_tests():
    """
    Need to comment out the following line in C:\VirtualEnvs\mappyfile\Lib\site-packages\pep8.py
    #stdin_get_value = sys.stdin.read
    Or get AttributeError: '_ReplInput' object has no attribute 'read'
    """
    pytest.main(["tests/test_validation.py"])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # main()
    # test_lowercase()
    # run_tests()
    test_add_messages()
    print("Done!")
