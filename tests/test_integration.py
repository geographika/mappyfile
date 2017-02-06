import os, logging, glob, json
from mappyfile.pprint import PrettyPrinter
from mappyfile.parser import Parser
from mappyfile.transformer import MapfileToDict
import pprint
import mappyfile
from subprocess import Popen, PIPE
import tempfile

def create_image_from_map(map_file):

    of = tempfile.NamedTemporaryFile(delete=False, suffix=".png", prefix="tmp_")
    of.close()

    logging.debug("Creating file %s", of.name)

    params = ["shp2img","-m", map_file,"-i","png","-o", of.name]

    dll_location = r"C:\MapServer\bin"
    os.environ['PATH'] = dll_location + ';' + os.environ['PATH']
    os.environ['PROJ_LIB'] = os.path.join(dll_location, "proj\SHARE")

    logging.debug(" ".join(params))

    # [SHP2IMG] -m [MAPFILE] -i png -o [RESULT]

    #p = subprocess.Popen(params)

    p = Popen(params, stdout=PIPE, bufsize=1)
    with p.stdout:
        print map_file
        #logging.info("Messages for %s", map_file)
        for line in iter(p.stdout.readline, b''):
            print line,

    p.wait() # wait for the subprocess to exit

    #os.startfile(of.name)

def main():

    parser = Parser(try_ply=False)
    transformer = MapfileToDict()
    pp = PrettyPrinter()
    fld = r"C:\Temp\msautotest"

    ignore_list = ["wms_inspire_scenario1.map","wms_inspire_scenario2.map"]

    mapfiles = glob.glob(fld + '/**/*.map')

    mapfiles = [f for f in mapfiles if '.tmp.' not in f]

    mapfiles = [f for f in mapfiles if os.path.basename(f) not in ignore_list]
    
    #mapfiles = [f for f in mapfiles if os.path.basename(f) == 'runtime_sub.map'] 


    for fn in mapfiles:
        #print fn
        ast = parser.parse_file(fn)

        #r = ast.select('composite_type *') #ast.select('attr_name')

        try:
            d = transformer.transform(ast)
        except Exception as ex:
            logging.warning("%s could not be successfully transformed", fn)
            logging.exception(ex)
            raise
        
        #dpp = pprint.PrettyPrinter()
        #print dpp.pprint(d)

        map_string = pp.pprint(d)
        #print map_string

        output_file = fn.replace(".map", ".tmp.map")
        mf = mappyfile.utils.write(d, output_file)
        create_image_from_map(mf) # fn for original map

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
    print("Done!")