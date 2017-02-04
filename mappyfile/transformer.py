"""
Module to transform an AST (Abstract Syntax Tree) to a 
Python dict structure
"""

from collections import defaultdict # OrderedDict

from plyplus import STransformer, is_stree

from tokens import ATTRIBUTE_NAMES, COMPOSITE_NAMES, SINGLETON_COMPOSITE_NAMES

def plural(s):

    if s == 'points':
        return s
    elif s.endswith('s'):
        return s +'es'
    else:
        return s +'s'

def dict_from_tail(t):
    d = {} # OrderedDict()

    for v in t.tail:
        d[v[0]] = v[1]

    return d

class MapFile2Dict__Transformer(STransformer):
    def start(self, t):
        t ,= t.tail
        assert t[0] == 'composite'
        assert t[1].lower() == 'map'
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

        composites = defaultdict(list)

        d = {}

        for itemtype, k, v in body:          
            
            if itemtype == 'attr':

                if k == 'processing':
                    # PROCESSING can be repeated
                    if 'processing' not in d.keys():
                        d[k] = [v]
                    else:
                        d[k].append(v)
                else:
                    d[k] = v

            elif itemtype == 'composite' and k in SINGLETON_COMPOSITE_NAMES:
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
        return ('composite', 'pattern', t.tail[0])
    def values(self, t):
        d = dict_from_tail(t)
        return ('composite', 'values', d)

    def validation(self, t):
        return ('attr', 'validation', t.tail)

    # for expressions
    def comparison(self, t):
        parts = [str(p) for p in list(t.tail)]
        x = " ".join(parts)
        return "( %s )" % x
    def and_test(self, t):
        x = " and ".join(t.tail)
        return "( %s )" % x
    def or_test(self, t):
        x = " or ".join(t.tail)
        return "( %s )" % x
    def compare_op(self, t):
        x ,= t.tail
        return x

    # for functions

    def func_call(self, t):
        func, param = t.tail
        func = func.tail[0] # this is an attr_name, not sure why it is not transformed already
        return "(%s(%s))" % (func, param)
    def func_params(self, t):
        x ,= t.tail
        return x

    def attr_bind(self, t):
        x ,= t.tail
        return "[%s]" % x



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



