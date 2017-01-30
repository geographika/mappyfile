import os
from io import open
from plyplus import Grammar, ParseError

class Parser(object):

    def __init__(self, try_ply=True):
        self.try_ply = try_ply

        gf = os.path.join(os.path.dirname(__file__), "mapfile.g")
        grammar_text = open(gf).read()

        self.g = Grammar(grammar_text, engine='pearley')
        if self.try_ply:
            self.ply_g = Grammar(grammar_text, engine='ply')

    def parse_file(self, fn):
        text = open(fn, "r", encoding="utf-8").read() # specify utf for Python 2.7
        return self.parse(text)

    def parse(self, text):
        if self.try_ply:
            try:
                return self.ply_g.parse(text+'\n')
            except ParseError:
                pass

        return self.g.parse(text+'\n')