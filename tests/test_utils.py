import logging
import os
import io
import tempfile
import mappyfile
import pytest
from mappyfile.transformer import MapfileTransformer, MapfileToDict
from mappyfile.parser import Parser


class CustomTransformer(MapfileTransformer):
    def __init__(
        self,
        include_position=False,
        include_comments=False,
        custom_parameter=False,
    ):
        self.custom_parameter = custom_parameter
        super().__init__(include_position, include_comments)


def test_open():
    fn = "./tests/sample_maps/256_overlay_res.map"
    d = mappyfile.open(fn)
    assert d["name"] == "TEST"

    d = mappyfile.open(fn, expand_includes=False)
    assert d["name"] == "TEST"

    d = mappyfile.open(fn, include_position=True)
    assert d["name"] == "TEST"

    d = mappyfile.open(fn, include_comments=True)
    assert d["name"] == "TEST"


def test_loads():
    s = """MAP NAME "TEST" END"""

    d = mappyfile.loads(s)
    assert d["name"] == "TEST"

    d = mappyfile.loads(s, expand_includes=False)
    assert d["name"] == "TEST"

    d = mappyfile.loads(s, include_position=True)
    assert d["name"] == "TEST"

    d = mappyfile.loads(s, include_comments=True)
    assert d["name"] == "TEST"


def test_loads_kwargs():
    s = """MAP NAME "TEST" END"""
    d = mappyfile.loads(s, transformer_class=CustomTransformer, custom_parameter=True)
    assert d["name"] == "TEST"

    p = Parser(expand_includes=True, include_comments=True, custom_parameter=True)
    assert p.kwargs["custom_parameter"] is True
    m = MapfileToDict(
        include_position=True, include_comments=True, custom_parameter=True
    )
    assert m.kwargs["custom_parameter"] is True


def test_dump():
    s = """MAP NAME "TEST" END"""
    d = mappyfile.loads(s)

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as fp:
        mappyfile.dump(d, fp)

    with open(fp.name) as fp2:
        d = mappyfile.load(fp2)

    assert d["name"] == "TEST"


def test_stringio():
    s = """MAP NAME "TEST" END"""
    ip = io.StringIO(s)

    d = mappyfile.load(ip)

    assert d["name"] == "TEST"


def test_save():
    s = """MAP NAME "TEST" END"""
    d = mappyfile.loads(s)

    output_file = os.path.join(tempfile.mkdtemp(), "test_mapfile.map")
    mappyfile.save(d, output_file)

    with open(output_file) as fp:
        d = mappyfile.load(fp)

    assert d["name"] == "TEST"


def test_dumps():
    s = """MAP NAME "TEST" END"""

    d = mappyfile.loads(s)
    output = mappyfile.dumps(d, indent=1, spacer="\t", newlinechar=" ")
    print(output)
    assert output == 'MAP 	NAME "TEST" END'


def test_dump_with_end_comments():
    s = """MAP NAME "TEST" END"""

    d = mappyfile.loads(s)
    output = mappyfile.dumps(
        d, indent=1, spacer="\t", newlinechar=" ", end_comment=True
    )
    print(output)
    assert output == 'MAP 	NAME "TEST" END # MAP'


def test_create_map():
    d = mappyfile.utils.create("map")
    output = mappyfile.dumps(d, indent=0, newlinechar=" ", quote="'")
    print(output)
    assert (
        output
        == "MAP ANGLE 0 DEBUG 0 DEFRESOLUTION 72 IMAGETYPE 'png' MAXSIZE 4096 NAME 'MS' RESOLUTION 72 SIZE -1 -1 END"
    )


def test_create_layer():
    d = mappyfile.utils.create("layer")
    output = mappyfile.dumps(d, indent=0, newlinechar=" ", quote="'")
    print(output)
    assert output == "LAYER STATUS OFF TILEITEM 'location' UNITS METERS END"


def test_create_label():
    d = mappyfile.utils.create("label")
    output = mappyfile.dumps(d, indent=0, newlinechar=" ", quote="'")
    print(output)
    assert (
        output
        == "LABEL ANGLE 0 ANTIALIAS FALSE BACKGROUNDSHADOWSIZE FALSE BUFFER 0 FORCE FALSE MAXOVERLAPANGLE 22.5 MAXSIZE 256 MINSIZE 4 "
        "OFFSET 0 0 OUTLINEWIDTH 1 PARTIALS FALSE POSITION CC PRIORITY 1 REPEATDISTANCE 0 SHADOWSIZE 1 1 SIZE 10 END"
    )


def test_create_symbol():
    d = mappyfile.utils.create("symbol")
    output = mappyfile.dumps(d, indent=0, newlinechar=" ", quote="'")
    print(output)
    assert output == "SYMBOL ANCHORPOINT 0.5 0.5 ANTIALIAS FALSE FILLED FALSE END"


def test_create_symbol_v6():
    d = mappyfile.utils.create("symbol", version=6.0)
    output = mappyfile.dumps(d, indent=0, newlinechar=" ", quote="'")
    print(output)
    assert output == "SYMBOL ANTIALIAS FALSE FILLED FALSE END"


def test_create_symbol_v8():
    d = mappyfile.utils.create("symbol", version=8.0)
    output = mappyfile.dumps(d, indent=0, newlinechar=" ", quote="'")
    print(output)
    assert output == "SYMBOL ANCHORPOINT 0.5 0.5 FILLED FALSE END"


def test_create_missing():
    error_raised = False
    try:
        mappyfile.utils.create("missing")
    except SyntaxError:
        # raise
        error_raised = True

    assert error_raised is True


def run_tests():
    pytest.main(["tests/test_utils.py"])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # run_tests()
    test_loads_kwargs()
    print("Done!")
