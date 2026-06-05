import os
import logging
import pytest
import mappyfile
from mappyfile.parser import Parser
from mappyfile.transformer import MapfileToDict
from mappyfile.pprint import PrettyPrinter
from mappyfile.validator import Validator

SAMPLE_DIR = os.path.join(os.path.dirname(__file__), "sample_maps")

IGNORE_LIST = [
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


def get_map_files(extra_ignore=None):
    ignore = set(IGNORE_LIST + (extra_ignore or []))
    return [
        fn
        for fn in os.listdir(SAMPLE_DIR)
        if fn.lower().endswith(".map") and fn not in ignore
    ]


@pytest.mark.parametrize("fn", get_map_files(extra_ignore=["centerline.map"]))
def test_all_maps(fn):
    p = Parser(expand_includes=True)
    m = MapfileToDict(include_position=True)
    v = Validator()

    ast = p.parse_file(os.path.join(SAMPLE_DIR, fn))
    d = m.transform(ast)
    errors = v.validate(d)
    assert len(errors) == 0, f"Validation errors in {fn}: {errors}"


@pytest.mark.parametrize("fn", get_map_files())
def test_yaml_roundtrip_all_maps(fn, tmp_path):
    import mappyfile.yaml

    v = Validator()
    map_path = os.path.join(SAMPLE_DIR, fn)
    yaml_path = tmp_path / f"{fn}.yaml"

    d = mappyfile.open(map_path, expand_includes=True)

    mappyfile.yaml.save(d, str(yaml_path))
    assert yaml_path.exists(), f"YAML file not created for {fn}"

    d2 = mappyfile.yaml.open(str(yaml_path))

    errors = v.validate(d2)
    if errors:
        logging.warning("Validation errors after YAML round-trip for %s", fn)

    original = mappyfile.dumps(d)
    roundtrip = mappyfile.dumps(d2)
    assert original == roundtrip, f"Output mismatch after YAML round-trip for {fn}"


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
    # test_all_maps()

    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as tmp_dir:
        test_yaml_roundtrip_all_maps(Path(tmp_dir))

    print("Done!")
