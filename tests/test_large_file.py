import os, logging
import pytest
import mappyfile
from mappyfile.parser import Parser
from mappyfile.transformer import MapfileToDict
from mappyfile.pprint import PrettyPrinter

def test_large_map(fn):

    p = Parser(expand_includes=False)

    try:

        p = Parser()
        m = MapfileToDict()
    
        ast = p.parse_file(fn)

        d = m.transform(ast)
        #print(d)
        pp = PrettyPrinter(indent=0, newlinechar=" ", quote="'")
        s = pp.pprint(d)
        print "hh"
        ast = p.parse(s)
        #print(ast)
        d = m.transform(ast)
        #print(d)
        pp = PrettyPrinter(indent=0, newlinechar=" ", quote="'")
        print(pp.pprint(d))

    except:
        logging.warning("Cannot process %s ", fn)
        raise

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    test_large_map(r"D:\Temp\corkcounty.map")
    print("Done!")