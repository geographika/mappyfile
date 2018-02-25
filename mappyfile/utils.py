from __future__ import unicode_literals
import codecs
import warnings
import functools
from mappyfile.parser import Parser
from mappyfile.transformer import MapfileToDict
from mappyfile.pprint import PrettyPrinter


def deprecated(func):
    """
    From https://stackoverflow.com/questions/2536307/how-do-i-deprecate-python-functions/30253848#30253848
    This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.
    """
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning)  # turn off filter
        warnings.warn("Call to deprecated function {}.".format(func.__name__),
                      category=DeprecationWarning,
                      stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning)  # reset filter
        return func(*args, **kwargs)
    return new_func


def open(fn, expand_includes=True, include_position=False, include_comments=False):
    """
    Load a Mapfile from a filename
    """
    p = Parser(expand_includes=expand_includes,
               include_comments=include_comments)
    ast = p.parse_file(fn)
    m = MapfileToDict(include_position=include_position,
                      include_comments=include_comments)
    d = m.transform(ast)
    return d


def load(fp, expand_includes=True, include_position=False, include_comments=False):
    """
    Load a Mapfile from a file-like object
    """
    p = Parser(expand_includes=expand_includes,
               include_comments=include_comments)
    ast = p.load(fp)
    m = MapfileToDict(include_position=include_position,
                      include_comments=include_comments)
    d = m.transform(ast)
    return d


def loads(s, expand_includes=True, include_position=False, include_comments=False):
    """
    Load a Mapfile from a string
    """
    p = Parser(expand_includes=expand_includes,
               include_comments=include_comments)
    ast = p.parse(s)
    m = MapfileToDict(include_position=include_position,
                      include_comments=include_comments)
    d = m.transform(ast)
    return d


def dump(d, fp, indent=4, spacer=" ", quote='"', newlinechar="\n"):
    """
    Write d (the Mapfile dictionary) as a JSON formatted stream to fp
    """
    map_string = _pprint(d, indent, spacer, quote, newlinechar)
    fp.write(map_string)


@deprecated
def write(d, output_file, indent=4, spacer=" ", quote='"', newlinechar="\n"):
    """
    Write a Mapfile dictionary to a file. The save function should now be used. 
    """
    return save(d, output_file, indent, spacer, quote, newlinechar)


def save(d, output_file, indent=4, spacer=" ", quote='"', newlinechar="\n"):
    """
    Write a Mapfile dictionary to a file. 
    """
    map_string = _pprint(d, indent, spacer, quote, newlinechar)
    _save(output_file, map_string)
    return output_file


def dumps(d, indent=4, spacer=" ", quote='"', newlinechar="\n"):
    """
    Output a Mapfile dictionary as a string. 
    """
    return _pprint(d, indent, spacer, quote, newlinechar)


def find(lst, key, value):
    """
    Find an item in a list of dicts using a key and a value
    """
    return next((item for item in lst if item[key.lower()] == value), None)


def findall(lst, key, value):
    """
    Find all objects in lst where key matches value. 
    For example find all LAYERs in a MAP where GROUP equals VALUE
    """
    possible_values = ("'%s'" % value, '"%s"' % value)
    return (item for item in lst if item[key.lower()] in possible_values)


def _save(output_file, map_string):
    with codecs.open(output_file, "w", encoding="utf-8") as f:
        f.write(map_string)


def _pprint(d, indent, spacer, quote, newlinechar):
    pp = PrettyPrinter(indent=indent, spacer=spacer, 
                       quote=quote, newlinechar=newlinechar)
    return pp.pprint(d)
