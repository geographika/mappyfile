import pytest
import logging
import mappyfile
import mappyfile.yaml

MAPFILE_STRING = """
MAP
    NAME "TEST"
    STATUS ON
    EXTENT -180 -90 180 90
    WEB
        METADATA
            "wms_title" "Test"
        END
    END
    LAYER
        NAME "test_layer"
        TYPE POLYGON
        STATUS ON
        DATA "test"
    END
END
"""


def test_yaml_import_error(monkeypatch):
    import sys

    # remove all relevant modules to force re-import
    monkeypatch.delitem(sys.modules, "mappyfile.yaml", raising=False)
    monkeypatch.delitem(sys.modules, "mappyfile.yamlutils", raising=False)
    monkeypatch.delitem(sys.modules, "yaml", raising=False)

    # make yaml unimportable
    monkeypatch.setitem(sys.modules, "yaml", None)

    with pytest.raises(ImportError, match="PyYAML is required for YAML support"):
        import mappyfile.yamlutils  # noqa: F401


def test_yaml_dumps():
    d = mappyfile.loads(MAPFILE_STRING)
    yaml_string = mappyfile.yaml.dumps(d)
    assert "__type__: map" in yaml_string
    assert "name: TEST" in yaml_string


def test_yaml_loads():
    d = mappyfile.loads(MAPFILE_STRING)
    yaml_string = mappyfile.yaml.dumps(d)
    d2 = mappyfile.yaml.loads(yaml_string)
    assert d2["name"] == "TEST"
    assert d2["__type__"] == "map"


def test_yaml_roundtrip_string():
    d = mappyfile.loads(MAPFILE_STRING)
    original = mappyfile.dumps(d)
    yaml_string = mappyfile.yaml.dumps(d)
    d2 = mappyfile.yaml.loads(yaml_string)
    roundtrip = mappyfile.dumps(d2)
    assert original == roundtrip


def test_yaml_open(tmp_path):
    d = mappyfile.loads(MAPFILE_STRING)
    original = mappyfile.dumps(d)
    yaml_file = tmp_path / "test.yaml"
    mappyfile.yaml.save(d, str(yaml_file))
    assert yaml_file.exists()
    d2 = mappyfile.yaml.open(str(yaml_file))
    roundtrip = mappyfile.dumps(d2)
    assert original == roundtrip


def test_yaml_load(tmp_path):
    d = mappyfile.loads(MAPFILE_STRING)
    original = mappyfile.dumps(d)
    yaml_file = tmp_path / "test.yaml"
    mappyfile.yaml.save(d, str(yaml_file))
    assert yaml_file.exists()
    with open(str(yaml_file)) as fp:
        d2 = mappyfile.yaml.load(fp)
    roundtrip = mappyfile.dumps(d2)
    assert original == roundtrip


def test_yaml_save(tmp_path):
    d = mappyfile.loads(MAPFILE_STRING)
    yaml_file = tmp_path / "test.yaml"
    result = mappyfile.yaml.save(d, str(yaml_file))
    assert result == str(yaml_file)
    assert yaml_file.exists()


def test_yaml_dump(tmp_path):
    d = mappyfile.loads(MAPFILE_STRING)
    original = mappyfile.dumps(d)
    yaml_file = tmp_path / "test.yaml"
    with open(str(yaml_file), "w") as fp:
        mappyfile.yaml.dump(d, fp)
    assert yaml_file.exists()
    d2 = mappyfile.yaml.open(str(yaml_file))
    roundtrip = mappyfile.dumps(d2)
    assert original == roundtrip


def test_yaml_nested_objects():
    d = mappyfile.loads(MAPFILE_STRING)
    yaml_string = mappyfile.yaml.dumps(d)
    d2 = mappyfile.yaml.loads(yaml_string)
    assert d2["web"]["__type__"] == "web"
    assert d2["web"]["metadata"]["wms_title"] == "Test"
    assert d2["layers"][0]["name"] == "test_layer"


def run_tests():
    pytest.main(["tests/test_yaml.py"])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_yaml_dumps()
    test_yaml_loads()
    test_yaml_roundtrip_string()
    test_yaml_nested_objects()
    print("Done!")
