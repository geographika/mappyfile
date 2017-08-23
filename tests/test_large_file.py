import logging
import cProfile

from mappyfile.parser import Parser
from mappyfile.pprint import PrettyPrinter
from mappyfile.transformer import MapfileToDict


def output(fn):
    """
    Parse, transform, and pretty print
    the result
    """
    p = Parser()
    m = MapfileToDict()

    ast = p.parse_file(fn)
    # print(ast)
    d = m.transform(ast)
    # print(d)
    pp = PrettyPrinter(indent=0, newlinechar=" ", quote="'")
    pp.pprint(d)


def main():
    fns = [r"D:\Temp\large_map1.txt", r"D:\Temp\large_map2.txt"]

    for fn in fns:
        pr = cProfile.Profile()
        pr.enable()
        output(fn)
        pr.disable()
        pr.print_stats(sort='time')


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
    print("Done!")
