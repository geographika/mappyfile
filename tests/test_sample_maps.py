import os
import logging
import pytest
import mappyfile
from mappyfile.parser import Parser
from mappyfile.transformer import MapfileToDict


def test_all_maps():

    sample_dir = os.path.join(os.path.dirname(__file__), "sample_maps")

    p = Parser(expand_includes=False)

    for fn in os.listdir(sample_dir):
        print(fn)
        try:
            p.parse_file(os.path.join(sample_dir, fn))
        except BaseException:
            logging.warning("Cannot process %s ", fn)
            raise


def test_includes():
    p = Parser()

    ast = p.parse_file('./tests/samples/include1.map')
    m = MapfileToDict()

    d = (m.transform(ast))  # works
    print(mappyfile.dumps(d))


def run_tests():
    pytest.main(["tests/test_sample_maps.py"])


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    test_all_maps()
    # run_tests()
    print("Done!")
