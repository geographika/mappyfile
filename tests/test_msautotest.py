"""
Parse all the test Mapfiles in msautotests, write them to a new file,
and then test that these also parse correctly
"""
import os
import logging
import glob
import shutil

from mappyfile.pprint import PrettyPrinter
from mappyfile.parser import Parser
from mappyfile.transformer import MapfileToDict
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
        # print(ast)
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

    # map_string = pp.pprint(d)
    # print(map_string)

    return d


def main(msautotest_fld, create_new_copy=True):

    msautotest_copy = os.path.join(
        os.path.dirname(msautotest_fld),
        "msautotest_mappyfile")

    if create_new_copy:
        create_copy(msautotest_fld, msautotest_copy)

    parser = Parser()
    transformer = MapfileToDict()
    pp = PrettyPrinter()

    # these two maps aren't in utf8
    # see https://github.com/mapserver/mapserver/pull/5460
    # ignore_list = ["wms_inspire_scenario1.map","wms_inspire_scenario2.map"]
    ignore_list = []

    mapfiles = glob.glob(msautotest_fld + '/**/*.map')
    mapfiles = [f for f in mapfiles if os.path.basename(f) not in ignore_list]

    for fn in mapfiles:

        d = parse_mapfile(parser, transformer, pp, fn)
        output_file = fn.replace(msautotest_fld, msautotest_copy)
        mappyfile.utils.write(d, output_file)

        # now try reading it again
        d = parse_mapfile(parser, transformer, pp, output_file)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    fld = r"D:\GitHub\mapserver\msautotest"
    main(fld, True)
    print("Done!")
