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


def open(fn, expand_includes=True, include_comments=False, include_position=False):
    """
    Load a Mapfile from the supplied filename into a Python dictionary

    :param string fn: The path to the Mapfile, or partial Mapfile
    :param boolean expand_includes: Load any ``INCLUDE`` files in the MapFile
    :param boolean include_comments: Include or discard comment strings from
                                     the Mapfile - *experimental*
    :param boolean include_position: Include the position of the Mapfile tokens in the output
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

    :param fp: A file-like object
    :param boolean expand_includes: Load any ``INCLUDE`` files in the MapFile
    :param boolean include_comments: Include or discard comment strings from
                                     the Mapfile - *experimental*
    :param boolean include_position: Include the position of the Mapfile tokens in the output
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

    :param string s: The Mapfile, or partial Mapfile, text
    :param boolean expand_includes: Load any ``INCLUDE`` files in the MapFile
    :param boolean include_comments: Include or discard comment strings from
                                     the Mapfile - *experimental*
    :param boolean include_position: Include the position of the Mapfile tokens in the output
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

    :param dictionary d: A Python dictionary based on the the mappyfile schema
    :param fp: A file-like object
    :param integer indent: The number of ``spacer`` characters to indent structures in
                           the Mapfile
    :param string spacer: The character to use for indenting structures in the Mapfile. Typically
                          spaces or tab characters (``\\t``)
    :param string quote: The quote character to use in the Mapfile (double or single quotes)
    :param string newlinechar: The character to to insert newlines in the Mapfile
    """
    map_string = _pprint(d, indent, spacer, quote, newlinechar)
    fp.write(map_string.encode('utf-8'))


@deprecated
def write(d, output_file, indent=4, spacer=" ", quote='"', newlinechar="\n"):
    """
    Write a Mapfile dictionary to a file. The save function should now be used.
    """
    return save(d, output_file, indent, spacer, quote, newlinechar)


def save(d, output_file, indent=4, spacer=" ", quote='"', newlinechar="\n"):
    """
    Write a Mapfile dictionary to a file.

    :param dictionary d: A Python dictionary based on the the mappyfile schema
    :param string output_file: The output filename
    :param integer indent: The number of ``spacer`` characters to indent structures in
                           the Mapfile
    :param string spacer: The character to use for indenting structures in the Mapfile. Typically
                          spaces or tab characters (``\\t``)
    :param string quote: The quote character to use in the Mapfile (double or single quotes)
    :param string newlinechar: The character to to insert newlines in the Mapfile
    """
    map_string = _pprint(d, indent, spacer, quote, newlinechar)
    _save(output_file, map_string)
    return output_file


def dumps(d, indent=4, spacer=" ", quote='"', newlinechar="\n"):
    """
    Output a Mapfile dictionary as a string

    :param dictionary d: A Python dictionary based on the the mappyfile schema
    :param integer indent: The number of ``spacer`` characters to indent structures in
                           the Mapfile
    :param string spacer: The character to use for indenting structures in the Mapfile. Typically
                          spaces or tab characters (``\\t``)
    :param string quote: The quote character to use in the Mapfile (double or single quotes)
    :param string newlinechar: The character to to insert newlines in the Mapfile
    """
    return _pprint(d, indent, spacer, quote, newlinechar)


def find(lst, key, value):
    """
    Find an item in a list of dicts using a key and a value

    :param list lst: A list of composite dictionaries e.g. ``layers``, ``classes``
    :param string key: The key name to search each dictionary in the list
    :param value: The value to search for
    """
    return next((item for item in lst if item[key.lower()] == value), None)


def findall(lst, key, value):
    """
    Find all items in lst where key matches value.
    For example find all ``LAYER``s in a ``MAP`` where ``GROUP`` equals ``VALUE``

    :param list lst: A list of composite dictionaries e.g. ``layers``, ``classes``
    :param string key: The key name to search each dictionary in the list
    :param value: The value to search for
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
