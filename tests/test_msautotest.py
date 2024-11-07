r"""
Parse all the test Mapfiles in msautotests, write them to a new file,
and then test that these also parse correctly

Setup instructions:

- clone the MapServer repository https://github.com/mapserver/mapserver
- point the ``fld`` variable at the bottom of this file to the location of msautotest
- if requried set the ``create_new_copy`` to True on the first run to avoid modifying the original files

Check the WARNING output for parsing errors
"""

import os
import logging
import glob
import shutil
from mappyfile.pprint import PrettyPrinter
from mappyfile.parser import Parser
from mappyfile.transformer import MapfileToDict
from mappyfile.validator import Validator
import mappyfile


def create_copy(msautotest_fld, msautotest_copy):
    # first make a backup copy of msautotest

    if os.path.isdir(msautotest_copy):
        shutil.rmtree(msautotest_copy)
        logging.info("Removing %s...", msautotest_copy)

    logging.info("Copying %s to %s...", msautotest_fld, msautotest_copy)
    shutil.copytree(msautotest_fld, msautotest_copy)
    logging.info("Copying complete!")

    return msautotest_copy


def parse_mapfile(parser, transformer, pp, fn):
    logging.debug("Parsing %s", fn)

    try:
        ast = parser.parse_file(fn)
    except Exception as ex:
        logging.warning("%s could not be successfully parsed", fn)
        logging.exception(ex)
        raise

    try:
        d = transformer.transform(ast)
    except Exception as ex:
        logging.warning("%s could not be successfully transformed", fn)
        logging.exception(ex)
        raise

    return d


def main(msautotest_fld, create_new_copy=True):
    msautotest_copy = os.path.join(
        os.path.dirname(msautotest_fld), "msautotest_mappyfile"
    )

    if create_new_copy:
        create_copy(msautotest_fld, msautotest_copy)

    parser = Parser()
    transformer = MapfileToDict()
    pp = PrettyPrinter()

    # list of Maps we cannot currently parse with mappyfile
    ignore_list = ["centerline.map"]

    mapfiles = glob.glob(msautotest_fld + "/**/*.map")
    mapfiles = [f for f in mapfiles if os.path.basename(f) not in ignore_list]

    v = Validator()

    for fn in mapfiles:
        d = parse_mapfile(parser, transformer, pp, fn)
        errors = v.validate(d, add_comments=True)
        if errors:
            logging.warning("{} failed validation".format(fn))

        output_file = fn.replace(msautotest_fld, msautotest_copy)
        try:
            mappyfile.save(d, output_file)
        except Exception:
            logging.warning(d)
            logging.warning("%s could not be successfully re-written", fn)
            raise

        # now try reading it again
        # print(d)
        d = parse_mapfile(parser, transformer, pp, output_file)

        errors = v.validate(d, add_comments=True)
        if errors:
            logging.warning("{} failed validation".format(fn))
            logging.warning(errors)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    fld = r"D:\GitHub\mapserver\msautotest"
    main(fld, create_new_copy=False)
    print("Done!")
