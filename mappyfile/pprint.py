# =================================================================
#
# Authors: Seth Girvin
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
import logging
import numbers
from mappyfile.tokens import (
    COMPOSITE_NAMES,
    SINGLETON_COMPOSITE_NAMES,
    REPEATED_KEYS,
    COMPLEX_TYPES,
    OBJECT_LIST_KEYS,
)
from mappyfile.validator import Validator
from mappyfile.quoter import Quoter
from mappyfile import dictutils
from typing import Any


log = logging.getLogger("mappyfile")


# pylint: disable=too-many-arguments
class PrettyPrinter:
    def __init__(
        self,
        indent: int = 4,
        spacer: str = " ",
        quote: str = '"',
        newlinechar: str = "\n",
        end_comment: bool = False,
        align_values: bool = False,
        separate_complex_types: bool = False,
    ):
        """
        Option use "\t" for spacer with an indent of 1
        """

        assert quote in ("'", '"')

        self.indent = indent
        self.spacer = spacer * self.indent
        self.quoter = Quoter(quote)
        self.newlinechar = newlinechar
        self.end_comment = end_comment
        self.end = "END"
        self.validator = Validator()
        self.align_values = align_values
        self.separate_complex_types = separate_complex_types

    def __is_metadata(self, key: str) -> bool:
        """
        Check to see if the property is hidden metadata
        e.g. "__type__", "__comments__", "__position__"
        """
        if key.startswith("__") and key.endswith("__"):
            return True

        return False

    def compute_aligned_max_indent(self, max_key_length: int) -> int:
        """
        Computes the indentation as a multiple of self.indent for aligning
        values at the same column based on the maximum key length.
        Example:
        key         value1
        longkey     value2
        longestkey  value3 <-- column at 12, indent of 4, determined by "longestkey"
        """
        indent = max(1, self.indent)
        return int((int(max_key_length / indent) + 1) * indent)

    def compute_max_key_length(self, composite: dict) -> int:
        """
        Computes the maximum length of all keys (non-recursive) in the passed
        composite.
        """
        length = 0

        ignore_list = (
            "metadata",
            "validation",
            "values",
            "connectionoptions",
            "pattern",
            "projection",
            "points",
            "config",
        )

        for attr, value in composite.items():
            attr_length = len(attr)
            if (
                not self.__is_metadata(attr)
                and attr not in ignore_list
                and not self.is_hidden_container(attr, value)
                and not self.is_composite(value)
            ):
                length = max(length, attr_length)

        return length

    def separate_complex(self, composite: dict, level: int) -> None:
        if not self.separate_complex_types:
            return
        for key in list(composite.keys()):
            if self.is_complex_type(composite, key, level):
                dictutils.dict_move_to_end(composite, key)

    def whitespace(self, level: int, indent: int) -> str:
        return self.spacer * (level + indent)

    def add_start_line(self, key: str, level: int) -> str:
        return self.whitespace(level, 1) + key.upper()

    def add_end_line(self, level: int, indent: int, key: str) -> str:
        end_line = self.whitespace(level, indent) + self.end
        if self.end_comment:
            end_line = f"{end_line} # {key.upper()}"
        return end_line

    def __format_line(
        self, spacer: str, key: str, value: Any, aligned_max_indent: int = 0
    ) -> str:
        if (aligned_max_indent is None) or (aligned_max_indent == 0):
            aligned_max_indent = len(key) + 1
        indent = " " * (aligned_max_indent - len(key))
        tmpl = "{spacer}{key}{indent}{value}"
        d = {"spacer": spacer, "key": key, "value": value, "indent": indent}
        return tmpl.format(**d)

    def process_key_dict(self, key: str, d: dict, level: int) -> list[str]:
        """
        Process key value dicts e.g. METADATA "key" "value"
        """

        # add any composite level comments
        comments = d.get("__comments__", {})
        lines: list[str] = []
        self._add_type_comment(level, comments, lines)

        lines += [self.add_start_line(key, level)]
        lines += self.process_dict(d, level, comments)
        lines.append(self.add_end_line(level, 1, key))

        return lines

    def process_dict(self, d: dict, level: int, comments: dict) -> list[str]:
        """
        Process keys and values within a block
        """
        lines = []

        aligned_max_indent = 0
        if self.align_values:
            max_key_length = self.compute_max_key_length(d) + 2  # add length of quotes
            aligned_max_indent = self.compute_aligned_max_indent(max_key_length)

        for k, v in d.items():
            if not self.__is_metadata(k):
                qk = self.quoter.add_quotes(k)
                qv = self.quoter.add_quotes(v)
                line = self.__format_line(
                    self.whitespace(level, 2), qk, qv, aligned_max_indent
                )
                line += self.process_attribute_comment(comments, k)
                lines.append(line)

        return lines

    def process_config_dict(self, d: dict, level: int) -> list[str]:
        """
        Process the CONFIG block
        """
        lines = []
        for k, v in d.items():
            cfg_val = self.quoter.add_quotes(k.upper())
            k = f"CONFIG {cfg_val}"
            v = self.quoter.add_quotes(v)
            lines.append(self.__format_line(self.whitespace(level, 1), k, v))
        return lines

    def process_repeated_list(
        self, key: str, lst: list[str], level: int, aligned_max_indent: int = 1
    ) -> list[str]:
        """
        Process blocks of repeated keys e.g. FORMATOPTION
        """
        lines = []

        for v in lst:
            k = key.upper()
            v = self.quoter.add_quotes(v)
            lines.append(
                self.__format_line(self.whitespace(level, 1), k, v, aligned_max_indent)
            )

        return lines

    def process_projection(
        self, key, lst: str | list[str], level: int, projection_comments: str
    ) -> list[str]:
        lines = [self.add_start_line(key, level)]

        whitespace = self.whitespace(level, 2)

        if projection_comments:
            lines.append(f"{whitespace}{projection_comments.strip()}")

        if self.quoter.is_string(lst):
            val = self.quoter.add_quotes(str(lst))
            # the value has been manually set to a single string projection
            lines.append(f"{whitespace}{val}")
        elif len(lst) == 1 and lst[0].upper() == "AUTO":
            lines.append(f"{whitespace}AUTO")
        else:
            for v in lst:
                v = self.quoter.add_quotes(v)
                lines.append(f"{whitespace}{v}")

        lines.append(self.add_end_line(level, 1, key))
        return lines

    def format_pair_list(self, key: str, pair_list: list[Any], level: int) -> list[str]:
        """
        Process lists of pairs (e.g. PATTERN block)
        """

        lines = [self.add_start_line(key, level)]

        list_spacer = self.spacer * (level + 2)
        pairs = [f"{list_spacer}{p[0]} {p[1]}" for p in pair_list]
        lines += pairs

        lines.append(self.add_end_line(level, 1, key))

        return lines

    def format_repeated_pair_list(
        self, key: str, root_list: list[Any], level: int
    ) -> list[str]:
        """
        Process (possibly) repeated lists of pairs e.g. POINTs blocks
        """

        lines = []

        def depth(iterable):
            return isinstance(iterable, (tuple, list)) and max(map(depth, iterable)) + 1

        if depth(root_list) == 2:
            # single set of points only
            root_list = [root_list]

        for pair_list in root_list:
            lines += self.format_pair_list(key, pair_list, level)

        return lines

    def is_composite(self, val: Any) -> bool:
        if isinstance(val, dict) and "__type__" in val:
            return True
        return False

    def is_complex_type(self, composite: dict, key: str, level: int) -> bool:
        # symbol needs special treatment
        if key == "symbol" and level > 0:
            return False
        return (
            key in COMPLEX_TYPES
            or self.is_composite(key)
            or self.is_hidden_container(key, composite[key])
        )

    def is_hidden_container(self, key: str, val: Any) -> bool:
        """
        The key is not one of the Mapfile keywords, and its
        values are a list
        """

        if key in OBJECT_LIST_KEYS and isinstance(val, list):
            return True
        return False

    def pprint(self, composites: dict | list[dict]) -> str:
        """
        Print out a nicely indented Mapfile
        """

        # if only a single composite is used then cast to list
        # and allow for multiple root composites

        if composites and not isinstance(composites, list):
            composites = [composites]

        lines = []

        for composite in composites:
            type_ = composite["__type__"]
            if type_ in ("metadata", "validation", "connectionoptions"):
                # types are being parsed directly, and not as an attr of a parent
                lines += self.process_key_dict(type_, composite, level=0)
            else:
                lines += self._format(composite)

        result = str(self.newlinechar.join(lines))
        return result

    def get_attribute_properties(self, type_: str, attr: str) -> dict:
        jsn_schema = self.validator.get_expanded_schema(type_)
        props = jsn_schema["properties"]

        # check if a value needs to be quoted or not, by referring to the JSON schema

        try:
            attr_props = props[attr]
        except KeyError as ex:
            log.error(
                "The key '%s' was not found in the JSON schema for '%s'", attr, type_
            )
            log.error(ex)
            return {}

        return attr_props

    def is_expression(self, option):
        return "description" in option and (option["description"] == "expression")

    def check_options_list(self, options_list, value):
        for option in options_list:
            if "enum" in option and value.lower() in option["enum"]:
                if value.lower() == "end":
                    # in GEOTRANSFORM "end" is an attribute value
                    return self.quoter.add_quotes(value)
                return value.upper()

            if self.is_expression(option):
                if value.endswith("'i") or value.endswith('"i'):
                    return value

        if self.quoter.in_slashes(value):
            return value

        return self.quoter.add_quotes(value)

    def format_value(self, attr: str, attr_props, value: Any) -> Any:
        """
        TODO - refactor and add more specific tests (particularly for expressions)
        """
        if isinstance(value, bool):
            return str(value).upper()

        if any(i in ["enum"] for i in attr_props):
            if isinstance(value, dict) and not value:
                raise ValueError(
                    f"The property {attr} has an empty dictionary as a value"
                )

            if not isinstance(value, numbers.Number):
                if attr == "compop":
                    return self.quoter.add_quotes(str(value))
                return str(value).upper()  # value is from a set list, no need for quote

            return value

        if (
            "type" in attr_props and attr_props["type"] == "string"
        ):  # and "enum" not in attr_props
            # check schemas for expressions and handle accordingly
            if self.is_expression(attr_props) and self.quoter.in_slashes(value):
                return value
            if self.is_expression(attr_props) and (
                value.endswith("'i") or value.endswith('"i')
            ):
                # for case insensitive regex
                return value

            return self.quoter.add_quotes(value)

        # expressions can be one of a string or an expression in brackets
        if any(
            i in ["oneOf", "anyOf"] for i in attr_props
        ):  # and check that type string is in list
            if "oneOf" in attr_props:
                options_list = attr_props["oneOf"]
            else:
                options_list = attr_props["anyOf"]
            if self.quoter.is_string(value):
                if self.quoter.in_parenthesis(value):
                    pass
                elif attr == "expression" and self.quoter.in_braces(value):
                    # don't add quotes to list expressions such as {val1, val2}
                    pass
                elif attr != "text" and self.quoter.in_brackets(value):
                    # TEXT expressions are often "[field1]-[field2]" so need to leave quotes for these
                    pass
                elif value.startswith("NOT ") and self.quoter.in_parenthesis(value[4:]):
                    value = f"NOT {value[4:]}"
                else:
                    value = self.check_options_list(options_list, value)

        if isinstance(value, list):
            new_values = []

            for v in value:
                if not isinstance(v, numbers.Number) and attr not in [
                    "offset",
                    "polaroffset",
                ]:
                    # don't add quotes to list of attributes for offset / polaroffset
                    v = self.quoter.add_quotes(v)
                new_values.append(v)

            value = " ".join(list(map(str, new_values)))
        else:
            value = self.quoter.escape_quotes(value)

        return value

    # pylint: disable=too-many-arguments
    def process_attribute(
        self, type_: str, attr: str, value: Any, level: int, aligned_max_indent: int = 1
    ) -> str:
        """
        Process one of the main composite types (see the type_ value)
        """

        attr_props = self.get_attribute_properties(type_, attr)
        value = self.format_value(attr, attr_props, value)
        line = self.__format_line(
            self.whitespace(level, 1), attr.upper(), value, aligned_max_indent
        )
        return line

    def format_comment(self, spacer: str, value: str) -> str:
        return f"{spacer}{value}"

    def process_composite_comment(self, level: int, comments: dict, key: str) -> str:
        """
        Process comments for composites such as MAP, LAYER etc.
        """
        if key not in comments:
            comment = ""
        else:
            value = comments[key]
            spacer = self.whitespace(level, 0)

            if isinstance(value, list):
                comment_list = [self.format_comment(spacer, v) for v in value]
                comment = self.newlinechar.join(comment_list)
            else:
                comment = self.format_comment(spacer, value)

        return comment

    def process_attribute_comment(self, comments: dict, key: str) -> str:
        if key not in comments:
            comment = ""
        else:
            value = comments[key]
            spacer = " "

            # for multiple comments associated with an attribute
            # simply join them together as a single string
            if isinstance(value, list):
                value = " ".join(value)

            comment = self.format_comment(spacer, value)

        return comment

    def _add_type_comment(self, level: int, comments: dict, lines: list[str]) -> None:
        comment = self.process_composite_comment(level, comments, "__type__")

        if comment:
            lines.append(str(comment))

    def _format(self, composite: dict, level: int = 0) -> list[str]:
        lines: list[str] = []
        type_ = ""

        # get any comments associated with the composite
        comments = composite.get("__comments__", {})

        if isinstance(composite, dict) and "__type__" in composite:
            type_ = composite["__type__"]
            assert type_ in COMPOSITE_NAMES.union(SINGLETON_COMPOSITE_NAMES)
            is_hidden = False
            self._add_type_comment(level, comments, lines)
            s = self.whitespace(level, 0) + type_.upper()
            lines.append(s)

        aligned_max_indent = 0
        if self.align_values:
            max_key_length = self.compute_max_key_length(composite)
            aligned_max_indent = self.compute_aligned_max_indent(max_key_length)

        self.separate_complex(composite, level)

        for attr, value in composite.items():
            if self.__is_metadata(attr):
                # skip hidden attributes
                continue

            if self.is_hidden_container(attr, value):
                # now recursively print all the items in the container
                for v in value:
                    lines += self._format(v, level + 1)
            elif attr == "pattern":
                lines += self.format_pair_list(attr, value, level)
            elif attr in ("metadata", "validation", "values", "connectionoptions"):
                # metadata and values are also composites
                # but will be processed here
                lines += self.process_key_dict(attr, value, level)

            elif attr == "projection":
                projection_comments = self.process_attribute_comment(comments, attr)
                lines += self.process_projection(
                    attr, value, level, projection_comments
                )
            elif attr in REPEATED_KEYS:
                lines += self.process_repeated_list(
                    attr, value, level, aligned_max_indent
                )
            elif attr == "points":
                lines += self.format_repeated_pair_list(attr, value, level)
            elif attr == "config":
                lines += self.process_config_dict(value, level)
            elif self.is_composite(value):
                lines += self._format(
                    value, level + 1
                )  # recursively add the child class
            else:
                # standard key value pair
                if not type_:
                    raise UnboundLocalError(
                        "The Mapfile object is missing a __type__ attribute"
                    )
                line = self.process_attribute(
                    type_, attr, value, level, aligned_max_indent
                )
                line += self.process_attribute_comment(comments, attr)
                lines.append(line)

        if not is_hidden:
            # close the container block with an END
            lines.append(self.add_end_line(level, 0, type_))

        return lines
