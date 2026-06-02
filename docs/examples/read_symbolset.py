from mappyfile.pprint import PrettyPrinter

import mappyfile

fn = "./docs/examples/symbols.sym"
mf = mappyfile.open(fn)
pp = PrettyPrinter()
print(pp.pprint(mf))
