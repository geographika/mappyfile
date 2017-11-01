import os
import logging
from io import open
from lark import Lark, ParseError
from lark.lexer import UnexpectedInput

log = logging.getLogger("mappyfile")


class Parser(object):

    def __init__(self, expand_includes=True, use_lalr=True):
        self.expand_includes = expand_includes
        self.use_lalr = use_lalr

        if self.use_lalr:
            self.lalr = self._create_lalr_parser()
            self.earley = None  # only load this grammar as required
        else:
            self.earley = self._create_earley_parser()

    def load_grammar(self, grammar_file):
        gf = os.path.join(os.path.dirname(__file__), grammar_file)
        return open(gf).read()

    def _create_earley_parser(self):
        grammar_text = self.load_grammar("mapfile.earley.g")
        return Lark(grammar_text, parser="earley", lexer="standard", earley__all_derivations=False)

    def _create_lalr_parser(self):
        grammar_text = self.load_grammar("mapfile.lalr.g")
        return Lark(grammar_text, parser="lalr", lexer="contextual")

    def _strip_quotes(self, s):
        s = s[:s.index('#')] if '#' in s else s
        return s.strip("'").strip('"')

    def load_includes(self, text, fn=None, _nested_includes=0):
        # Per default use working directory of the process
        if fn is None:
            fn = os.getcwd()
        lines = text.split('\n')
        includes = {}
        for idx, l in enumerate(lines):
            if l.strip().lower().startswith("include"):
                if _nested_includes == 5:
                    raise Exception("Maximum nested include exceeded! (MaxNested=5)")

                inc, inc_file_path = l.split()
                inc_file_path = self._strip_quotes(inc_file_path)
                if not os.path.isabs(inc_file_path):
                    inc_file_path = os.path.join(os.path.dirname(fn), inc_file_path)
                try:
                    include_text = self.open_file(inc_file_path)
                except IOError as ex:
                    log.warning("Include file '%s' not found", inc_file_path)
                    raise ex
                # recursively load any further includes
                includes[idx] = self.load_includes(include_text, fn=fn, _nested_includes=_nested_includes+1)

        for idx, txt in includes.items():
            lines.pop(idx)  # remove the original include
            lines.insert(idx, txt)
        return '\n'.join(lines)

    def open_file(self, fn):
        try:
            # specify Unicode for Python 2.7
            return open(fn, "r", encoding="utf-8").read()
        except UnicodeDecodeError as ex:
            log.debug(ex)
            log.error("Please check the encoding for %s. All Mapfiles should be in utf-8 format.", fn)
            raise

    def parse_file(self, fn):
        text = self.open_file(fn)
        return self.parse(text, fn=fn)

    def parse(self, text, fn=None):
        """
        Parse the Mapfile, using one of three options, from the quickest (LALR)
        to slowest, but handles all cases
        """

        if self.expand_includes:
            text = self.load_includes(text, fn=fn)

        if self.use_lalr:
            try:
                return self.lalr.parse(text)
            except (ParseError, UnexpectedInput) as ex:
                log.error("Parsing with LALR unsuccessful")
                log.info(ex)

        log.info("Attempting to parse with Earley")

        if self.earley is None:
            self.earley = self._create_earley_parser()

        try:
            ast = self.earley.parse(text)
            log.info("Parsing with Earley successful")
            return ast
        except (ParseError, UnexpectedInput) as ex:
            log.exception(ex)
            log.error("Parsing with Earley unsuccessful")
            raise
