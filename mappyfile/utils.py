# =================================================================
#
# Authors: Seth Girvin
#
# Copyright (c) 2021 Seth Girvin
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

from __future__ import unicode_literals
import sys
import codecs
import warnings
import functools
from collections import OrderedDict
from mappyfile.parser import Parser
from mappyfile.transformer import MapfileToDict
from mappyfile.pprint import PrettyPrinter
from mappyfile.validator import Validator

try:
    from itertools import izip_longest as zip_longest  # py2
except ImportError:
    from itertools import zip_longest  # py3


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


def open(fn, expand_includes=True, include_comments=False, include_position=False, **kwargs):
    """
    Load a Mapfile from the supplied filename into a Python dictionary.

    Parameters
    ----------

    fn: string
        The path to the Mapfile, or partial Mapfile
    expand_includes: boolean
        Load any ``INCLUDE`` files in the MapFile
    include_comments: boolean
         Include or discard comment strings from the Mapfile - *experimental*
    include_position: boolean
         Include the position of the Mapfile tokens in the output

    Returns
    -------

    dict
        A Python dictionary representing the Mapfile in the mappyfile format

    Example
    -------

    To open a Mapfile from a filename and return it as a dictionary object::

        d = mappyfile.open('mymap.map')

    Notes
    -----

    Partial Mapfiles can also be opened, for example a file containing a ``LAYER`` object.

    """
    p = Parser(expand_includes=expand_includes,
               include_comments=include_comments, **kwargs)
    ast = p.parse_file(fn)
    m = MapfileToDict(include_position=include_position,
                      include_comments=include_comments, **kwargs)
    d = m.transform(ast)
    return d


def load(fp, expand_includes=True, include_position=False, include_comments=False, **kwargs):
    """
    Load a Mapfile from an open file or file-like object.

    Parameters
    ----------

    fp: file
        A file-like object - as with all Mapfiles this should be encoded in "utf-8"
    expand_includes: boolean
        Load any ``INCLUDE`` files in the MapFile
    include_comments: boolean
         Include or discard comment strings from the Mapfile - *experimental*
    include_position: boolean
         Include the position of the Mapfile tokens in the output

    Returns
    -------

    dict
        A Python dictionary representing the Mapfile in the mappyfile format

    Example
    -------

    To open a Mapfile from a file and return it as a dictionary object::

        with open('mymap.map') as fp:
            d = mappyfile.load(fp)

    Notes
    -----

    Partial Mapfiles can also be opened, for example a file containing a ``LAYER`` object.
    """
    p = Parser(expand_includes=expand_includes,
               include_comments=include_comments, **kwargs)
    ast = p.load(fp)
    m = MapfileToDict(include_position=include_position,
                      include_comments=include_comments, **kwargs)
    d = m.transform(ast)
    return d


def loads(s, expand_includes=True, include_position=False, include_comments=False, **kwargs):
    """
    Load a Mapfile from a string

    Parameters
    ----------

    s: string
        The Mapfile, or partial Mapfile, text
    expand_includes: boolean
        Load any ``INCLUDE`` files in the MapFile
    include_comments: boolean
         Include or discard comment strings from the Mapfile - *experimental*
    include_position: boolean
         Include the position of the Mapfile tokens in the output

    Returns
    -------

    dict
        A Python dictionary representing the Mapfile in the mappyfile format

    Example
    -------

    To open a Mapfile from a string and return it as a dictionary object::

        s = '''MAP NAME "TEST" END'''

        d = mappyfile.loads(s)
        assert d["name"] == "TEST"

    """
    p = Parser(expand_includes=expand_includes,
               include_comments=include_comments, **kwargs)
    ast = p.parse(s)
    m = MapfileToDict(include_position=include_position,
                      include_comments=include_comments, **kwargs)
    d = m.transform(ast)
    return d


def dump(d, fp, indent=4, spacer=" ", quote='"', newlinechar="\n", end_comment=False,
         align_values=False, separate_complex_types=False):
    """
    Write d (the Mapfile dictionary) as a formatted stream to fp

    Parameters
    ----------

    d: dict
        A Python dictionary based on the the mappyfile schema
    fp: file
        A file-like object
    indent: int
        The number of ``spacer`` characters to indent structures in the Mapfile
    spacer: string
        The character to use for indenting structures in the Mapfile. Typically
        spaces or tab characters (``\\t``)
    quote: string
        The quote character to use in the Mapfile (double or single quotes)
    newlinechar: string
        The character used to insert newlines in the Mapfile
    end_comment: bool
        Add a comment with the block type at each closing END
        statement e.g. END # MAP
    align_values: bool
        Aligns the values in the same column for better readability. The column is
        multiple of indent and determined by the longest key
    separate_complex_types: bool
        Groups composites (complex mapserver definitions with "END") together at the end.
        Keeps the given order except that all simple key-value pairs appear before composites.

    Example
    -------

    To open a Mapfile from a string, and then dump it back out to an open file,
    using 2 spaces for indentation, and single-quotes for properties::

        s = '''MAP NAME "TEST" END'''

        d = mappyfile.loads(s)
        with open(fn, "w") as f:
            mappyfile.dump(d, f, indent=2, quote="'")

    """
    map_string = _pprint(d, indent, spacer, quote, newlinechar, end_comment, align_values, separate_complex_types)
    fp.write(map_string)


def save(d, output_file, indent=4, spacer=" ", quote='"', newlinechar="\n", end_comment=False,
         align_values=False, separate_complex_types=False, **kwargs):
    """
    Write a dictionary to an output Mapfile on disk

    Parameters
    ----------

    d: dict
        A Python dictionary based on the the mappyfile schema
    output_file: string
        The output filename
    indent: int
        The number of ``spacer`` characters to indent structures in the Mapfile
    spacer: string
        The character to use for indenting structures in the Mapfile. Typically
        spaces or tab characters (``\\t``)
    quote: string
        The quote character to use in the Mapfile (double or single quotes)
    newlinechar: string
        The character used to insert newlines in the Mapfile
    end_comment: bool
        Add a comment with the block type at each closing END
        statement e.g. END # MAP
    align_values: bool
        Aligns the values in the same column for better readability. The column is
        multiple of indent and determined by the longest key.
    separate_complex_types: bool
        Groups composites (complex mapserver definitions with "END") together at the end.
        Keeps the given order except that all simple key-value pairs appear before composites.

    Returns
    -------

    string
          The output_file passed into the function

    Example
    -------

    To open a Mapfile from a string, and then save it to a file::

        s = '''MAP NAME "TEST" END'''

        d = mappyfile.loads(s)
        fn = "C:/Data/mymap.map"
        mappyfile.save(d, fn)
    """
    map_string = _pprint(d, indent, spacer, quote, newlinechar, end_comment, align_values, separate_complex_types)
    _save(output_file, map_string)
    return output_file


def dumps(d, indent=4, spacer=" ", quote='"', newlinechar="\n", end_comment=False,
          align_values=False, separate_complex_types=False, **kwargs):
    """
    Output a Mapfile dictionary as a string

    Parameters
    ----------

    d: dict
        A Python dictionary based on the the mappyfile schema
    indent: int
        The number of ``spacer`` characters to indent structures in the Mapfile
    spacer: string
        The character to use for indenting structures in the Mapfile. Typically
        spaces or tab characters (``\\t``)
    quote: string
        The quote character to use in the Mapfile (double or single quotes)
    newlinechar: string
        The character used to insert newlines in the Mapfile
    end_comment: bool
        Add a comment with the block type at each closing END
        statement e.g. END # MAP
    align_values: bool
        Aligns the values in the same column for better readability. The column is
        multiple of indent and determined by the longest key
    separate_complex_types: bool
        Groups composites (complex mapserver definitions with "END") together at the end.
        Keeps the given order except that all simple key-value pairs appear before composites.

    Returns
    -------

    string
          The Mapfile as a string

    Example
    -------

    To open a Mapfile from a string, and then print it back out
    as a string using tabs::

        s = '''MAP NAME "TEST" END'''

        d = mappyfile.loads(s)
        print(mappyfile.dumps(d, indent=1, spacer="\\t"))
    """
    return _pprint(d, indent, spacer, quote, newlinechar, end_comment, align_values, separate_complex_types, **kwargs)


def find(lst, key, value):
    """
    Find an item in a list of dicts using a key and a value

    Parameters
    ----------

    list: list
        A list of composite dictionaries e.g. ``layers``, ``classes``
    key: string
        The key name to search each dictionary in the list
    key: value
        The value to search for

    Returns
    -------

    dict
        The first composite dictionary object with a key that matches the value

    Example
    -------

    To find the ``LAYER`` in a list of layers with ``NAME`` set to ``Layer2``::

        s = '''
        MAP
            LAYER
                NAME "Layer1"
                TYPE POLYGON
            END
            LAYER
                NAME "Layer2"
                TYPE POLYGON
                CLASS
                    NAME "Class1"
                    COLOR 0 0 -8
                END
            END
        END
        '''

        d = mappyfile.loads(s)
        cmp = mappyfile.find(d["layers"], "name", "Layer2")
        assert cmp["name"] == "Layer2"
    """
    return next((item for item in lst if item[key.lower()] == value), None)


def findall(lst, key, value):
    """
    Find all items in lst where key matches value.
    For example find all ``LAYER`` s in a ``MAP`` where ``GROUP`` equals ``VALUE``

    Parameters
    ----------

    list: list
        A list of composite dictionaries e.g. ``layers``, ``classes``
    key: string
        The key name to search each dictionary in the list
    key: value
        The value to search for

    Returns
    -------

    list
        A Python list containing the matching composite dictionaries

    Example
    -------

    To find all ``LAYER`` s with ``GROUP`` set to ``test``::

        s = '''
        MAP
            LAYER
                NAME "Layer1"
                TYPE POLYGON
                GROUP "test"
            END
            LAYER
                NAME "Layer2"
                TYPE POLYGON
                GROUP "test1"
            END
            LAYER
                NAME "Layer3"
                TYPE POLYGON
                GROUP "test2"
            END
            LAYER
                NAME "Layer4"
                TYPE POLYGON
                GROUP "test"
            END
        END
        '''

        d = mappyfile.loads(s)
        layers = mappyfile.findall(d["layers"], "group", "test")
        assert len(layers) == 2
    """
    return [item for item in lst if item[key.lower()] in value]


def findunique(lst, key):
    """
    Find all unique key values for items in lst.

    Parameters
    ----------

    lst: list
         A list of composite dictionaries e.g. ``layers``, ``classes``
    key: string
        The key name to search each dictionary in the list

    Returns
    -------

    list
        A sorted Python list of unique keys in the list

    Example
    -------

    To find all ``GROUP`` values for ``CLASS`` in a ``LAYER``::

        s = '''
        LAYER
            CLASS
                GROUP "group1"
                NAME "Class1"
                COLOR 0 0 0
            END
            CLASS
                GROUP "group2"
                NAME "Class2"
                COLOR 0 0 0
            END
            CLASS
                GROUP "group1"
                NAME "Class3"
                COLOR 0 0 0
            END
        END
        '''

        d = mappyfile.loads(s)
        groups = mappyfile.findunique(d["classes"], "group")
        assert groups == ["group1", "group2"]
    """
    return sorted(set([item[key.lower()] for item in lst]))


def findkey(d, *keys):
    """
    Get a value from a dictionary based on a list of keys and/or list indexes.

    Parameters
    ----------

    d: dict
        A Python dictionary
    keys: list
        A list of key names, or list indexes

    Returns
    -------

    dict
        The composite dictionary object at the path specified by the keys

    Example
    -------

    To return the value of the first class of the first layer in a Mapfile::

        s = '''
        MAP
            LAYER
                NAME "Layer1"
                TYPE POLYGON
                CLASS
                    NAME "Class1"
                    COLOR 0 0 255
                END
            END
        END
        '''

        d = mappyfile.loads(s)

        pth = ["layers", 0, "classes", 0]
        cls1 = mappyfile.findkey(d, *pth)
        assert cls1["name"] == "Class1"
    """
    if keys:
        keys = list(keys)
        key = keys.pop(0)
        return findkey(d[key], *keys)
    else:
        return d


def update(d1, d2):
    """
    Update dict d1 with properties from d2

    Note
    ----

    Allows deletion of objects with a special ``__delete__`` key
    For any list of dicts new items can be added when updating

    Parameters
    ----------

    d1: dict
        A Python dictionary
    d2: dict
        A Python dictionary that will be used to update any keys with the same name in d1

    Returns
    -------

    dict
        The updated dictionary

    """
    NoneType = type(None)

    if d2.get("__delete__", False):
        return {}

    for k, v in d2.items():
        if isinstance(v, dict):
            if v.get("__delete__", False):
                # allow a __delete__ property to be set to delete objects
                del d1[k]
            else:
                d1[k] = update(d1.get(k, {}), v)
        elif isinstance(v, (tuple, list)) and all(isinstance(li, (NoneType, dict)) for li in v):
            # a list of dicts and/or NoneType
            orig_list = d1.get(k, [])
            new_list = []
            pairs = list(zip_longest(orig_list, v, fillvalue=None))
            for orig_item, new_item in pairs:
                if orig_item is None:
                    orig_item = {}  # can't use {} for fillvalue as only one dict created/modified!
                if new_item is None:
                    new_item = {}

                if new_item.get("__delete__", False):
                    d = None  # orig_list.remove(orig_item) # remove the item to delete
                else:
                    d = update(orig_item, new_item)

                if d is not None:
                    new_list.append(d)
            d1[k] = new_list
        else:
            if k in d1 and v == "__delete__":
                del d1[k]
            else:
                d1[k] = v
    return d1


def validate(d, version=None):
    """
    Validate a mappyfile dictionary by using the Mapfile schema.
    An optional version number can be used to specify a specific
    a Mapfile is valid for a specific MapServer version.

    Parameters
    ----------

    d: dict
        A Python dictionary based on the the mappyfile schema
   version: float
        The MapServer version number used to validate the Mapfile

    Returns
    -------

    list
          A list containing validation errors

    """
    v = Validator()
    return v.validate(d, version=version)


def _save(output_file, string):
    with codecs.open(output_file, "w", encoding="utf-8") as f:
        f.write(string)


def _pprint(d, indent, spacer, quote, newlinechar, end_comment, align_values, separate_complex_types, **kwargs):
    pp = PrettyPrinter(indent=indent, spacer=spacer,
                       quote=quote, newlinechar=newlinechar,
                       end_comment=end_comment, align_values=align_values,
                       separate_complex_types=separate_complex_types, **kwargs)
    return pp.pprint(d)


def create(type, version=None):
    """
    Create a new mappyfile object, using MapServer defaults (if any).

    Parameters
    ----------

    s: type
        The mappyfile type to be stored in the __type__ property

    Returns
    -------

    dict
        A Python dictionary representing the Mapfile object in the mappyfile format
    """

    # get the schema for this type

    v = Validator()
    try:
        schema = v.get_versioned_schema(version=version, schema_name=type)
    except IOError:
        raise SyntaxError("The mappyfile type '{}' does not exist!".format(type))

    d = OrderedDict()
    d["__type__"] = type

    properties = sorted(schema["properties"].items())

    for k, v in properties:
        if "default" in v:
            d[k] = v["default"]

    return d


def dict_move_to_end(ordered_dict, key):

    if sys.version_info[0] < 3:
        # mappyfile requires Python >= 2.7,
        # so this should be safe
        val = ordered_dict[key]
        del ordered_dict[key]
        ordered_dict[key] = val
    else:
        ordered_dict.move_to_end(key)
