"""
Module to transform an AST (Abstract Syntax Tree) to a 
Python dict structure
"""

from collections import OrderedDict
from plyplus import STransformer, is_stree
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

    for v in t.tail:
        if len(v) == 2:
            d[v[0]] = v[1]
        elif len(v) == 3:
            d[v[1]] = v[2]
        else:
            raise ValueError("Unsupported block '%s'", str(v))
    return d

class MapfileToDict(STransformer):

    def start(self, t):
        t ,= t.tail
        assert t[0] == 'composite'
        #assert t[1].lower() == 'map' # we can also parse partial map files
        return t[2]

    def composite(self, t):
        if len(t.tail) == 3:
            # Parser artefact. See LINE-BREAK FLUIDITY in parsing_decisions.txt
            type_, attr, body = t.tail
        else:
            type_, body = t.tail
            attr = None

        if isinstance(body, tuple):
            assert body[0] == 'attr' or body[1] == 'points', body  # Parser artefacts
            body = [body]
        else:
            body = body.tail

        type_ = type_.tail[0].lower()
        assert type_ in COMPOSITE_NAMES.union(SINGLETON_COMPOSITE_NAMES)

        if attr:
            body = [attr] + body

        for x in body:
            assert isinstance(x, tuple), x

        composites = DefaultOrderedDict(list)
        #composites = defaultdict(list)

        d = DefaultOrderedDict(OrderedDict)
        #d = OrderedDict()

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

    def attr(self, t):
        name = t.tail[0].tail[0]
        if is_stree(name):
            name = name.tail[0] # Solve a parser artefact for composite names
        name = name.lower()
        assert name in ATTRIBUTE_NAMES, name
        value = t.tail[1:]

        if len(value) == 1:
            value ,= value
        return 'attr', name, value

    def projection(self, t):
        return ('composite', 'projection', t.tail)

    def metadata(self, t):
        """
        Create a dict for the metadata items
        """
        d = dict_from_tail(t)
        return ('composite', 'metadata', d)

    def points(self, t):
        return ('composite', 'points', t.tail)

    def pattern(self, t):
        # http://www.mapserver.org/mapfile/style.html
        return ('composite', 'pattern', t.tail)

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
        parts = [str(p) for p in list(t.tail)]
        x = " ".join(parts)
        return "( %s )" % x
    def and_test(self, t):
        #print t.tail
        x = " and ".join(t.tail)
        return "( %s )" % x
    def or_test(self, t):
        x = " or ".join(t.tail)
        return "( %s )" % x
    def compare_op(self, t):
        x ,= t.tail
        return x

    def regexp(self, t):
        """
        E.g. regexp(u'/^[0-9]*$/')
        """
        x ,= t.tail
        return x

    # for functions

    def func_call(self, t):
        func, params = t.tail
        func = func.tail[0] # this is an attr_name, not sure why it is not transformed already
        return "(%s(%s))" % (func, params)

    def func_params(self, t):
        params = ",".join(str(x) for x in t.tail)
        return params

    def attr_bind(self, t):
        x ,= t.tail
        return "[%s]" % x

    # basic types

    def int(self, t):
        x ,= t.tail
        return int(x)
    def float(self, t):
        x ,= t.tail
        return float(x)
    def bare_string(self, t):
        x ,= t.tail
        return x
    def string(self, t):
        x ,= t.tail
        return x
    def path(self, t):
        x ,= t.tail
        return x
    def string_pair(self, t):
        a, b = t.tail
        return [a, b]
    def int_pair(self, t):
        a, b = t.tail
        return [a, b]
    def list(self, t):
        # http://www.mapserver.org/mapfile/expressions.html#list-expressions
        return "{%s}" % ",".join([str(v) for v in t.tail])



