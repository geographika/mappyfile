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

from __future__ import annotations
import codecs
import warnings
import functools
from mappyfile.ordereddict import DefaultOrderedDict
from mappyfile.parser import Parser
from mappyfile.transformer import MapfileToDict
from mappyfile.pprint import PrettyPrinter
from mappyfile.validator import Validator
from typing import IO


def deprecated(func):
    """
    From https://stackoverflow.com/questions/2536307/how-do-i-deprecate-python-functions/30253848#30253848
    This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.
    """

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter("always", DeprecationWarning)  # turn off filter
        warnings.warn(
            f"Call to deprecated function {func.__name__}.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        warnings.simplefilter("default", DeprecationWarning)  # reset filter
        return func(*args, **kwargs)

    return new_func


# pylint: disable=redefined-builtin
def open(
    fn: str,
    expand_includes: bool = True,
    include_comments: bool = False,
    include_position: bool = False,
    **kwargs,
) -> dict:
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
    p = Parser(
        expand_includes=expand_includes, include_comments=include_comments, **kwargs
    )
    ast = p.parse_file(fn)
    m = MapfileToDict(
        include_position=include_position, include_comments=include_comments, **kwargs
    )
    d = m.transform(ast)
    return d


def load(
    fp: IO[str],
    expand_includes: bool = True,
    include_position: bool = False,
    include_comments: bool = False,
    **kwargs,
) -> dict:
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
    p = Parser(
        expand_includes=expand_includes, include_comments=include_comments, **kwargs
    )
    ast = p.load(fp)
    m = MapfileToDict(
        include_position=include_position, include_comments=include_comments, **kwargs
    )
    d = m.transform(ast)
    return d


def loads(
    s: str,
    expand_includes: bool = True,
    include_position: bool = False,
    include_comments: bool = False,
    **kwargs,
) -> dict:
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
    p = Parser(
        expand_includes=expand_includes, include_comments=include_comments, **kwargs
    )
    ast = p.parse(s)
    m = MapfileToDict(
        include_position=include_position, include_comments=include_comments, **kwargs
    )
    d = m.transform(ast)
    return d


# pylint: disable=too-many-arguments
def dump(
    d: dict,
    fp: IO[str],
    indent: int = 4,
    spacer: str = " ",
    quote: str = '"',
    newlinechar: str = "\n",
    end_comment: bool = False,
    align_values: bool = False,
    separate_complex_types: bool = False,
):
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
    map_string = _pprint(
        d,
        indent,
        spacer,
        quote,
        newlinechar,
        end_comment,
        align_values,
        separate_complex_types,
    )
    fp.write(map_string)


# pylint: disable=too-many-arguments
def save(
    d: dict,
    output_file: str,
    indent: int = 4,
    spacer: str = " ",
    quote: str = '"',
    newlinechar: str = "\n",
    end_comment: bool = False,
    align_values: bool = False,
    separate_complex_types: bool = False,
) -> str:
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
    map_string = _pprint(
        d,
        indent,
        spacer,
        quote,
        newlinechar,
        end_comment,
        align_values,
        separate_complex_types,
    )
    _save(output_file, map_string)
    return output_file


# pylint: disable=too-many-arguments
def dumps(
    d: dict,
    indent: int = 4,
    spacer: str = " ",
    quote: str = '"',
    newlinechar: str = "\n",
    end_comment: bool = False,
    align_values: bool = False,
    separate_complex_types: bool = False,
    **kwargs,
) -> str:
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
    return _pprint(
        d,
        indent,
        spacer,
        quote,
        newlinechar,
        end_comment,
        align_values,
        separate_complex_types,
        **kwargs,
    )


def validate(d: dict, version: float | None = None) -> list:
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


def _save(output_file: str, string: str) -> None:
    with codecs.open(output_file, "w", encoding="utf-8") as f:
        f.write(string)


def _pprint(
    d: dict,
    indent: int,
    spacer: str,
    quote: str,
    newlinechar: str,
    end_comment: bool,
    align_values: bool,
    separate_complex_types: bool,
    **kwargs,
) -> str:
    pp = PrettyPrinter(
        indent=indent,
        spacer=spacer,
        quote=quote,
        newlinechar=newlinechar,
        end_comment=end_comment,
        align_values=align_values,
        separate_complex_types=separate_complex_types,
        **kwargs,
    )
    return pp.pprint(d)


def create(type: str, version=None) -> dict:
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
    except IOError as exc:
        raise SyntaxError("The mappyfile type '{type}' does not exist!") from exc

    d = DefaultOrderedDict()
    d["__type__"] = type

    properties = sorted(schema["properties"].items())

    for key, value in properties:
        if "default" in value:
            d[key] = value["default"]

    return d
