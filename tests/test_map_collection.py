import logging
import os
import cProfile
import glob2
import json
import mappyfile
from mappyfile.parser import Parser
from mappyfile.transformer import MapfileToDict
from mappyfile.validator import Validator
import pytest


def output(fn):
    """
    Parse, transform, and pretty print
    the result
    """
    p = Parser(expand_includes=False, include_comments=True)
    m = MapfileToDict(include_position=True, include_comments=True)
    v = Validator()

    try:
        ast = p.parse_file(fn)
        # print(ast)
        d = m.transform(ast)
        logging.debug("Number of layers: {}".format(len(d["layers"])))

        errors = v.validate(d, add_comments=True)
        assert(len(errors) == 0)

    except Exception as ex:
        logging.exception(ex)
        logging.warning("%s could not be successfully parsed", fn)
        d = None
        raise

    if d:
        try:
            s = mappyfile.utils.dumps(d)
        except Exception:
            logging.warning(json.dumps(d, indent=4))
            logging.warning("%s could not be successfully re-written", fn)
            raise

        # now try reading it again
        ast = p.parse(s)
        d = m.transform(ast)

        errors = v.validate(d)
        assert(len(errors) == 0)


def test_maps():
    sample_dir = os.path.join(os.path.dirname(__file__), "mapfiles")
    pth = sample_dir + r'/**/*.map'
    mapfiles = glob2.glob(pth)
    mapfiles = [f for f in mapfiles if "basemaps" not in f]

    for fn in mapfiles:
        logging.info("Processing {}".format(fn))
        fn = os.path.join(sample_dir, fn)
        pr = cProfile.Profile()
        pr.enable()
        output(fn)
        pr.disable()
        # pr.print_stats(sort='time')


def run_tests():
    pytest.main(["tests/test_map_collection.py"])


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    run_tests()
    print("Done!")
