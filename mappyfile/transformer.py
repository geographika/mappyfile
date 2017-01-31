"""
Module to transform an AST (Abstract Syntax Tree) to a 
Python dict structure
"""
from collections import defaultdict

from plyplus import STransformer, is_stree

from tokens import ATTRIBUTE_NAMES, COMPOSITE_NAMES

def plural(s):
    if s == 'points':
        return s
    elif s.endswith('s'):
        return s+'es'
    return s+'s'

class MapFile2Dict__Transformer(STransformer):
    def start(self, t):
        t ,= t.tail
        assert t[0] == 'composite'
        assert t[1].lower() == 'map'
        return t[2]

    def composite(self, t):
        if len(t.tail) == 3:
            # Parser artifact. See LINE-BREAK FLUIDITY in parsing_decisions.txt
            type_, attr, body = t.tail
        else:
            type_, body = t.tail
            attr = None
        if isinstance(body, tuple):
            assert body[0] == 'attr' or body[1] == 'points', body  # Parser artifcats
            body = [body]
        else:
            body = body.tail
        type_ = type_.tail[0].lower()
        assert type_ in COMPOSITE_NAMES

        if attr:
            body = [attr] + body

        for x in body:
            assert isinstance(x, tuple), x

        composites = defaultdict(list)

        d = {}
        for itemtype, k, v in body:
            if itemtype == 'attr':
                d[k] = v
            elif itemtype == 'composite':
                composites[k].append(v)
            else:
                assert False, item

        for k, v in composites.items():
            d[plural(k)] = v

        d['__type__'] = type_
        return ('composite', type_, d)

    def attr(self, t):
        name = t.tail[0].tail[0]
        if is_stree(name):
            name = name.tail[0] # Solve a parser artifact for composite names
        name = name.lower()
        assert name in ATTRIBUTE_NAMES, name
        value = t.tail[1:]
        if len(value) == 1:
            value ,= value
        return 'attr', name, value

    def projection(self, t):
        return ('composite', 'projection', t.tail)
    def metadata(self, t):
        return ('composite', 'metadata', t.tail)
    def points(self, t):
        return ('composite', 'points', t.tail)
    def pattern(self, t):
        return ('composite', 'pattern', t.tail)
    def values(self, t):
        return ('attr', 'values', t.tail)
    def validation(self, t):
        return ('attr', 'validation', t.tail)

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



