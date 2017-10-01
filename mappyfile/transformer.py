"""
Module to transform an AST (Abstract Syntax Tree) to a
Python dict structure
"""

import sys
from collections import OrderedDict
from lark import Transformer, Tree
from mappyfile.tokens import COMPOSITE_NAMES, SINGLETON_COMPOSITE_NAMES
from mappyfile.ordereddict import DefaultOrderedDict
from mappyfile.pprint import Quoter


PY2 = sys.version_info[0] < 3
if PY2:
    str = unicode # NOQA


class MapfileToDict(Transformer):

    def __init__(self):
        self.quoter = Quoter()

    def start(self, children):
        """
        Parses a MapServer Mapfile
        Parsing of partial Mapfiles or lists of composites is also possible
        """

        composites = []

        for child in children:
            assert(child[0] == 'composite')
            composites.append(child[2])

        # only return a list when there are multiple root composites (e.g.
        # several CLASSes)
        if len(composites) == 1:
            return composites[0]
        else:
            return composites

    def plural(self, s):

        if s == 'points':
            return s
        elif s.endswith('s'):
            return s + 'es'
        else:
            return s + 's'

    def repeated_key(self, d, k, v):
        """
        Allow the key to be added multiple times to its parent
        Examples are INCLUDE, PROCESSING
        """

        k = self.quoter.remove_quotes(k)
        v = self.quoter.remove_quotes(v)

        if k not in d.keys():
            d[k] = [v]
        else:
            d[k].append(v)

        return d

    def config_settings(self, d, k, v):
        """
        CONFIG settings can be repeated, but with pairs of strings as a
        value
        E.g CONFIG "MS_ERRORFILE" "filename"
        CONFIG "MS_NONSQUARE" "YES"
        """

        assert(k == 'config')
        subkey = self.quoter.remove_quotes(v[0].lower())
        d['config'][subkey] = self.quoter.remove_quotes(v[1])
        return d

    def dict_from_tail(self, vals):
        """
        VALIDATION blocks can also have attributes such as qstring
        Values then have 3 parts - [('attr', u'qstring', u"'.'")]
        METADATA blocks have a simple 2 part form -
        [[u'"ows_enable_request"', u'"*"']]

        As these values are case-sensitive use a standard OrderedDict
        """
        d = OrderedDict()

        for v in vals:
            v = map(self.quoter.remove_quotes, v)
            if len(v) == 2:
                k = v[0]
                d[k] = v[1]
            elif len(v) == 3:
                k = v[1]
                d[k] = v[2]
            else:
                raise ValueError("Unsupported block '%s'", str(v))
        return d

    def process_composite_body(self, body):
        """
        Process all the attributes and child objects of a COMPOSITE..END block
        """

        # create an ordered dict to contain lists of layers, classes etc.
        composites = DefaultOrderedDict(list)

        # create a dict to store standard attribute values
        attr_dict = DefaultOrderedDict(DefaultOrderedDict)

        # loop through all the attributes in the composite body
        for itemtype, k, v in body:

            if itemtype == 'attr':
                if k in ("processing", "formatoption", "include"):
                    self.repeated_key(attr_dict, k, v)
                elif k == 'config':
                    self.config_settings(attr_dict, k, v)
                else:
                    attr_dict[k] = self.quoter.remove_quotes(v)

            elif itemtype == 'composite' and k in SINGLETON_COMPOSITE_NAMES:
                # there can only ever be one child instance of these
                composites[k] = v  # defaultdict using list
            elif itemtype == 'composite':
                composites[k].append(v)
            else:
                raise ValueError("Item type '%s' unknown", itemtype)

        return composites, attr_dict

    def composite(self, t):
        """
        Handle the composite types e.g. CLASS..END
        [Tree(composite_type,
         [Token(__CLASS8, 'CLASS')]),
         Tree(composite_body, [('attr', u'name', "'test'")])]
        """
        if len(t) == 3:
            # unprocessed composite type
            type_, attr, body = t
        elif len(t) == 2:
            # process composite_type, composite_body
            type_, body = t
            attr = None
        else:
            # already processed by a separate function
            # e.g. metadata
            assert(len(t) == 1)
            type_, attr, body = t[0]
            types = ("metadata", "validation", "values")
            assert(attr in types)
            body['__type__'] = attr
            return ('composite', attr, body)

        if isinstance(body, tuple):
            # Parser artefacts
            assert body[0] == 'attr' or body[1] in ('points', 'pattern'), body
            body = [body]
        else:
            body = body.children

        type_ = type_.children[0].lower()

        assert type_ in COMPOSITE_NAMES.union(SINGLETON_COMPOSITE_NAMES)
        composites, attr_dict = self.process_composite_body(body)

        # collection of all items e.g. at the map level this is status,
        # metadata etc.
        for k, v in composites.items():

            if k in SINGLETON_COMPOSITE_NAMES:
                attr_dict[k] = v
            else:
                attr_dict[self.plural(k)] = v

        attr_dict['__type__'] = type_
        return ('composite', type_, attr_dict)

    def convert_value(self, value):

        if str(value).lower() == "true":
            return True
        if str(value).lower() == "false":
            return False

        try:
            value = int(value)
        except ValueError:
            value = str(value)

        return value

    def attr(self, children):

        key = children[0].children[0]

        if isinstance(key, Tree):
            # solve a parser artefact for composite names
            key = key.children[0]

        key = key.lower()  # make all keys lower-case

        # TODO one line Mapfiles can place several attributes on the same line
        values = children[1:]

        if len(values) == 1:
            value = self.convert_value(values[0])
        else:
            value = values  # "".join(map(str, values))

        return ('attr', key, value)

    def metadata(self, t):
        """
        Create a dict for the metadata items
        """
        d = self.dict_from_tail(t)
        return ('composite', 'metadata', d)

    def values(self, t):
        d = self.dict_from_tail(t)
        return ('composite', 'values', d)

    def validation(self, t):
        """
        Create a dict for the validation items
        """
        d = self.dict_from_tail(t)
        return ('composite', 'validation', d)

    def projection(self, t):
        v = map(self.quoter.remove_quotes, t)
        return ('composite', 'projection', v)

    def points(self, t):
        pairs = zip(t[::2], t[1::2])
        return ('composite', 'points', pairs)

    def pattern(self, t):
        pairs = zip(t[::2], t[1::2])
        return ('composite', 'pattern', pairs)

    # for expressions

    def comparison(self, t):
        parts = [str(p) for p in list(t)]
        v = " ".join(parts)
        return "( %s )" % v

    def and_test(self, t):
        v = " and ".join(t)
        return "( %s )" % v

    def or_test(self, t):
        v = " or ".join(t)
        return "( %s )" % v

    def compare_op(self, t):
        v = t[0]
        return v

    def not_expression(self, t):
        return "not %s" % t[0]

    def expression(self, t):
        v = t[0]
        if self.quoter.in_parenthesis(v):
            return v
        else:
            return "({})".format(v)

    def add(self, t):
        return "%s + %s" % tuple(t)

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
        func_name = func.children[0]
        v = "(%s(%s))" % (func_name, params)
        return v

    def func_params(self, t):
        params = ",".join(str(v) for v in t)
        return params

    def attr_bind(self, t):
        v = t[0]
        return "[%s]" % v

    # basic types

    def int(self, t):
        v = t[0]
        return int(v)

    def float(self, t):
        v = t[0]
        return float(v)

    def bare_string(self, t):
        if t:
            v = t[0]
        else:
            v = t
        return v

    def bare_string2(self, t):
        if t:
            v = t[0]
        else:
            v = t
        return v

    def string(self, t):
        v = t[0].value
        return v

    def path(self, t):
        v = t[0]
        return v

    def string_pair(self, t):
        a, b = t
        return [a, b]

    def int_pair(self, t):
        a, b = t
        return [a, b]

    def list(self, t):
        # http://www.mapserver.org/mapfile/expressions.html#list-expressions
        return "{%s}" % ",".join([str(v) for v in t])
