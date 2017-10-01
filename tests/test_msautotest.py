"""
Parse all the test Mapfiles in msautotests, write them to a new file,
and then test that these also parse correctly
"""
import os
import logging
import glob
import shutil
import json

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

    msautotest_copy = os.path.join(os.path.dirname(msautotest_fld), "msautotest_mappyfile")

    if create_new_copy:
        create_copy(msautotest_fld, msautotest_copy)

    parser = Parser()
    transformer = MapfileToDict()
    pp = PrettyPrinter()

    # these two maps aren't in utf8
    # see https://github.com/mapserver/mapserver/pull/5460
    # ignore_list = ["wms_inspire_scenario1.map","wms_inspire_scenario2.map"]

    # transparent_layer.map has an extra END, see https://github.com/mapserver/mapserver/pull/5468
    # polyline_no_clip.map needs symbol names in quotes

    ignore_list = ["poly-label-multiline-pos-auto.map", "poly-label-pos-auto.map"]  # has attributes all on the same line

    mapfiles = glob.glob(msautotest_fld + '/**/*.map')
    mapfiles = [f for f in mapfiles if os.path.basename(f) not in ignore_list]

    # target_map = "wms_grid_reproj_to_3857.map" # "polyline_no_clip.map"
    # mapfiles = [f for f in mapfiles if os.path.basename(f) in (target_map)]

    v = Validator()

    for fn in mapfiles:

        d = parse_mapfile(parser, transformer, pp, fn)
        if not v.validate(d):
            logging.warning(json.dumps(d, indent=4))
            # raise

        output_file = fn.replace(msautotest_fld, msautotest_copy)
        try:
            print(mappyfile.dumps(d))
            mappyfile.utils.write(d, output_file)
        except Exception:
            logging.warning(json.dumps(d, indent=4))
            logging.warning("%s could not be successfully re-written", fn)
            raise

        # now try reading it again
        print(d)
        print(json.dumps(d, indent=4))
        d = parse_mapfile(parser, transformer, pp, output_file)

        if not v.validate(d):
            logging.warning(json.dumps(d, indent=4))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    fld = r"D:\GitHub\mapserver\msautotest"
    main(fld, False)
    print("Done!")
