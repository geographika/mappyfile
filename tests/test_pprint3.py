from tests import sample_dict
from mappyfile.pprint import PrettyPrinter
import logging
from mappyfile.parser import Parser
from mappyfile.transformer import MapFile2Dict__Transformer
import pprint

logging.basicConfig(level=logging.DEBUG)


parser = Parser(try_ply=False)
ast = parser.parse_file('./tests/sample_maps/256_overlay_res.map')
ast = parser.parse_file('./tests/sample_maps/class16_oddscale.map')
ast = parser.parse_file('./tests/sample_maps/class16_range.map')
ast = parser.parse_file('./tests/sample_maps/wmsclient_3543.map')
ast = parser.parse_file('./tests/sample_maps/heat.map')

ast = parser.parse_file('./tests/sample_maps/labelpnt.map')
ast = parser.parse_file('./tests/sample_maps/maxfeatures.map')





m = MapFile2Dict__Transformer()
d = (m.transform(ast))

dpp = pprint.PrettyPrinter()
print dpp.pprint(d)

pp = PrettyPrinter()
print pp.pprint(d)

d = sample_dict.d4





#f = tempfile.NamedTemporaryFile(delete=False, suffix=".map")
#f.write(pp.pprint(map_))

print "Done!"
