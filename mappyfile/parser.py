import os
import logging
from io import open
from lark import Lark
import re

try:
    from StringIO import StringIO
except ImportError:
    # Python3
    from io import StringIO


class Parser(object):

    def __init__(self, expand_includes=True):
        self.expand_includes = expand_includes
        self.g = self.load_grammar("mapfile.g")
        self._nested_include = 0

    def load_grammar(self, grammar_file):
        gf = os.path.join(os.path.dirname(__file__), grammar_file)
        grammar_text = open(gf).read()
        return Lark(grammar_text, parser="earley", lexer="standard")

    def _strip_quotes(self, s):
        s = s[:s.index('#')] if '#' in s else s
        return s.strip("'").strip('"')

    def load_includes(self, text, fn=None):
        # Per default use working directory of the process
        if fn is None:
            fn = os.getcwd()
        lines = text.split('\n')
        includes = {}
        include_discovered = False
        for idx, l in enumerate(lines):
            if l.strip().lower().startswith("include"):
                if not include_discovered:
                    include_discovered = True
                    self._nested_include += 1
                if self._nested_include > 5:
                    raise Exception("Maximum nested include exceeded! (MaxNested=5)")

                inc, inc_file_path = l.split()
                inc_file_path = self._strip_quotes(inc_file_path)
                if not os.path.isabs(inc_file_path):
                    inc_file_path = os.path.join(os.path.dirname(fn), inc_file_path)
                try:
                    include_text = self.open_file(inc_file_path)
                except IOError as ex:
                    logging.warning("Include file '%s' not found", inc_file_path)
                    raise ex
                # recursively load any further includes
                includes[idx] = self.load_includes(include_text, fn=inc_file_path)

        for idx, txt in includes.items():
            lines.pop(idx)  # remove the original include
            lines.insert(idx, txt)
        return '\n'.join(lines)

    def open_file(self, fn):
        try:
            # specify Unicode for Python 2.7
            return open(fn, "r", encoding="utf-8").read()
        except UnicodeDecodeError as ex:
            logging.debug(ex)
            logging.error("Please check the encoding for %s. All Mapfiles should be in utf-8 format.", fn)
            raise

    def parse_file(self, fn):
        self._nested_include = 0
        text = self.open_file(fn)
        return self.parse(text, fn=fn)

    def parse(self, text, fn=None):
        self._nested_include = 0
        if self.expand_includes:
            text = self.load_includes(text, fn=fn)

        return self.g.parse(text)
