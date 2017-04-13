"""
Module to transform an AST (Abstract Syntax Tree) to a 
Python dict structure
"""

from collections import OrderedDict
from lark import Transformer, Tree
from mappyfile.tokens import ATTRIBUTE_NAMES, COMPOSITE_NAMES, SINGLETON_COMPOSITE_NAMES
from mappyfile.ordereddict import DefaultOrderedDict

def plural(s):

    if s == 'points':
        return s
    elif s.endswith('s'):
        return s +'es'
    else:
        return s +'s'

def dict_from_tail(t):
    """
    VALIDATION blocks can also have attributes such as qstring
    Values then have 3 parts - [('attr', u'qstring', u"'.'")]
    METADATA blocks have a simple 2 part form - [[u'"ows_enable_request"', u'"*"']]
    """
    d = OrderedDict()

    for v in t:
        if len(v) == 2:
            d[v[0]] = v[1]
        elif len(v) == 3:
            d[v[1]] = v[2]
        else:
            raise ValueError("Unsupported block '%s'", str(v))
    return d

class MapfileToDict(Transformer):

    def start(self, children):
        t,= children
        assert t[0] == 'composite'
        #assert t[1].lower() == 'map' # we can also parse partial map files
        return t[2]

    def composite(self, t):
        if len(t) == 3:
            # Parser artefact. See LINE-BREAK FLUIDITY in parsing_decisions.txt
            type_, attr, body = t
        else:
            type_, body = t
            attr = None

        if isinstance(body, tuple):
            assert body[0] == 'attr' or body[1] == 'points' or body[1] == 'pattern', body  # Parser artefacts
            body = [body]
        else:
            body = body.children

        #type_ = type_.tail[0].lower()
        type_ = type_.children[0].lower()

        assert type_ in COMPOSITE_NAMES.union(SINGLETON_COMPOSITE_NAMES)

        if attr:
            body = [attr] + body

        for x in body:
            assert isinstance(x, tuple), x

        composites = DefaultOrderedDict(list)
        d = DefaultOrderedDict(OrderedDict)

        for itemtype, k, v in body:          
            
            if itemtype == 'attr':

                # TODO tidy-up the code below
                if k == 'processing':
                    # PROCESSING can be repeated
                    if 'processing' not in d.keys():
                        d[k] = [v]
                    else:
                        d[k].append(v)
                elif k == 'config':
                    # CONFIG can be repeated, but with pairs of strings as a value
                    if 'config' not in d.keys():
                        d[k] = OrderedDict()
                    d[k][v[0]] = v[1]
                else:
                    d[k] = v

            elif itemtype == 'composite' and k in SINGLETON_COMPOSITE_NAMES:
                # there can only ever be one instance of these
                composites[k] = v # defaultdict using list
            elif itemtype == 'composite':
                composites[k].append(v)

            else:
                raise ValueError("Itemtype '%s' unknown", itemtype)
        
        for k, v in composites.items(): # collection of all items e.g. at the map level this is status, metadata etc. 

            if k not in SINGLETON_COMPOSITE_NAMES:
                d[plural(k)] = v
            else:
                d[k] = v

        d['__type__'] = type_
        return ('composite', type_, d)

    def attr(self, children):
        name = children[0].children[0]
        
        if isinstance(name, Tree):
            name = name.children[0] # Solve a parser artefact for composite names

        name = name.lower()
        assert name in ATTRIBUTE_NAMES, name

        value = children[1:]
        if len(value) == 1:
            value = value[0]
        return 'attr', name, value

    def projection(self, t):
        return ('composite', 'projection', t)

    def metadata(self, t):
        """
        Create a dict for the metadata items
        """
        d = dict_from_tail(t)
        return ('composite', 'metadata', d)

    def points(self, t):
        return ('composite', 'points', t)

    def pattern(self, t):
        # http://www.mapserver.org/mapfile/style.html
        return ('composite', 'pattern', t)

    def values(self, t):
        d = dict_from_tail(t)
        return ('composite', 'values', d)

    def validation(self, t):
        """
        Create a dict for the validation items
        """
        d = dict_from_tail(t)
        return ('composite', 'validation', d)

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
        return "(%s)" % t[0]
    def add(self, t):
        return "%s + %s" % tuple(t)

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



