from mappyfile.parser import Parser
from mappyfile.transformer import MapFile2Dict__Transformer
from mappyfile.pprint import PrettyPrinter

import codecs

def load(fn):
    p = Parser()
    ast = p.parse_file(fn)
    m = MapFile2Dict__Transformer()
    d = m.transform(ast)

    return d    

def loads(s):
    p = Parser()
    ast = p.parse(s)
    m = MapFile2Dict__Transformer()
    d = m.transform(ast)

    return d   

def dumps(d):
    pp = PrettyPrinter()
    return pp.pprint(d)

def find(lst, key, value):

    obj = __find__(lst, key, value)

    if not obj:
        v = "'%s'" % value
        obj = __find__(lst, key, v)

    if not obj:
        v = '"%s"' % value
        obj = __find__(lst, key, v)

    return obj

def __find__(lst, key, value):
    return next((item for item in lst if item[key.lower()] == value), None)

def save(map_string, output_file):

    with codecs.open(output_file, "w", encoding="utf-8") as f:
        f.write(map_string)

    return output_file