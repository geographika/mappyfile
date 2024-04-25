# =================================================================
#
# Authors: Seth Girvin
#
# Copyright (c) 2023 Seth Girvin
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
from typing import Any
from itertools import zip_longest


def find(lst: list[dict], key: str, value: Any) -> dict | None:
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


def findall(lst: list[dict], key: str, value: Any) -> list[dict]:
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
    return [item for item in lst if item[key.lower()] and item[key.lower()] in value]


def findunique(lst, key):
    """
    Find all unique key values for items in lst. If no
    items with the key are found an empty list is returned.

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
    return sorted(
        set((item.get(key.lower(), None) for item in lst))
        - {
            None,
        }
    )


def findkey(d: dict, *keys: list[Any]) -> dict:
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
        keys_list = list(keys)
        search_key = keys_list.pop(0)
        return findkey(d[search_key], *keys_list)

    return d


def update(d1: dict, d2: dict, overwrite: bool = True) -> dict:
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
    overwrite: boolean
        If a key already exists in the dictionary should its value be overwritten

    Returns
    -------

    dict
        The updated dictionary

    """
    none_type = type(None)

    if d2.get("__delete__", False):
        return {}

    for k, v in d2.items():
        if isinstance(v, dict):
            if v.get("__delete__", False):
                # allow a __delete__ property to be set to delete objects
                del d1[k]
            else:
                d1[k] = update(d1.get(k, {}), v, overwrite)
        elif isinstance(v, (tuple, list)) and all(
            isinstance(li, (none_type, dict)) for li in v  # type: ignore
        ):
            # a list of dicts and/or none_type
            orig_list = d1.get(k, [])
            new_list = []
            pairs = list(zip_longest(orig_list, v, fillvalue=None))
            for orig_item, new_item in pairs:
                if orig_item is None:
                    orig_item = (
                        {}
                    )  # can't use {} for fillvalue as only one dict created/modified!
                if new_item is None:
                    new_item = {}

                if new_item.get("__delete__", False):
                    d = None  # orig_list.remove(orig_item) # remove the item to delete
                else:
                    d = update(orig_item, new_item, overwrite)

                if d is not None:
                    new_list.append(d)
            d1[k] = new_list
        else:
            if k in d1 and v == "__delete__":
                del d1[k]
            else:
                if overwrite is True or k not in d1:
                    d1[k] = v
    return d1


def dict_move_to_end(ordered_dict, key):
    ordered_dict.move_to_end(key)
