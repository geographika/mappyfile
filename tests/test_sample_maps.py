import os
import logging
import pytest
import mappyfile
from mappyfile.parser import Parser
from mappyfile.transformer import MapfileToDict
from lark.common import UnexpectedToken


def test_all_maps():

    sample_dir = os.path.join(os.path.dirname(__file__), "sample_maps")

    p = Parser(expand_includes=False)

    failing_maps = []

    for fn in os.listdir(sample_dir):
        print(fn)
        try:
            p.parse_file(os.path.join(sample_dir, fn))
        except (BaseException, UnexpectedToken):
            logging.warning("Cannot process %s ", fn)
            failing_maps.append(fn)

    logging.warning(failing_maps)


def test_includes():
    p = Parser()

    ast = p.parse_file('./tests/samples/include1.map')
    m = MapfileToDict()

    d = (m.transform(ast))  # works
    print(mappyfile.dumps(d))


def test_includes_nested_path():
    p = Parser()

    ast = p.parse_file('./tests/samples/include1_nested_path.map')
    m = MapfileToDict()

    d = (m.transform(ast))  # works
    print(mappyfile.dumps(d))


def test_includes_max_recursion():
    p = Parser()

    with pytest.raises(Exception) as excinfo:
        p.parse_file('./tests/samples/include1_recursive.map')

    assert 'Maximum nested include exceeded' in str(excinfo.value)


def run_tests():
    pytest.main(["tests/test_sample_maps.py"])


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    test_all_maps()
    print("Done!")
