import os, logging, glob, json, shutil

from mappyfile.pprint import PrettyPrinter
from mappyfile.parser import Parser
from mappyfile.transformer import MapfileToDict
import pprint
import mappyfile
from subprocess import Popen, PIPE
import tempfile

def create_image_from_map(map_file, dll_location):

    of = tempfile.NamedTemporaryFile(delete=False, suffix=".png", prefix="tmp_")
    of.close()

    logging.debug("Creating file %s", of.name)
    # [SHP2IMG] -m [MAPFILE] -i png -o [RESULT]
    params = ["shp2img","-m", map_file,"-i","png","-o", of.name]

    os.environ['PATH'] = dll_location + ';' + os.environ['PATH']
    os.environ['PROJ_LIB'] = os.path.join(dll_location, "proj\SHARE")

    logging.debug(" ".join(params))

    p = Popen(params, stdout=PIPE, bufsize=1)
    with p.stdout:
        print(map_file)
        for line in iter(p.stdout.readline, b''):
            print(line)

    p.wait() # wait for the subprocess to exit

    #os.startfile(of.name)

def create_copy(msautotest_fld):

    # first make a backup copy of msautotest
    msautotest_copy = os.path.join(os.path.dirname(msautotest_fld), "msautotest_mappyfile")

    if os.path.isdir(msautotest_copy):
        shutil.rmtree(msautotest_copy)
        logging.info("Removing %s...", msautotest_copy)

    logging.info("Copying %s to %s...", msautotest_fld, msautotest_copy)
    shutil.copytree(msautotest_fld, msautotest_copy)
    logging.info("Copying complete!")

    return msautotest_copy

def main(msautotest_fld, dll_location):

    msautotest_copy = create_copy(msautotest_fld)

    parser = Parser()
    transformer = MapfileToDict()
    pp = PrettyPrinter()

    ignore_list = ["wms_inspire_scenario1.map","wms_inspire_scenario2.map"] # these two maps aren't in utf8
    #ignore_list = []

    mapfiles = glob.glob(msautotest_fld + '/**/*.map')
    #mapfiles = [f for f in mapfiles if '.tmp.' not in f]
    mapfiles = [f for f in mapfiles if os.path.basename(f) not in ignore_list]
    
    for fn in mapfiles:
        logging.debug("Parsing %s", fn)
        ast = parser.parse_file(fn)
        #print ast
        #r = ast.select('composite_type *') #ast.select('attr_name')
        #continue

        try:
            d = transformer.transform(ast)
        except Exception as ex:
            logging.warning("%s could not be successfully transformed", fn)
            logging.exception(ex)
            raise
        
        #dpp = pprint.PrettyPrinter()
        #print(dpp.pprint(d))

        map_string = pp.pprint(d)
        #print(map_string)

        output_file = fn.replace(msautotest_fld, msautotest_copy)
        mf = mappyfile.utils.write(d, output_file)
        #create_image_from_map(mf, dll_location) # fn for original map

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    fld = r"D:\GitHub\mapserver\msautotest"
    dll_location = r"C:\MapServer\bin"
    main(fld, dll_location)
    print("Done!")