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


    mapfiles = glob.glob(fld + '/**/*.map')
    mapfiles = [f for f in mapfiles if '.tmp.' not in f]

    mapfiles = [f for f in mapfiles if os.path.basename(f) == 'filters.map'] 

    for fn in mapfiles:
        print fn

        ast = parser.parse_file(fn)

        r = ast.select('composite_type *') #ast.select('attr_name')
        #print ast.__dict__
        ast.remove_kids_by_head("INCLUDE")
        print type(ast)
        print list(r)
        continue
        d = m.transform(ast)
        

        dpp = pprint.PrettyPrinter()
        print dpp.pprint(d)


        map_string = pp.pprint(d)

        print map_string

        output_file = fn.replace(".map", ".tmp.map")

        map_file = mappyfile.utils.write_map_to_file(map_string, output_file)

        utils.create_image_from_map(map_file) # fn for original map


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
    print("Done!")