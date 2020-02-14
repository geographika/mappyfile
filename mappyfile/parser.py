# =================================================================
#
# Authors: Seth Girvin, Erez Shinan
#
# Copyright (c) 2020 Seth Girvin
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

import os
import sys
import logging
from io import open
from lark import Lark, ParseError, Tree, UnexpectedInput


PY2 = sys.version_info[0] < 3
if not PY2:
    unicode = str # NOQA


log = logging.getLogger("mappyfile")


class Parser(object):

    def __init__(self, expand_includes=True, include_comments=False, **kwargs):
        self.expand_includes = expand_includes
        self.include_comments = include_comments
        self._comments = []
        self.lalr = self._create_lalr_parser()

    def load_grammar(self, grammar_file):
        gf = os.path.join(os.path.dirname(__file__), grammar_file)
        return open(gf).read()

    def _create_lalr_parser(self):
        grammar_text = self.load_grammar("mapfile.lalr.g")
        if self.include_comments:
            callbacks = {'COMMENT': self._comments.append, 'CCOMMENT': self._comments.append}
            extra_args = dict(propagate_positions=True, lexer_callbacks=callbacks)
        else:
            extra_args = {}
        return Lark(grammar_text, parser="lalr", lexer="contextual", **extra_args)

    def _get_include_filename(self, line):

        if "#" in line:
            # remove any comments on the same line
            line = line.split("#")[0]

        include_pairs = line.split()
        if len(include_pairs) > 2:
            log.warning("Multiple include files have been found on the same line. "
                        "Only the first will be used. ")
        inc_file_path = include_pairs[1]

        return inc_file_path.strip("'").strip('"')

    def load_includes(self, text, fn=None, _nested_includes=0):
        # Per default use working directory of the process
        if fn is None:
            fn = os.getcwd() + os.sep

        lines = text.split('\n')
        includes = {}
        for idx, l in enumerate(lines):
            if l.strip().lower().startswith("include"):
                if _nested_includes == 5:
                    raise Exception("Maximum nested include exceeded! (MaxNested=5)")

                inc_file_path = self._get_include_filename(l)

                if not os.path.isabs(inc_file_path):
                    inc_file_path = os.path.abspath(os.path.join(os.path.dirname(fn), inc_file_path))
                try:
                    include_text = self.open_file(inc_file_path)
                except IOError as ex:
                    log.warning("Include file '%s' not found in '%s'", inc_file_path, fn)
                    raise ex
                # recursively load any further includes
                includes[idx] = self.load_includes(include_text, fn=fn, _nested_includes=_nested_includes+1)

        for idx, txt in includes.items():
            lines.pop(idx)  # remove the original include
            lines.insert(idx, txt)
        return '\n'.join(lines)

    def assign_comments(self, tree, comments):
        """
        Capture any comments in the tree

        header_comments stores comments preceding a node

        """
        comments = list(comments)
        comments.sort(key=lambda c: c.line)

        idx_by_line = {0: 0}  # {line_no: comment_idx}

        for i, c in enumerate(comments):
            if c.line not in idx_by_line:
                idx_by_line[c.line] = i

        idx = []

        # convert comment tokens to strings, and remove any line breaks
        self.comments = [c.value.strip() for c in comments]
        last_comment_line = max(idx_by_line.keys())

        # make a list with an entry for each line
        # number associated with a comment list index

        for i in range(last_comment_line, 0, -1):
            if i in idx_by_line:
                # associate line with new comment
                idx.append(idx_by_line[i])
            else:
                # associate line with following comment
                idx.append(idx[-1])

        idx.append(0)  # line numbers start from 1
        idx.reverse()
        self.idx = idx
        self._assign_comments(tree, 0)

    def _get_comments(self, from_line, to_line):

        idx = self.idx
        comments = self.comments

        if from_line >= len(idx):
            return []  # no more comments

        from_idx = idx[from_line]

        if to_line < len(idx):
            associated_comments = comments[from_idx:idx[to_line]]
        else:
            # get all remaining comments
            associated_comments = comments[from_idx:]

        return associated_comments

    def _assign_comments(self, _tree, prev_end_line):

        for node in _tree.children:
            if not isinstance(node, Tree):
                continue

            try:
                line = node.meta.line
            except AttributeError:
                assert not node.children
                continue

            if node.data not in ("composite", "attr", "string_pair"):
                if isinstance(node, Tree):
                    self._assign_comments(node, prev_end_line)
                    continue

            node.meta.header_comments = self._get_comments(prev_end_line, line)
            if node.meta.line == node.meta.end_line:
                # node is on a single line, so check for inline comments
                node.meta.inline_comments = self._get_comments(line, line + 1)
                prev_end_line = node.meta.end_line + 1
            else:
                if isinstance(node, Tree):
                    self._assign_comments(node, line)
                prev_end_line = node.meta.end_line

    def load(self, fp):
        text = fp.read()
        if hasattr(fp, 'name'):
            fn = fp.name  # name is a read-only attribute and may not be present on all file-like objects.
        else:
            fn = None
        return self.parse(text, fn)

    def open_file(self, fn):
        try:
            # specify Unicode for Python 2.7
            with open(fn, "r", encoding="utf-8") as f:
                return f.read()
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

        if PY2 and not isinstance(text, unicode):
            # specify Unicode for Python 2.7
            text = unicode(text, 'utf-8')

        if self.expand_includes:
            text = self.load_includes(text, fn=fn)

        try:
            self._comments[:] = []  # clear any comments from a previous parse
            tree = self.lalr.parse(text)
            if self.include_comments:
                self.assign_comments(tree, self._comments)
            return tree
        except (ParseError, UnexpectedInput) as ex:
            if fn:
                log.error("Parsing of {} unsuccessful".format(fn))
            else:
                log.error("Parsing of Mapfile unsuccessful")
            log.info(ex)
            raise
