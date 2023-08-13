# =================================================================
#
# Authors: Seth Girvin
#
# Copyright (c) 2023 Seth Girvin
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
import logging
from typing import Any


log = logging.getLogger("mappyfile")


class Quoter:
    """
    A class to handle adding and standardising quotes around strings
    """

    def __init__(self, quote: str = '"'):
        assert quote in ("'", '"')

        self.quote = quote

        if self.quote == "'":
            self.altquote = '"'
        else:
            self.altquote = "'"

    def add_quotes(self, val: str) -> str:
        return self._add_quotes(val, self.quote)

    def add_altquotes(self, val: str) -> str:
        return self._add_quotes(val, self.altquote)

    def _add_quotes(self, val: str, quote: str) -> str:
        return f"{quote}{val}{quote}"

    def in_quotes(self, val: str) -> bool:
        return self._in_quotes(val, self.quote) or self._in_quotes(val, self.altquote)

    def _in_quotes(self, val: str, char: str):
        return val.startswith(char) and val.endswith(char)

    def escape_quotes(self, val: Any) -> Any:
        """
        Escape any quotes in a value
        """
        if self.is_string(val) and self._in_quotes(val, self.quote):
            # make sure any previously escaped quotes are not re-escaped
            middle = self.remove_quotes(val).replace("\\" + self.quote, self.quote)
            middle = middle.replace(self.quote, "\\" + self.quote)
            val = self.add_quotes(middle)

        return val

    def is_string(self, val: Any) -> bool:
        return isinstance(val, str)

    def remove_quotes(self, val: Any) -> Any:
        if isinstance(val, list):
            return list(map(self.remove_quotes, val))

        if not self.is_string(val):
            return val

        if self.in_quotes(val):
            return val[1:-1]

        return val

    def in_brackets(self, val: str) -> bool:
        val = val.strip()
        return val.startswith("[") and val.endswith("]")

    def in_parenthesis(self, val: str) -> bool:
        val = val.strip()
        return val.startswith("(") and val.endswith(")")

    def in_braces(self, val: str) -> bool:
        val = val.strip()
        return val.startswith("{") and val.endswith("}")

    def in_slashes(self, val: str) -> bool:
        val = val.strip()
        return self._in_quotes(val, "/")

    def standardise_quotes(self, val: str) -> str:
        """
        Change the quotes used to wrap a value to the pprint default
        E.g. "val" to 'val' or 'val' to "val"
        """
        if self._in_quotes(val, self.altquote):
            middle = self.remove_quotes(val)
            val = self.add_quotes(middle)

        return self.escape_quotes(val)
