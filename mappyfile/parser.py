import os
import logging
from io import open
from lark import Lark, ParseError, Tree
from lark.lexer import UnexpectedInput

log = logging.getLogger("mappyfile")


class Parser(object):

    def __init__(self, expand_includes=True, keep_comments=True):
        self.expand_includes = expand_includes
        self.keep_comments = keep_comments
        self._comments = []
        self.lalr = self._create_lalr_parser()

    def load_grammar(self, grammar_file):
        gf = os.path.join(os.path.dirname(__file__), grammar_file)
        return open(gf).read()

    def _create_lalr_parser(self):
        grammar_text = self.load_grammar("mapfile.lalr.g")
        if self.keep_comments:
            extra_args = dict(propagate_positions=True, lexer_callbacks={'COMMENT': self._comments.append})
        else:
            extra_args = {}
        return Lark(grammar_text, parser="lalr", lexer="contextual", **extra_args)

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
        Parse the Mapfile
        """

        if self.expand_includes:
            text = self.load_includes(text, fn=fn)

        try:
            self._comments[:] = []
            tree = self.lalr.parse(text)
            if self.keep_comments:
                assign_comments(tree, self._comments)
            return tree
        except (ParseError, UnexpectedInput) as ex:
            log.error("Parsing of Mapfile unsuccessful")
            log.info(ex)
            raise



def assign_comments(tree, comments):
    comments = list(comments)
    comments.sort(key=lambda c: c.line)

    idx_by_line = {0: 0}
    for i, c in enumerate(comments):
        if c.line not in idx_by_line:
            idx_by_line[c.line] = i
    idx = []
    for i in range(max(idx_by_line.keys()), 0, -1):
        if i in idx_by_line:
            idx.append( idx_by_line[i] )
        else:
            idx.append( idx[-1] )
    idx.append(0)
    idx.reverse()

    def _get_comments(from_line, to_line):
        if from_line >= len(idx):
            return []
        from_idx = idx[from_line]
        return comments[from_idx:idx[to_line]] if to_line < len(idx) else comments[from_idx:]

    def _assign_comments(_tree, prev_end_line):
        for node in _tree.children:
            try:
                line = node.line
            except AttributeError:
                assert not node.children
                continue

            node.line_comments = _get_comments(prev_end_line, line)
            if node.line == node.end_line:
                node.comments = _get_comments(line, line+1)
                prev_end_line = node.end_line + 1
            else:
                if isinstance(node, Tree):
                    _assign_comments(node, line)
                prev_end_line = node.end_line

    _assign_comments(tree, 0)
