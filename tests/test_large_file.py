import logging
import os
import cProfile
import glob
import json
import mappyfile
from mappyfile.parser import Parser
from mappyfile.transformer import MapfileToDict
from mappyfile.validator import Validator


def output(fn):
    """
    Parse, transform, and pretty print
    the result
    """
    p = Parser(expand_includes=False)
    m = MapfileToDict()
    v = Validator()

    ast = p.parse_file(fn)
    # print(ast)
    d = m.transform(ast)

    errors = v.validate(d)
    assert(len(errors) == 0)

    output_file = fn + ".map"

    try:
        mappyfile.utils.write(d, output_file)
    except Exception:
        logging.warning(json.dumps(d, indent=4))
        logging.warning("%s could not be successfully re-written", fn)
        raise

    # now try reading it again
    ast = p.parse_file(output_file)
    d = m.transform(ast)

    errors = v.validate(d)
    assert(len(errors) == 0)


def main():
    sample_dir = os.path.join(os.path.dirname(__file__), "mapfiles")
    mapfiles = glob.glob(sample_dir + '/*.txt')
    # mapfiles = ["map4.txt"]

    for fn in mapfiles:
        print("Processing {}".format(fn))
        fn = os.path.join(sample_dir, fn)
        pr = cProfile.Profile()
        pr.enable()
        output(fn)
        pr.disable()
        # pr.print_stats(sort='time')


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
    print("Done!")
