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

from __future__ import annotations
import os
import logging
from io import open
from lark import Lark, ParseError, Tree, UnexpectedInput
from typing import Any, IO


try:
    import lark_cython
except ImportError:
    lark_cython = None


log = logging.getLogger("mappyfile")

SYMBOL_ATTRIBUTES = {
    "ANCHORPOINT",
    "ANTIALIAS",
    "FILLED",
    "FONT",
    "IMAGE",
    "NAME",
    "COLOR",
    "TYPE",
    "FONT",
    "CHARACTER",
    "POINTS",
    "TRANSPARENT",
}


class Parser(object):
    def __init__(
        self, expand_includes: bool = True, include_comments: bool = False, **kwargs
    ):
        self.expand_includes = expand_includes
        self.include_comments = include_comments
        self._comments: list[Any] = []
        self.lalr = self._create_lalr_parser()

    def _create_lalr_parser(self) -> Any:
        extra_args = {}

        if lark_cython:
            extra_args["_plugins"] = lark_cython.plugins

        if self.include_comments:
            callbacks = {
                "COMMENT": self._comments.append,
                "CCOMMENT": self._comments.append,
            }
            extra_args.update(dict(propagate_positions=True, lexer_callbacks=callbacks))

        return Lark.open("mapfile.lark", rel_to=__file__, parser="lalr", **extra_args)

    def _get_include_filename(self, line: str) -> str:
        if "#" in line:
            # remove any comments on the same line
            line = line.split("#")[0]

        include_pairs = line.split()
        if len(include_pairs) > 2:
            log.warning(
                "Multiple include files have been found on the same line. "
                "Only the first will be used. "
            )
        inc_file_path = include_pairs[1]

        return inc_file_path.strip("'").strip('"')

    def load_includes(
        self, text: str, fn: (str | None) = None, _nested_includes: int = 0
    ) -> str:
        # Per default use working directory of the process
        if fn is None:
            fn = os.getcwd() + os.sep

        lines = text.split("\n")
        includes = {}
        for idx, l in enumerate(lines):
            if l.strip().lower().startswith("include"):
                if _nested_includes == 5:
                    raise Exception("Maximum nested include exceeded! (MaxNested=5)")

                inc_file_path = self._get_include_filename(l)

                if not os.path.isabs(inc_file_path):
                    inc_file_path = os.path.abspath(
                        os.path.join(os.path.dirname(fn), inc_file_path)
                    )
                try:
                    include_text = self.open_file(inc_file_path)
                except IOError as ex:
                    log.warning(
                        "Include file '%s' not found in '%s'", inc_file_path, fn
                    )
                    raise ex
                # recursively load any further includes
                includes[idx] = self.load_includes(
                    include_text, fn=fn, _nested_includes=_nested_includes + 1
                )

        for idx, txt in includes.items():
            lines.pop(idx)  # remove the original include
            lines.insert(idx, txt)
        return "\n".join(lines)

    def assign_comments(self, tree: Any, comments: list[Any]) -> None:
        """
        Capture any comments in the tree

        header_comments stores comments preceding a node

        """
        comments = list(comments)
        comments.sort(key=lambda c: c.line)

        idx_by_line = {0: 0}  # {line_no: comment_idx}

        # enumerate through the comment tokens
        # and store their Mapfile line number as a key
        # with the index in the comment list as a value
        # e.g. in the example {0: 0, 2: 0, 3: 1, 6: 2}
        # line 3 in the Mapfile is associated with the comment at index 1
        # in the comment list
        for i, c in enumerate(comments):
            if c.line not in idx_by_line:
                idx_by_line[c.line] = i

        # convert comment tokens to strings, and remove any line breaks
        self.comments = [c.value.strip() for c in comments]

        # get the line of the last comment in the Mapfile
        last_comment_line = max(idx_by_line.keys())

        idx = []

        # make a list with an entry for each line
        # number associated with a comment list index
        # we go from the last comment line backwards
        for i in range(last_comment_line, 0, -1):
            if i in idx_by_line:
                # associate line with new comment
                idx.append(idx_by_line[i])
            else:
                # associate line with following comment
                idx.append(idx[-1])

        idx.append(0)  # line numbers start from 1
        # we processed the Mapfile backwards, but now reverse it for readability
        idx.reverse()

        # we now have a list representing lines in the Mapfile, with a value
        # storing the index to its associated comment
        # e.g. [0, 0, 0, 1, 2, 2, 2]
        # lines 1-3 are associated with the first comment in self.comments
        # lines 4 is associated with the second comment in self.comments
        # etc.

        self.idx = idx
        # now we can store the comments as properties on each of the nodes

        log.debug(self.idx)
        log.debug(self.comments)

        self._assign_comments(tree, 0)

    def _get_comments(self, from_line: int, to_line: int) -> list[Any]:
        """
        The self.comments property is a list of all comments found in the Mapfile
        ['# comment1', '# comment2', '# comment3']

        self.idx is in the form [0, 0, 0, 1, 2, 2, 2]

        """
        idx = self.idx
        comments = self.comments

        if from_line >= len(idx):
            return []  # no more comments

        from_idx = idx[from_line]

        if to_line < len(idx):
            to_idx = idx[to_line]
            if from_idx == to_idx:
                associated_comments = [comments[from_idx]]
            else:
                associated_comments = comments[from_idx:to_idx]
        else:
            # get all remaining comments in the Mapfile
            associated_comments = comments[from_idx:]

        return associated_comments

    def _assign_comments(self, _tree: Any, prev_end_line: int) -> None:
        """
        For each node in the tree assign any related comments
        """

        for node in _tree.children:
            if not isinstance(node, Tree):
                continue

            try:
                line = node.meta.line
            except AttributeError:
                assert not node.children
                continue

            if node.data not in ("composite", "attr", "string_pair", "string"):
                if isinstance(node, Tree):
                    prev_end_line = node.meta.end_line
                    self._assign_comments(node, prev_end_line)
                    continue  # move to next node

            # header_comments is a custom mappyfile property added to the meta object
            # it is used to store comments preceding the object
            log.debug(
                f"Finding header comments between lines {prev_end_line} and {line} for {node.data}"
            )
            header_comments = self._get_comments(prev_end_line, line)
            log.debug(f"{node.data} has associated header comments: {header_comments}")
            node.meta.header_comments = header_comments

            if node.meta.line == node.meta.end_line:
                # node is on a single line, so check for inline comments
                # and add them as a custom property to the Meta class of the node
                log.debug(
                    f"Finding inline comments between lines {prev_end_line} and {line} for {node.data}"
                )
                inline_comments = self._get_comments(line, line)
                log.debug(
                    f"{node.data} has associated inline comments: {inline_comments}"
                )
                node.meta.inline_comments = inline_comments  # type: ignore
                prev_end_line = node.meta.end_line + 1
            else:
                if isinstance(node, Tree):
                    self._assign_comments(node, line)
                prev_end_line = node.meta.end_line


    def load(self, fp: IO[str]) -> Any:
        text = fp.read()
        if hasattr(fp, "name"):
            fn = (
                fp.name
            )  # name is a read-only attribute and may not be present on all file-like objects.
        else:
            fn = None
        return self.parse(text, fn)

    def open_file(self, fn: str):
        try:
            with open(fn, "r", encoding="utf-8") as f:
                return f.read()
        except UnicodeDecodeError as ex:
            log.debug(ex)
            log.error(
                "Please check the encoding for %s. All Mapfiles should be in utf-8 format.",
                fn,
            )
            raise

    def parse_file(self, fn: str) -> Any:
        text = self.open_file(fn)
        return self.parse(text, fn=fn)

    def parse(self, text: str, fn: (str | None) = None) -> Any:
        """
        Parse the Mapfile
        """

        if self.expand_includes:
            text = self.load_includes(text, fn=fn)

        try:
            self._comments[:] = []  # clear any comments from a previous parse
            ip = self.lalr.parse_interactive(text)
            for t in ip.iter_parse():
                if t.type == "UNQUOTED_STRING":
                    # Unquoted strings after SYMBOL can only be values, not attributes
                    if (
                        ip.parser_state.value_stack[-1] == "SYMBOL"
                        and t.value.upper() not in SYMBOL_ATTRIBUTES
                    ):
                        t.type = "UNQUOTED_STRING_VALUE"
                elif t.type == "GRID":
                    # Unquoted 'GRID' coming after NAME is always a value, not a composite type
                    if ip.parser_state.value_stack[-1] == "NAME":
                        t.type = "UNQUOTED_STRING_VALUE"

            tree = ip.resume_parse()
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
