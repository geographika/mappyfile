import os
import logging
import pytest
import mappyfile
from mappyfile.parser import Parser
from mappyfile.transformer import MapfileToDict
from mappyfile.pprint import PrettyPrinter
from lark import UnexpectedToken
from mappyfile.validator import Validator


def test_all_maps():
    sample_dir = os.path.join(os.path.dirname(__file__), "sample_maps")

    # the following "map" files are includes used by other mapfiles in msautotest
    # TODO - rename all these to .include in MapServer source to allow them to be more
    # easily processed
    ignore_list = [
        "bdry_counpy2_mssql.map",
        "bdry_counpy2_ogr.map",
        "bdry_counpy2_postgis.map",
        "bdry_counpy2_shapefile.map",
        "indx_q100kpy4_ogr.map",
        "indx_q100kpy4_shapefile.map",
        "mssql_connection.map",
        "quoted_text.MAP",
        "style-size.map",
        "wfs_ogr_export_metadata.map",
    ]

    # list any maps that are known not to parse and are to be fixed
    ignore_list += ["centerline.map"]

    p = Parser(expand_includes=False)
    m = MapfileToDict(include_position=True)
    v = Validator()

    failing_maps = []

    for fn in os.listdir(sample_dir):
        if fn not in ignore_list:
            print(fn)
            try:
                ast = p.parse_file(os.path.join(sample_dir, fn))
                d = m.transform(ast)
                errors = v.validate(d)
                try:
                    assert len(errors) == 0
                except AssertionError as ex:
                    logging.warning("Validation errors in %s ", fn)
                    logging.error(ex)
                    logging.warning(errors)
            except (BaseException, UnexpectedToken) as ex:
                logging.warning("Cannot process %s ", fn)
                logging.error(ex)
                failing_maps.append(fn)

    logging.warning("The list of maps below have failed to parse")
    logging.warning(failing_maps)


def test_includes():
    p = Parser()

    ast = p.parse_file("./tests/samples/include1.map")
    m = MapfileToDict()

    d = m.transform(ast)  # works
    print(mappyfile.dumps(d))


def test_includes_nested_path():
    p = Parser()

    ast = p.parse_file("./tests/samples/include1_nested_path.map")
    m = MapfileToDict()

    d = m.transform(ast)  # works
    print(mappyfile.dumps(d))


def test_includes_max_recursion():
    p = Parser()

    with pytest.raises(Exception) as excinfo:
        p.parse_file("./tests/samples/include1_recursive.map")

    assert "Maximum nested include exceeded" in str(excinfo.value)


def test_includes_no_expand():
    """
    https://github.com/geographika/mappyfile/issues/39
    """
    s = """
    MAP
        INCLUDE "includes/mymapfile.map"
    END
    """

    d = mappyfile.loads(s, expand_includes=False)
    pp = PrettyPrinter(indent=0, newlinechar=" ", quote="'")
    output = pp.pprint(d)

    expected = "MAP INCLUDE 'includes/mymapfile.map' END"
    assert output == expected


def test_two_includes():
    s = """
    MAP
        INCLUDE "include1.txt"
        INCLUDE "include2.txt"
    END
    """

    d = mappyfile.loads(s, expand_includes=False)
    logging.debug(d)
    pp = PrettyPrinter(indent=0, newlinechar=" ", quote="'")
    output = pp.pprint(d)
    print(output)
    expected = "MAP INCLUDE 'include1.txt' INCLUDE 'include2.txt' END"
    assert output == expected


def test_non_ascii():
    p = Parser()

    ast = p.parse_file("./tests/samples/non_ascii.map")
    m = MapfileToDict()

    d = m.transform(ast)  # works
    print(mappyfile.dumps(d))


def test_unicode_map():
    with open("./tests/samples/unicode.map", "r") as mf_file:
        mf = mappyfile.load(mf_file)

    print(mappyfile.dumps(mf))


def run_tests():
    pytest.main(["tests/test_sample_maps.py"])


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("mappyfile").setLevel(logging.INFO)
    # run_tests()
    # test_unicode_map()
    test_all_maps()
    print("Done!")
