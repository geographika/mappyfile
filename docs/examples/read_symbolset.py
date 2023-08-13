from mappyfile.pprint import PrettyPrinter

import mappyfile

fn = r"D:\TFS\hymo\mapfiles\symbols\symbols.sym"
mf = mappyfile.open(fn)
pp = PrettyPrinter()
print(pp.pprint(mf))
