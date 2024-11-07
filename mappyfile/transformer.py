# =================================================================
#
# Authors: Erez Shinan, Seth Girvin
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

"""
Module to transform an AST (Abstract Syntax Tree) to a
Python dict structure
"""

from __future__ import annotations
import logging
from collections import OrderedDict
from lark import Tree
from lark.visitors import Transformer_InPlace, Transformer, v_args
from lark.lexer import Token
from .parser import lark_cython
from typing import Any
from mappyfile.tokens import SINGLETON_COMPOSITE_NAMES, REPEATED_KEYS
from mappyfile.ordereddict import CaseInsensitiveOrderedDict
from mappyfile.quoter import Quoter


if lark_cython:
    TOKEN_TYPES = (Token, lark_cython.Token)

    def update_token_value(t, value):
        return Token.new_borrow_pos(t.type, value, t)

else:
    TOKEN_TYPES = Token  # type: ignore

    def update_token_value(t, value):
        t.value = value
        return t


log = logging.getLogger("mappyfile")


class MapfileTransformer(Transformer):
    def __init__(self, include_position: bool = False, include_comments: bool = False):
        self.quoter = Quoter()
        self.include_position = include_position
        self.include_comments = include_comments

    def key_name(self, token) -> str:
        return token.value.lower()

    def start(self, composites):
        """
        Parses a MapServer Mapfile
        Parsing of partial Mapfiles or lists of composites is also possible
        """

        # only return a list when there are multiple root composites (e.g.
        # several CLASSes)
        if len(composites) == 1:
            return composites[0]

        return composites

    def flatten(self, values: list[Any]) -> list[Any]:
        flat_list = []

        for v in values:
            if isinstance(v, TOKEN_TYPES):
                flat_list.append(v)
            elif isinstance(v, list):
                flat_list += v
            elif isinstance(v, tuple):
                flat_list += v
            elif isinstance(v, dict):
                assert "__tokens__" in v
                flat_list += v["__tokens__"]
            else:
                raise ValueError("Attribute value type not supported", v)

        return flat_list

    def plural(self, s: str) -> str:
        if s.endswith("s"):
            return s + "es"

        return s + "s"

    def create_position_dict(self, key_token, values) -> dict:
        line, column = key_token.line, key_token.column
        d = OrderedDict()
        d["line"] = line
        d["column"] = column

        if values:
            flat_list = self.flatten(values)
            value_positions = [(v.line, v.column) for v in flat_list]
            d["values"] = value_positions

        return d

    def get_single_key(self, d: dict):
        keys = list(d.keys())  # convert to list for py3
        assert len(keys) == 1
        return keys[0]

    def composite_body(self, t):
        return t

    def composite_type(self, t):
        return t

    def _process_composite_config(
        self,
        composite_dict: dict,
        attribute_dict: dict,
        position_dict: dict | None,
        pos: int,
    ):
        key_name = "config"

        # there may be several config dicts - one for each setting
        if key_name not in composite_dict:
            # create an initial OrderedDict
            composite_dict[key_name] = CaseInsensitiveOrderedDict(
                CaseInsensitiveOrderedDict
            )
        # populate the existing config dict
        cfg_dict = composite_dict[key_name]
        cfg_dict.update(attribute_dict[key_name])

        if position_dict is not None:
            if key_name not in position_dict:
                position_dict[key_name] = OrderedDict()

            subkey_name = self.get_single_key(attribute_dict[key_name])
            position_dict[key_name][subkey_name] = pos

    def _process_composite_points(
        self,
        composite_dict: dict,
        attribute_dict: dict,
        position_dict: dict | None,
        pos: int,
    ):
        key_name = "points"

        if key_name not in composite_dict:
            composite_dict[key_name] = attribute_dict[key_name]
        else:
            # if points are already in a feature then
            # allow for multipart features in a nested list
            existing_points = composite_dict[key_name]

            if calculate_depth(existing_points) == 2:
                composite_dict[key_name] = [existing_points]

            if key_name not in composite_dict:
                composite_dict[key_name] = []
            composite_dict[key_name].append(attribute_dict[key_name])

        if position_dict is not None:
            if key_name not in position_dict:
                position_dict[key_name] = pos
            else:
                existing_pos = position_dict[key_name]
                if isinstance(existing_pos, dict):
                    position_dict[key_name] = [existing_pos]
                position_dict[key_name].append(pos)

    def composite(self, t):
        """
        Handle the composite types e.g. CLASS..END
        t is a list in the form [[Token(__LAYER36, 'LAYER')], [OrderedDict([...])]]

        """
        if len(t) == 1:
            return t[0]  # metadata and values - already processed

        key_token = t[0][0]
        attribute_dicts = t[1]

        if not isinstance(attribute_dicts, list):
            # always handle a list of attributes
            attribute_dicts = [attribute_dicts]

        key_name = self.key_name(key_token)
        composite_dict = CaseInsensitiveOrderedDict(CaseInsensitiveOrderedDict)
        composite_dict["__type__"] = key_name

        if self.include_position:
            position_dict = self.create_position_dict(key_token, None)
            composite_dict["__position__"] = position_dict
        else:
            position_dict = None

        if self.include_comments:
            comments_dict = composite_dict["__comments__"] = OrderedDict()

        for d in attribute_dicts:
            keys = d.keys()
            if "__type__" in keys:
                k = d["__type__"]
                if k in SINGLETON_COMPOSITE_NAMES:
                    composite_dict[k] = d
                else:
                    plural_key = self.plural(k)
                    if plural_key not in composite_dict:
                        composite_dict[plural_key] = []

                    composite_dict[plural_key].append(d)
            else:
                #  simple attribute
                pos = d.pop("__position__")
                d.pop(
                    "__tokens__", None
                )  # tokens are no longer needed now we have the positions
                comments = d.pop("__comments__", None)

                key_name = self.get_single_key(d)

                if key_name == "config":
                    self._process_composite_config(
                        composite_dict, d, position_dict, pos
                    )
                elif key_name == "points":
                    self._process_composite_points(
                        composite_dict, d, position_dict, pos
                    )
                elif key_name in REPEATED_KEYS:
                    if key_name not in composite_dict:
                        composite_dict[key_name] = []

                    composite_dict[key_name].append(d[key_name])

                    if position_dict:
                        if key_name not in position_dict:
                            position_dict[key_name] = []
                        position_dict[key_name].append(pos)
                else:
                    assert len(d.items()) == 1
                    if position_dict:
                        # hoist position details to composite
                        position_dict[key_name] = pos
                    if self.include_comments and comments:
                        # hoist comments to composite
                        comments_dict[key_name] = comments

                    composite_dict[key_name] = d[key_name]

        return composite_dict

    def clean_string(self, val: str) -> str:
        return self.quoter.remove_quotes(val)

    def attr_name(self, tokens) -> str:
        t = tokens[0]
        if not isinstance(t, TOKEN_TYPES):
            #  handle ambiguities
            t = t[0]
            assert t.value.lower() in ("symbol", "style")

        return t

    def attr(self, tokens) -> dict:
        key_token = tokens[0]

        if isinstance(key_token, (list, tuple)):
            key_token = key_token[0]
            assert self.key_name(key_token) in ("style", "symbol"), self.key_name(
                key_token
            )

        key_name = self.key_name(key_token)
        value_tokens = tokens[1:]

        if isinstance(value_tokens[0], (list, tuple)):
            # for any multi-part attributes they will be lists or tuples
            # e.g. int_pair, rgb etc.
            assert len(value_tokens) == 1
            value_tokens = value_tokens[0]

        pd = self.create_position_dict(key_token, value_tokens)
        d: dict = OrderedDict()
        d["__position__"] = pd

        if len(value_tokens) > 1:
            if key_name == "config":
                assert len(value_tokens) == 2
                values = {value_tokens[0].value: value_tokens[1].value}
            else:
                # list of values
                values = [v.value for v in value_tokens]  # type: ignore
                d["__tokens__"] = [key_token] + list(value_tokens)
        else:
            # single value
            value_token = value_tokens[0]
            # store the original tokens so they can be processed
            # differently for METADATA, VALIDATION, and VALUES
            d["__tokens__"] = [key_token, value_token]
            values = value_token.value

            if self.quoter.is_string(values):
                values = self.clean_string(values)  # type: ignore

        d[key_name] = values

        return d

    def check_composite_tokens(self, name: str, tokens) -> tuple[str, list[Any]]:
        """
        Return the key and contents of a KEY..END block
        for PATTERN, POINTS, and PROJECTION
        """
        assert len(tokens) >= 2
        key = tokens[0]

        assert key.value.lower() == name
        assert tokens[-1].value.lower() == "end"

        if len(tokens) == 2:
            body = []  # empty TYPE..END block
        else:
            body = tokens[1:-1]

        body_tokens = []

        for t in body:
            if isinstance(t, dict):
                body_tokens.append(t["__tokens__"])
            else:
                body_tokens.append(t)
        return key, body_tokens

    def process_value_pairs(self, tokens, type_) -> dict:
        """
        Metadata, Values, and Validation blocks can either
        have string pairs or attributes
        Attributes will already be processed
        """
        key, body = self.check_composite_tokens(type_, tokens)
        key_name = self.key_name(key)

        d = CaseInsensitiveOrderedDict(CaseInsensitiveOrderedDict)

        for t in body:
            k = self.clean_string(t[0].value).lower()
            v = self.clean_string(t[1].value)

            if k in d.keys():
                log.warning(
                    "A duplicate key (%s) was found in %s. Only the last value (%s) will be used. ",
                    k,
                    type_,
                    v,
                )

            d[k] = v

        if self.include_position:
            pd = self.create_position_dict(key, body)
            d["__position__"] = pd

        d["__type__"] = key_name

        # return the token as well as the processed dict so the
        # composites function works the same way
        return d

    def connectionoptions(self, tokens):
        """
        Create a dict for the connectionoptions items
        """

        return self.process_value_pairs(tokens, "connectionoptions")

    def metadata(self, tokens):
        """
        Create a dict for the metadata items
        """

        return self.process_value_pairs(tokens, "metadata")

    def values(self, tokens):
        """
        Create a dict for the values items
        """

        return self.process_value_pairs(tokens, "values")

    def config(self, t):
        # process this as a separate rule
        assert len(t) == 3
        key = t[1].value.lower()  # store all subkeys in lowercase
        value = t[2].value
        t[1].value = self.clean_string(key)
        t[2].value = self.clean_string(value)
        return self.attr(t)

    def validation(self, tokens):
        """
        Create a dict for the validation items
        """
        return self.process_value_pairs(tokens, "validation")

    def projection(self, tokens):
        _, body = self.check_composite_tokens("projection", tokens)
        projection_strings = [self.clean_string(v.value) for v in body]

        key_token = tokens[0]
        value_token = tokens[1]  # take the first string as the default token
        value_token = update_token_value(value_token, projection_strings)
        tokens = (key_token, value_token)

        return self.attr(tokens)

    def process_pair_lists(self, key_name, tokens):
        _, body = self.check_composite_tokens(key_name, tokens)
        pairs = [(v[0].value, v[1].value) for v in body]

        key_token = tokens[0]
        value_token = tokens[1][0]  # take the first numeric value pair as the token
        value_token.value = pairs  # set its value to all values
        tokens = (key_token, value_token)

        return self.attr(tokens)

    def points(self, tokens):
        return self.process_pair_lists("points", tokens)

    def pattern(self, tokens):
        return self.process_pair_lists("pattern", tokens)

    # for expressions

    def comparison(self, t):
        assert len(t) == 3
        parts = [str(p.value) for p in t]
        v = " ".join(parts)

        v = f"( {v} )"
        t[0].value = v
        return t[0]

    def and_test(self, t):
        assert len(t) == 2
        t[0].value = f"( {t[0].value} AND {t[1].value} )"
        return t[0]

    def or_test(self, t):
        assert len(t) == 2
        t[0].value = f"( {t[0].value} OR {t[1].value} )"
        return t[0]

    def compare_op(self, t):
        v = t[0]
        return v

    def not_expression(self, t):
        v = t[0]
        v.value = f"NOT {v.value}"
        return v

    def expression(self, t):
        exp = " ".join(
            [str(v.value) for v in t]
        )  # convert to string for boolean expressions e.g. (true)

        if not self.quoter.in_parenthesis(exp):
            t[0].value = f"({exp})"

        return t[0]

    def add(self, t):
        assert len(t) == 2
        t[0].value = f"{t[0].value} + {t[1].value}"
        return t[0]

    def sub(self, t):
        assert len(t) == 2
        t[0].value = f"{t[0].value} - {t[1].value}"
        return t[0]

    def div(self, t):
        assert len(t) == 2
        t[0].value = f"{t[0].value} / {t[1].value}"
        return t[0]

    def mul(self, t):
        assert len(t) == 2
        t[0].value = f"{t[0].value} * {t[1].value}"
        return t[0]

    def power(self, t):
        assert len(t) == 2
        t[0].value = f"{t[0].value} ^ {t[1].value}"
        return t[0]

    def neg(self, t):
        assert len(t) == 1
        t[0].value = f"-{t[0].value}"
        return t[0]

    def runtime_var(self, t):
        v = t[0]
        return v

    def regexp(self, t):
        """
        E.g. regexp(u'/^[0-9]*$/')
        """
        v = t[0]
        return v

    # for functions

    def func_call(self, t):
        """
        For function calls e.g. TEXT (tostring([area],"%.2f"))
        """
        func, params = t
        func_name = func.value
        func.value = f"({func_name}({params}))"
        return func

    def func_params(self, t):
        params = ",".join(str(v.value) for v in t)
        return params

    def attr_bind(self, t):
        assert len(t) == 1
        t = t[0]
        t.value = f"[{t.value}]"
        return t

    def extent(self, t):
        assert len(t) == 4
        return t

    def color(self, t):
        pass

    def value(self, t):
        return t

    # basic types

    def true(self, t):
        v = t[0]
        return update_token_value(v, True)

    def false(self, t):
        v = t[0]
        return update_token_value(v, False)

    def int(self, t):
        v = t[0]
        return update_token_value(v, int(v.value))

    def float(self, t):
        v = t[0]
        return update_token_value(v, float(v.value))

    def bare_string(self, t):
        return t[0]

    def name(self, t):
        v = t[0]
        return v

    def string(self, t):
        v = t[0]
        return v

    def path(self, t):
        return t[0]

    def string_pair(self, t):
        a, b = t
        return [a, b]

    def rgb(self, t):
        r, g, b = t
        return r, g, b

    def attr_bind_pair(self, t):
        assert len(t) == 2
        return t

    def attr_mixed_pair(self, t):
        assert len(t) == 2
        return t

    def colorrange(self, t):
        assert len(t) == 6
        return t

    def hexcolorrange(self, t):
        assert len(t) == 2
        return t

    def hexcolor(self, t):
        t[0].value = self.clean_string(t[0].value).lower()
        return t[0]

    def num_pair(self, t):
        a, b = t
        return a, b

    def int_pair(self, t):
        a, b = t
        return a, b

    def list(self, t):
        # http://www.mapserver.org/mapfile/expressions.html#list-expressions
        v = t[0]
        list_values = ",".join([str(s) for s in t])
        v.value = "{%s}" % list_values
        return v


class CommentsTransformer(Transformer_InPlace):
    """
    This is an additional transformer that is used to go through
    all the nodes and take any of the custom node.meta.comment properties
    and add these value to the node's corresponding dictionary
    """

    def __init__(self, mapfile_todict):
        self._mapfile_todict = mapfile_todict

    def get_comments(self, meta):
        all_comments = []

        if hasattr(meta, "comments"):
            all_comments += meta.comments

        return all_comments

    def add_metadata_comments(self, d, metadata):
        """
        Any duplicate keys will be replaced with the last duplicate along with comments
        """

        if len(metadata) > 2:
            string_pairs = metadata[1:-1]  # get all metadata pairs
            for sp in string_pairs:
                # get the raw metadata key

                if isinstance(sp.children[0], TOKEN_TYPES):
                    token = sp.children[0]
                    assert token.type == "UNQUOTED_STRING"
                    key = token.value
                else:
                    # quoted string (double or single)
                    token = sp.children[0].children[0]
                    key = token.value

                # clean it to match the dict key
                key = self._mapfile_todict.clean_string(key).lower()
                assert key in d.keys()
                key_comments = self.get_comments(sp.meta)
                d["__comments__"][key] = key_comments

        return d

    @v_args(tree=True)
    def _save_attr_comments(self, tree):
        d = self._mapfile_todict.transform(tree)
        d["__comments__"] = self.get_comments(tree.meta)
        return d

    @v_args(tree=True)
    def _save_composite_comments(self, tree):
        d = self._mapfile_todict.transform(tree)

        # composites such as METADATA will not have had a comments
        # dict created yet
        if "__comments__" not in d:
            d["__comments__"] = OrderedDict()

        comments = self.get_comments(tree.meta)
        if comments:
            d["__comments__"]["__type__"] = comments

        if d["__type__"] == "metadata":
            md = tree.children[0].children
            self.add_metadata_comments(d, md)

        return d

    @v_args(tree=True)
    def _save_projection_comments(self, tree):
        d = self._mapfile_todict.transform(tree)
        comments = self.get_comments(tree.meta)
        if comments:
            d["__comments__"] = comments

        return d

    # below we assign callbacks to process comments for each of the following types
    attr = _save_attr_comments
    projection = _save_projection_comments
    composite = _save_composite_comments


class MapfileToDict:
    def __init__(
        self,
        include_position=False,
        include_comments=False,
        transformer_class=MapfileTransformer,
        **kwargs,
    ):
        self.include_position = include_position
        self.include_comments = include_comments
        self.transformer_class = transformer_class
        self.kwargs = kwargs

    def transform(self, tree):
        tree = Canonize().transform(tree)

        self.mapfile_transformer = self.transformer_class(
            include_position=self.include_position,
            include_comments=self.include_comments,
            **self.kwargs,
        )

        if self.include_comments:
            comments_transformer = CommentsTransformer(self.mapfile_transformer)
            tree = comments_transformer.transform(tree)

        return self.mapfile_transformer.transform(tree)


class Canonize(Transformer_InPlace):
    @v_args(tree=True)
    def symbolset(self, tree):
        composite_type = Tree("composite_type", [Token("symbolset", "symbolset")])

        tree.data = "composite"
        tree.children.insert(0, composite_type)
        return tree


def calculate_depth(iterable):
    """
    A helper function to get the max length + 1 in a list of lists
    """
    return (
        isinstance(iterable, (tuple, list)) and max(map(calculate_depth, iterable)) + 1
    )
