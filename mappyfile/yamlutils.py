# =================================================================
#
# Authors: Seth Girvin
#
# Copyright (c) 2026 Seth Girvin
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

import builtins
import collections
from typing import IO

try:
    import yaml
except ImportError:
    raise ImportError(
        "PyYAML is required for YAML support: pip install mappyfile[yaml]"
    )

from mappyfile.ordereddict import CaseInsensitiveOrderedDict, DefaultOrderedDict


def _represent_as_mapping(dumper, data):
    return dumper.represent_mapping("tag:yaml.org,2002:map", data.items())


def _represent_tuple(dumper, data):
    return dumper.represent_sequence("tag:yaml.org,2002:seq", data)


def _make_dumper():
    dumper = yaml.Dumper
    dumper.add_representer(CaseInsensitiveOrderedDict, _represent_as_mapping)
    dumper.add_representer(DefaultOrderedDict, _represent_as_mapping)
    dumper.add_representer(tuple, _represent_tuple)
    dumper.add_representer(collections.OrderedDict, _represent_as_mapping)
    return dumper


def open(fn: str) -> dict:
    """
    Load a Mapfile dictionary from a YAML file.

    Parameters
    ----------

    fn: string
        The path to the YAML file

    Returns
    -------

    dict
        A Python dictionary representing the Mapfile in the mappyfile format

    Example
    -------

    To open a YAML file and return it as a dictionary object::

        import mappyfile.yaml
        d = mappyfile.yaml.open('mymap.yaml')

    """
    with builtins.open(fn, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load(fp: IO[str]) -> dict:
    """
    Load a Mapfile dictionary from an open YAML file or file-like object.

    Parameters
    ----------

    fp: file
        A file-like object

    Returns
    -------

    dict
        A Python dictionary representing the Mapfile in the mappyfile format

    Example
    -------

    To load a YAML file using an open file object::

        import mappyfile.yaml
        with open('mymap.yaml', encoding='utf-8') as fp:
            d = mappyfile.yaml.load(fp)

    """
    return yaml.safe_load(fp)


def loads(s: str) -> dict:
    """
    Load a Mapfile dictionary from a YAML string.

    Parameters
    ----------

    s: string
        A YAML string representing a Mapfile

    Returns
    -------

    dict
        A Python dictionary representing the Mapfile in the mappyfile format

    Example
    -------

    To load a Mapfile dictionary from a YAML string::

        import mappyfile.yaml
        yaml_string = '''
        __type__: map
        name: MyMap
        '''
        d = mappyfile.yaml.loads(yaml_string)
        assert d["name"] == "MyMap"

    """
    return yaml.safe_load(s)


def dump(d: dict, fp: IO[str], **kwargs) -> None:
    """
    Write a Mapfile dictionary as a YAML formatted stream to fp.

    Parameters
    ----------

    d: dict
        A Python dictionary based on the mappyfile schema
    fp: file
        A file-like object
    kwargs:
        Additional keyword arguments passed to ``yaml.dump``, for example
        ``sort_keys=False`` to preserve key order

    Returns
    -------

    None

    Example
    -------

    To open a Mapfile and dump it as YAML to an open file::

        import mappyfile
        import mappyfile.yaml

        d = mappyfile.open('mymap.map')
        with open('mymap.yaml', 'w') as fp:
            mappyfile.yaml.dump(d, fp)

    """
    kwargs.setdefault("default_flow_style", False)
    kwargs.setdefault("allow_unicode", True)
    yaml.dump(d, fp, Dumper=_make_dumper(), **kwargs)


def save(d: dict, fn: str, **kwargs) -> str:
    """
    Write a Mapfile dictionary to a YAML file on disk.

    Parameters
    ----------

    d: dict
        A Python dictionary based on the mappyfile schema
    fn: string
        The output filename
    kwargs:
        Additional keyword arguments passed to ``yaml.dump``, for example
        ``sort_keys=False`` to preserve key order

    Returns
    -------

    string
          The output_file passed into the function

    Example
    -------

    To open a Mapfile and save it as a YAML file::

        import mappyfile
        import mappyfile.yaml

        d = mappyfile.open('mymap.map')
        mappyfile.yaml.save(d, 'mymap.yaml')

    """
    kwargs.setdefault("default_flow_style", False)
    kwargs.setdefault("allow_unicode", True)
    with builtins.open(fn, "w", encoding="utf-8") as f:
        yaml.dump(d, f, Dumper=_make_dumper(), **kwargs)
    return fn


def dumps(d: dict, **kwargs) -> str:
    """
    Output a Mapfile dictionary as a YAML string.

    Parameters
    ----------

    d: dict
        A Python dictionary based on the mappyfile schema
    kwargs:
        Additional keyword arguments passed to ``yaml.dump``, for example
        ``sort_keys=False`` to preserve key order

    Returns
    -------

    string
        The Mapfile as a YAML string

    Example
    -------

    To output a Mapfile dictionary as a YAML string::

        import mappyfile
        import mappyfile.yaml

        d = mappyfile.open('mymap.map')
        yaml_string = mappyfile.yaml.dumps(d)
        print(yaml_string)

    """
    kwargs.setdefault("default_flow_style", False)
    kwargs.setdefault("allow_unicode", True)
    return yaml.dump(d, Dumper=_make_dumper(), **kwargs)
