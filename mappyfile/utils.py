from mappyfile.parser import Parser
from mappyfile.transformer import MapfileToDict
from mappyfile.pprint import PrettyPrinter
import codecs

def load(fn, cwd=None):

    p = Parser(cwd=cwd)
    ast = p.parse_file(fn)
    m = MapfileToDict()
    d = m.transform(ast)

    return d    

def loads(s, cwd=None):
    p = Parser(cwd=cwd)
    ast = p.parse(s)
    m = MapfileToDict()
    d = m.transform(ast)

    return d   

def write(d, output_file, indent=4):

    map_string = _pprint(d, indent)
    _save(output_file, map_string)

    return output_file

def dumps(d):
    return _pprint(d)

def find(lst, key, value):
    """
    When looking for an item by value also check for the value 
    surrounded by apostrophes
    """
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

def _save(output_file, map_string):

    with codecs.open(output_file, "w", encoding="utf-8") as f:
        f.write(map_string)

def _pprint(d, indent=4):
    pp = PrettyPrinter(indent=indent)
    return pp.pprint(d)
