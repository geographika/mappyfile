import os
from pprint import pprint
from collections import defaultdict
from plyplus import STransformer, is_stree

from tokens import ATTRIBUTE_NAMES, COMPOSITE_NAMES
from parser import Parser

from transformer import MapFile2Dict__Transformer

parser = Parser(try_ply=False)
ast = parser.parse_file('../tests/sample_maps/labels-bitmap-multiline.map')

m = MapFile2Dict__Transformer()
pprint (m.transform(ast))

def main():
    DIR = '../tests/sample_maps/'
    for fn in os.listdir(DIR):
        print fn
        ast = parser.parse_file(DIR+fn)
        (m.transform(ast))


if __name__ == '__main__':
    main()
