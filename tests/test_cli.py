import logging
import tempfile
import pytest
from click.testing import CliRunner
from mappyfile import cli


MAPFILE_STRING = """
MAP
    NAME "TEST"
    STATUS ON
    EXTENT -180 -90 180 90
    LAYER
        NAME "test_layer"
        TYPE POLYGON
        STATUS ON
        DATA "test"
    END
END
"""


def test_get_mapfiles():
    tf = tempfile.NamedTemporaryFile(suffix=".map")
    print(tf.name)
    mapfiles = [tf.name]
    found_mapfiles = cli.get_mapfiles(mapfiles)
    print(found_mapfiles)


def test_yaml_export(tmp_path):
    runner = CliRunner()
    map_file = tmp_path / "test.map"
    yaml_file = tmp_path / "test.yaml"
    map_file.write_text(MAPFILE_STRING, encoding="utf-8")

    result = runner.invoke(cli.main, ["yaml-export", str(map_file), str(yaml_file)])

    assert result.exit_code == 0, result.output
    assert yaml_file.exists()
    assert "__type__: map" in yaml_file.read_text(encoding="utf-8")
    assert f"{map_file} exported to {yaml_file}" in result.output


def test_yaml_import(tmp_path):
    runner = CliRunner()
    map_file = tmp_path / "test.map"
    yaml_file = tmp_path / "test.yaml"
    output_map_file = tmp_path / "output.map"
    map_file.write_text(MAPFILE_STRING, encoding="utf-8")

    # first export to YAML
    runner.invoke(cli.main, ["yaml-export", str(map_file), str(yaml_file)])

    # then import back
    result = runner.invoke(
        cli.main, ["yaml-import", str(yaml_file), str(output_map_file)]
    )

    assert result.exit_code == 0, result.output
    assert output_map_file.exists()
    assert f"{yaml_file} imported to {output_map_file}" in result.output


def test_yaml_roundtrip_cli(tmp_path):
    runner = CliRunner()
    map_file = tmp_path / "test.map"
    yaml_file = tmp_path / "test.yaml"
    output_map_file = tmp_path / "output.map"
    map_file.write_text(MAPFILE_STRING, encoding="utf-8")

    runner.invoke(cli.main, ["yaml-export", str(map_file), str(yaml_file)])
    runner.invoke(cli.main, ["yaml-import", str(yaml_file), str(output_map_file)])

    original = map_file.read_text(encoding="utf-8")
    roundtrip = output_map_file.read_text(encoding="utf-8")

    # compare by parsing both to normalise formatting
    import mappyfile

    d1 = mappyfile.loads(original)
    d2 = mappyfile.loads(roundtrip)
    assert mappyfile.dumps(d1) == mappyfile.dumps(d2)


def run_tests():
    pytest.main(["tests/test_cli.py"])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_get_mapfiles()
    print("Done!")
