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

try:
    from urllib.parse import urlsplit
except ImportError:
    from urlparse import urlsplit

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
    errors = validate(s)
    assert(len(errors) == 0)


def test_color_validation():
    s = """
    MAP
        IMAGECOLOR 255 255 255
    END
    """
    errors = validate(s)
    assert(len(errors) == 0)


def test_color_validation_fail():
    s = """
    MAP
        IMAGECOLOR 255 255 256
    END
    """
    errors = validate(s)
    assert(len(errors) == 1)


def test_hexcolor_validation():
    s = """
    MAP
        IMAGECOLOR '#FF00FF'
    END
    """
    errors = validate(s)
    assert(len(errors) == 0)


def test_hexcolor_validation_fail():
    s = """
    MAP
        IMAGECOLOR 'FF00FF'
    END
    """
    errors = validate(s)
    assert(len(errors) == 1)


def test_hexcolor_validation_translucence():
    """
    See https://github.com/geographika/mappyfile/issues/65
    """

    s = """
    MAP
        LAYER
            TYPE POINT
            CLASS
                STYLE
                    COLOR '#FF00FFCC'
                END
            END
        END
    END
    """
    errors = validate(s)
    assert(len(errors) == 0)


def test_nested_validation():
    s = """
    MAP
        LAYER
            TYPE POLYGON
            EXTENT 0 0 0
        END
    END
    """
    errors = validate(s)
    print(errors)
    assert(len(errors) == 1)


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
    errors = validate(s)
    print(errors)
    assert(len(errors) == 0)
    # deepcopy crashes on (u'config', OrderedDict([('ON_MISSING_DATA', Token(NAME, 'FAIL'))]))


def test_ref_path():
    url = "file:////home/user/mappyfile/mappyfile/schemas/"
    scheme, netloc, path, query, fragment = urlsplit(url)
    print(scheme, netloc, path, query, fragment)
    assert(scheme == "file")

    url = "file:///D:/GitHub/mappyfile/mappyfile/schemas/"

    scheme, netloc, path, query, fragment = urlsplit(url)
    print(scheme, netloc, path, query, fragment)
    assert(scheme == "file")


def test_add_comments():
    s = """
    MAP
        IMAGECOLOR 'FF00FF'
        LAYER
            EXTENT 0 0 0
            TYPE POLYGON
        END
    END
    """
    d = to_dict(s)
    v = Validator()
    errors = v.validate(d, add_comments=True)

    print(len(errors))
    print(json.dumps(d, indent=4))

    for error in errors:
        print(error)

    pp = PrettyPrinter(indent=4, quote='"')  # expected

    res = pp.pprint(d)
    print(res)


def test_deref():
    """
    Check that the full schema properties have been expanded
    """
    v = Validator()
    schema_name = "cluster"
    validator = v.get_schema_validator(schema_name)
    jsn_schema = validator.schema

    print(json.dumps(jsn_schema, indent=4))
    print(jsn_schema["properties"]["filter"])
    assert(list(jsn_schema["properties"]["filter"].keys())[0] == "$ref")
    deref_schema = v.get_expanded_schema(schema_name)
    print(json.dumps(deref_schema, indent=4))
    print(deref_schema["properties"]["filter"])
    assert(list(deref_schema["properties"]["filter"].keys())[0] == "anyOf")


def test_cached_schema():
    """
    Check that the full schema properties have been expanded
    """
    v = Validator()
    schema_name = "cluster"
    validator = v.get_schema_validator(schema_name)
    jsn_schema = validator.schema
    assert(list(jsn_schema["properties"]["filter"].keys())[0] == "$ref")

    # get the schame again
    validator = v.get_schema_validator(schema_name)
    jsn_schema = validator.schema
    assert(list(jsn_schema["properties"]["filter"].keys())[0] == "$ref")


def test_cached_expanded_schema():
    """
    Check that the full schema properties have been expanded
    """
    v = Validator()
    schema_name = "cluster"

    deref_schema = v.get_expanded_schema(schema_name)
    assert(list(deref_schema["properties"]["filter"].keys())[0] == "anyOf")

    # get the schame again
    deref_schema = v.get_expanded_schema(schema_name)
    assert(list(deref_schema["properties"]["filter"].keys())[0] == "anyOf")


def test_extra_property_validation():
    """
    Check root errors are handled correctly
    """
    s = """
    MAP
        LAYER
            TYPE POLYGON
        END
    END
    """

    d = to_dict(s)
    d["unwanted"] = "error"
    v = Validator()
    errors = v.validate(d, add_comments=True)
    print(errors)
    assert(len(errors) == 1)


def test_double_error():

    s = """MAP
    NAME "sample"
    STATUS ON
    SIZE 600 400
    SYMBOLSET "../etc/symbols.txt"
    EXTENT -180 -90 180
    UNITS DD
    SHAPEPATH "../data"
    IMAGECOLOR 255 255 256
    FONTSET "../etc/fonts.txt"
    WEB
        IMAGEPATH "/ms4w/tmp/ms_tmp/"
        IMAGEURL "/ms_tmp/"
    END
    LAYER
        NAME "global-raster"
        TYPE RASTER
        STATUS DEFAULT
        DATA "bluemarble.gif"
    END
END"""

    d = mappyfile.loads(s, include_position=True)
    # print(json.dumps(d, indent=4))
    v = Validator()
    errors = v.validate(d, add_comments=True)
    # print(json.dumps(d, indent=4))
    # print(errors)
    for e in errors:
        print(e)
    assert(len(errors) == 2)
    print(mappyfile.dumps(d))


def test_line_position_mutlilines():

    s = """MAP
    NAME "sample"
    LAYER
        NAME "test"
        STATUS DEFAULT
        DATA "SELECT GEOM
        FROM
        TABLE"
        TYPE LINEX
    END
END"""

    p = Parser()
    ast = p.parse(s)
    print(ast)

    d = mappyfile.loads(s, include_position=True)
    v = Validator()
    errors = v.validate(d, add_comments=True)
    print(json.dumps(d, indent=4))
    # print(errors)
    for e in errors:
        print(e)
    assert(len(errors) == 1)
    err = errors[0]
    assert(err["line"] == 9)
    assert(err["column"] == 9)
    print(mappyfile.dumps(d))


def test_root_position():
    """
    Check the root objects position is found correctly
    """

    s = """
    MAP
        METADATA
            "wms_title"    "Toronto Landsat 5 TM"
        END
    END
    """

    d = mappyfile.loads(s, include_position=True)
    v = Validator()
    assert d["__position__"]["line"] == 2
    errors = v.validate(d, add_comments=True)
    assert len(errors) == 1


def test_cluster_validation():

    s = u"""
    MAP
        LAYER
            TYPE POINT
            CLUSTER
                MAXDISTANCE 50
                REGION "ELLIPSE"
            END
        END
    END
    """

    d = mappyfile.loads(s, include_position=True)
    v = Validator()
    assert d["__position__"]["line"] == 2
    errors = v.validate(d, add_comments=True)
    print(mappyfile.dumps(d))
    assert len(errors) == 0


def test_cluster_validation_fail():

    s = u"""
    MAP
        LAYER
            TYPE POINT
            CLUSTER
                MAXDISTANCE 50
                REGION "ELLIPSEZ"
            END
        END
    END
    """

    d = mappyfile.loads(s, include_position=True)
    v = Validator()
    errors = v.validate(d, add_comments=True)
    print(mappyfile.dumps(d))
    assert len(errors) == 1


def test_version_warnings():

    s = """MAP
    NAME "sample"
    LAYER
        NAME "test"
        TYPE LINE
        CLASS
            #MADEUP True
            COLOR 0 0 0
        END
    END
END"""

    d = mappyfile.loads(s, include_position=False)
    v = Validator()
    errors = v.validate(d, add_comments=True, version=8.0)
    print(errors)
    assert len(errors) == 1


def test_keyword_versioning():

    properties = {
  "type": "object",
  "properties": {
    "__type__": {
      "enum": ["label"]
    },
    "align": {
      "oneOf": [
        {
          "type": "string",
          "enum": ["left", "center", "right"],
          "additionalProperties": False
        },
        {
          "type": "string",
          "pattern": "^\\[(.*?)\\]$",
          "description": "attribute"
        }
      ],
      "metadata": {
        "minVersion": 5.4
      }
    }
  }
}

    v = Validator()
    assert "align" in properties["properties"].keys()
    properties = v.get_versioned_properties(properties, 5.2)
    print(json.dumps(properties, indent=4))
    assert "align" not in properties["properties"].keys()


def test_property_versioning():

    properties = {
      "force": {
      "oneOf": [
        {"type": "boolean"},
        {
          "enum": ["group"],
          "metadata": {
            "minVersion": 6.2
          }
        }]
      }
    }

    v = Validator()
    assert "enum" in properties["force"]["oneOf"][1].keys()
    assert len(properties["force"]["oneOf"]) == 2
    properties = v.get_versioned_properties(properties, 6.0)
    print(json.dumps(properties, indent=4))
    assert len(properties["force"]["oneOf"]) == 1


def test_object_versioning():
    """
    Exclude whole objects if they were added in a
    later version of MapServer
    """

    s = """MAP
    NAME "sample"
    LAYER
        TYPE POLYGON
        COMPOSITE
            COMPOP "lighten"
            OPACITY 50
            COMPFILTER "blur(10)"
        END
    END
END"""

    d = mappyfile.loads(s, include_position=False)
    v = Validator()
    errors = v.validate(d, add_comments=True, version=6.0)
    assert len(errors) == 1

    d = mappyfile.loads(s, include_position=False)
    errors = v.validate(d, add_comments=True, version=7.0)
    assert len(errors) == 0


def test_get_versioned_schema():

    validator = Validator()
    jsn = validator.get_versioned_schema(7.6)
    # print(json.dumps(jsn, indent=4))
    assert "defresolution" in jsn["properties"].keys()


def run_tests():
    pytest.main(["tests/test_validation.py"])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # run_tests()
    test_object_versioning()
    print("Done!")
