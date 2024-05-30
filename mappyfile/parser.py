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


log = logging.getLogger("mappyfile")


def string_to_boolean(string_value: str):
    return string_value.lower() not in ("false", "no", "0", "off")


use_cython = string_to_boolean(os.environ.get("MAPPYFILE_USE_CYTHON", "True"))
lark_cython = None

if use_cython:
    try:
        import lark_cython  # type: ignore
    except ImportError:
        pass


SYMBOL_ATTRIBUTES = {
    "ANCHORPOINT",
    "ANTIALIAS",
    "FILLED",
    "FONT",
    "IMAGE",
    "NAME",
    "COLOR",
    "TYPE",
    "CHARACTER",
    "POINTS",
    "TRANSPARENT",
}


class Parser:
    def __init__(
        self, expand_includes: bool = True, include_comments: bool = False, **kwargs
    ):
        self.expand_includes = expand_includes
        self.include_comments = include_comments
        self._comments: list[Any] = []
        self.lalr = self._create_lalr_parser()
        self.kwargs = kwargs

    def _create_lalr_parser(self) -> Any:
        extra_args = {}

        if lark_cython:
            extra_args["_plugins"] = lark_cython.plugins

        if self.include_comments:
            callbacks = {
                "COMMENT": self._comments.append,
                "CCOMMENT": self._comments.append,
            }
            extra_args.update(
                {"propagate_positions": True, "lexer_callbacks": callbacks}
            )

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
        self, text: str, fn: str | None = None, _nested_includes: int = 0
    ) -> str:
        # Per default use working directory of the process
        if fn is None:
            fn = os.getcwd() + os.sep

        lines = text.split("\n")
        includes = {}
        for idx, l in enumerate(lines):
            if l.strip().lower().startswith("include"):
                if _nested_includes == 5:
                    raise ValueError("Maximum nested include exceeded! (MaxNested=5)")

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

    def _assign_comments(self, _tree: Any) -> None:
        for node in _tree.children:
            if not isinstance(node, Tree):
                continue

            if not hasattr(node.meta, "line"):
                continue

            line = node.meta.line

            # when we encounter a new type that can have associated comments
            # assign all comments up to that point in the Mapfile to the node
            # for metadata we want to assign comments to the string_pair
            if node.data in ("composite", "attr", "projection", "string_pair"):
                # for projection blocks capture any comments within the block

                if node.data in ("projection"):
                    line = node.meta.end_line
                line_numbers = list(sorted(self.comments_dict.keys()))
                comments = []

                for line_number in line_numbers:
                    if line_number <= line:
                        comments.append(self.comments_dict.pop(line_number))

                if comments:
                    node.meta.comments = comments  # type: ignore

            if isinstance(node, Tree):
                self._assign_comments(node)

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

    def parse(self, text: str, fn: str | None = None) -> Any:
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
                self.comments_dict = {}
                # create a dictionary using line numbers as keys, and comments as values
                for c in self._comments:
                    self.comments_dict[c.line] = c.value.strip()
                self._assign_comments(tree)

            return tree
        except (ParseError, UnexpectedInput) as ex:
            if fn:
                log.error("Parsing of %s unsuccessful", fn)
            else:
                log.error("Parsing of Mapfile unsuccessful")
            log.info(ex)
            raise
