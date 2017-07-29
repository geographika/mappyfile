import os, logging
from io import open
from lark import Lark, ParseError
import re

try:
    from StringIO import StringIO
except ImportError:
    # Python3
    from io import StringIO

class Parser(object):

    def __init__(self, cwd="", expand_includes=True, add_linebreaks=False):
        self.cwd = cwd
        self.expand_includes = expand_includes
        self.add_linebreaks = add_linebreaks
        self.g = self.load_grammar("mapfile.g")

        
    def load_grammar(self, grammar_file):

        gf = os.path.join(os.path.dirname(__file__), grammar_file)
        grammar_text = open(gf).read()

        return Lark(grammar_text, parser='earley', lexer='standard')

    def strip_quotes(self, s):
        return s.strip("'").strip('"')

    def load_includes(self, text):

        lines = text.split('\n')
        includes = {}

        for idx, l in enumerate(lines):
            if l.strip().lower().startswith('include'):
                if '#' in l:
                    l = l[:l.index('#')]

                parts = [p for p in l.split()]

                assert (len(parts) == 2)
                assert (parts[0].lower() == 'include')
                fn = os.path.join(self.cwd, self.strip_quotes(parts[1]))
                try:
                    include_text = self.open_file(fn)
                except IOError as ex:
                    logging.warning("Include file '%s' not found", fn)
                    raise ex
                # recursively load any further includes
                includes[idx] = self.load_includes(include_text)
    
        for idx, txt in includes.items():
            lines.pop(idx) # remove the original include
            lines.insert(idx, txt)

        return '\n'.join(lines)

    def open_file(self, fn):
        try:
            return open(fn, "r", encoding="utf-8").read() # specify Unicode for Python 2.7
        except UnicodeDecodeError as ex:
            logging.debug(ex)
            logging.error("Please check the encoding for %s. All Mapfiles should be in utf-8 format. ", fn)
            raise

    def parse_file(self, fn):

        self.cwd = os.path.dirname(fn)

        text = self.open_file(fn)
        return self.parse(text)

    def add_linebreaks(self, text):
        """
        Add a line-break before each END keyword to speed-up parsing
        """
        pattern = re.compile(r'\bEND\b', re.IGNORECASE)

        text = StringIO(text)
        new_lines = []
        for line in text:
            parts = line.split('#')
            parts[0] = pattern.sub('\nEND', parts[0])
            new_lines.append('#'.join(parts))

        return "\n".join(new_lines)

    def parse(self, text):

        if self.expand_includes == True:
            text = self.load_includes(text)

        if self.add_linebreaks:
            text = self.add_linebreaks(text)

        return self.g.parse(text)