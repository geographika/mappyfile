import os, logging
import pytest
from mappyfile.parser import Parser
from mappyfile.pprint import PrettyPrinter
import mappyfile
from mappyfile.transformer import MapfileToDict

import cProfile


def output():
    """
    Parse, transform, and pretty print 
    the result
    """
    p = Parser()
    m = MapfileToDict()
    
    fn = r"D:\Temp\large.map"
    with open(fn) as f:
        s = f.read()

    ast = p.parse(s)
    ##print(ast)
    d = m.transform(ast)
    ##print(d)
    pp = PrettyPrinter(indent=0, newlinechar=" ", quote="'")
    pp.pprint(d)

if __name__ == "__main__":
    
    pr = cProfile.Profile()
    pr.enable()

    #cProfile.run('output()')
    output()
    pr.disable()
    pr.print_stats(sort='time')
