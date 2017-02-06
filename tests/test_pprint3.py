from tests import sample_dict
from mappyfile.pprint import PrettyPrinter
import logging
from mappyfile.parser import Parser
from mappyfile.transformer import MapFile2Dict__Transformer
import pprint

def test():

    logging.basicConfig(level=logging.DEBUG)


    #parser = Parser(try_ply=True)
    #ast = parser.parse_file('./tests/sample_maps/256_overlay_res.map')
    #ast = parser.parse_file('./tests/sample_maps/class16_oddscale.map')
    #ast = parser.parse_file('./tests/sample_maps/class16_range.map')
    #ast = parser.parse_file('./tests/sample_maps/wmsclient_3543.map')
    #ast = parser.parse_file('./tests/sample_maps/heat.map')

    #ast = parser.parse_file('./tests/sample_maps/labelpnt.map')
    #ast = parser.parse_file('./tests/sample_maps/maxfeatures.map')

    #ast = parser.parse_file(r'C:\Temp\msautotest\query\include\bdry_counpy2_shapefile.map', is_subcomponent=True)


    #print ast.tail[0]
    #return
    cwd = r"C:\Temp\msautotest\query"
    parser = Parser(try_ply=True, cwd=cwd)

    ast = parser.parse_file('./tests/sample_maps/query.map')


    m = MapFile2Dict__Transformer()

    d = (m.transform(ast)) # works

    dpp = pprint.PrettyPrinter()
    print dpp.pprint(d)

    pp = PrettyPrinter()
    print pp.pprint(d)

    d = sample_dict.d4





    #f = tempfile.NamedTemporaryFile(delete=False, suffix=".map")
    #f.write(pp.pprint(map_))

test()
print "Done!"
