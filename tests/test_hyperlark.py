import os
import sys
import glob
import json
import logging
import subprocess
import importlib.util
import pytest
import mappyfile
from mappyfile.parser import hyperlark, lark_cython

needs_hyperlark = pytest.mark.skipif(
    importlib.util.find_spec("hyperlark") is None, reason="Hyperlark is not installed"
)

HAS_CYTHON = importlib.util.find_spec("lark_cython") is not None


def print_engines():
    """Print whether mappyfile parses with Hyperlark, and whether with lark_cython"""
    print(json.dumps([bool(hyperlark), bool(lark_cython)]))


def print_dicts():
    """
    Print the dicts of the test Mapfiles, and of a CONFIG and a SYMBOLSET file,
    with and without comments and positions
    """
    files = sorted(glob.glob("./tests/mapfiles/*.map")) + [
        "./tests/samples/configs/config1.cfg",
        "./docs/examples/symbols.sym",
    ]
    dicts = {}
    for fn in files:
        for comments in (False, True):
            for position in (False, True):
                d = mappyfile.open(
                    fn,
                    expand_includes=False,
                    include_comments=comments,
                    include_position=position,
                )
                dicts[f"{fn} comments={comments} position={position}"] = repr(d)
    print(json.dumps(dicts))


def run(code, use_hyperlark=None, use_cython=None):
    """
    Run code in a new process, as mappyfile picks its parsing engine on import,
    and return the JSON it prints
    """
    env = dict(os.environ)
    for name, value in [
        ("MAPPYFILE_USE_HYPERLARK", use_hyperlark),
        ("MAPPYFILE_USE_CYTHON", use_cython),
    ]:
        env.pop(name, None)
        if value is not None:
            env[name] = value
    result = subprocess.run(
        [sys.executable, "-c", code], env=env, capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


ENGINES = "from tests.test_hyperlark import print_engines; print_engines()"
DICTS = "from tests.test_hyperlark import print_dicts; print_dicts()"


@needs_hyperlark
def test_used_when_installed():
    assert run(ENGINES) == [True, False]  # in place of lark_cython


def test_disabled():
    assert run(ENGINES, use_hyperlark="False") == [False, HAS_CYTHON]


def test_not_installed():
    code = "import sys; sys.modules['hyperlark'] = None; " + ENGINES
    assert run(code) == [False, HAS_CYTHON]


@needs_hyperlark
def test_same_as_lark():
    assert run(DICTS) == run(DICTS, use_hyperlark="False", use_cython="False")


def run_tests():
    pytest.main(["tests/test_hyperlark.py"])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_tests()
    print("Done!")
