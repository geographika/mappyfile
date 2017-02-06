import os, logging
from mappyfile.pprint import PrettyPrinter
from mappyfile.parser import Parser

from mappyfile.transformer import MapFile2Dict__Transformer
import glob
import json
import pprint
import mappyfile
from tests import utils

parser = Parser(try_ply=False)
ast = parser.parse_file('./tests/sample_maps/labels-bitmap-multiline.map')

m = MapFile2Dict__Transformer()
d = (m.transform(ast))

#print pprint(d, indent=4)


# valid JSON
#print json.dumps(d, indent=4)



def main():
    DIR = './tests/sample_maps/'
    pp = PrettyPrinter()
    fld = r"C:\Temp\msautotest"

    ignore_list = ["wms_inspire_scenario1.map","wms_inspire_scenario2.map"]

    mapfiles = glob.glob(fld + '/**/*.map')
    mapfiles = [f for f in mapfiles if '.tmp.' not in f]

    mapfiles = [f for f in mapfiles if os.path.basename(f) not in ignore_list]
    
    mapfiles = [f for f in mapfiles if os.path.basename(f) == 'runtime_sub.map'] 
    # filters.map loadLayer(): Unknown identifier. Parsing error near (i):(line 15) <br>
    # wms_inspire_scenario1.map UnicodeDecodeError: 'utf8' codec can't decode byte 0xdf in position 7851: invalid continuation byte

    for fn in mapfiles:
        print fn

        ast = parser.parse_file(fn)

        #r = ast.select('composite_type *') #ast.select('attr_name')
        #print ast.__dict__
        
        #ast.remove_kids_by_head("INCLUDE")
        #print type(ast)
        #print list(r)
        #continue

        try:
            d = m.transform(ast)
        except Exception as ex:
            print fn
            logging.exception(ex)
            raise
        

        dpp = pprint.PrettyPrinter()
        #print dpp.pprint(d)


        map_string = pp.pprint(d)

        #print map_string

        output_file = fn.replace(".map", ".tmp.map")

        map_file = mappyfile.utils.save(map_string, output_file)

        utils.create_image_from_map(map_file) # fn for original map


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
    print("Done!")