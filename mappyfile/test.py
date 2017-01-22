import os
from io import open
from plyplus import Grammar, ParseError

TRY_PLY = True

grammar_text = open('mapfile.g').read()

g = Grammar(grammar_text, engine='pearley')
if TRY_PLY:
    ply_g = Grammar(grammar_text, engine='ply')

def parse_file(fn):
    fc = open(fn).read()
    if TRY_PLY:
        try:
            return ply_g.parse(fc+'\n')
        except ParseError:
            pass

    return g.parse(fc+'\n')


def main():
    DIR = '../tests/sample_maps/'
    for fn in os.listdir(DIR):
        print fn
        parse_file(DIR+fn)


if __name__ == '__main__':
    main()
