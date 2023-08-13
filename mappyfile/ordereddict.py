# =================================================================
#
# Authors: Seth Girvin
#          Jason Kirtland [1]
#          Zach Kelling [2]
#          m000 [3],[4]
#
# [1] http://code.activestate.com/recipes/523034-emulate-collectionsdefaultdict/
# [2] http://stackoverflow.com/a/6190500/562769
# [3] https://stackoverflow.com/users/277172/m000
# [4] https://stackoverflow.com/a/32888599/179520
#
# Copyright (c) 2020 Seth Girvin
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

from collections import OrderedDict
import copy
from mappyfile.tokens import OBJECT_LIST_KEYS
import json


class DefaultOrderedDict(OrderedDict):
    """
    Used for storing components
    Source: http://stackoverflow.com/a/6190500/562769
    Based on: http://code.activestate.com/recipes/523034-emulate-collectionsdefaultdict/
    """

    # pylint: disable=keyword-arg-before-vararg
    def __init__(self, default_factory=None, *args, **kwargs):
        if default_factory is not None and not callable(default_factory):
            raise TypeError("First argument must be callable")

        OrderedDict.__init__(self, *args, **kwargs)
        self.default_factory = default_factory

    def __getitem__(self, key):
        key = key.lower()  # all keys should be lower-case to make editing easier

        try:
            return OrderedDict.__getitem__(self, key)
        except KeyError:
            return self.__missing__(key)

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)

        if key in OBJECT_LIST_KEYS:
            # create empty lists for keys of object lists such as "layers"
            self[key] = value = []
        else:
            self[key] = value = self.default_factory()
        return value

    def __reduce__(self):
        if self.default_factory is None:
            args: tuple = tuple()
        else:
            args = (self.default_factory,)
        return type(self), args, None, None, iter(self.items())

    def copy(self):
        return copy.copy(self)

    def __copy__(self):
        return type(self)(self.default_factory, self)

    def __deepcopy__(self, memo):
        return type(self)(self.default_factory, copy.deepcopy(list(self.items())))

    def __repr__(self):
        """
        Return a human-readable version of the dict contents
        """
        return json.dumps(self, indent=4)  # sort_keys=True


class CaseInsensitiveOrderedDict(DefaultOrderedDict):
    """
    Based on: https://stackoverflow.com/a/32888599/179520
    """

    @classmethod
    def _k(cls, key):
        return key.lower() if isinstance(key, str) else key

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._convert_keys()

    def __getitem__(self, key):
        return super().__getitem__(self.__class__._k(key))

    def __setitem__(self, key, value):
        super().__setitem__(self.__class__._k(key), value)

    def __delitem__(self, key):
        return super().__delitem__(self.__class__._k(key))

    def __contains__(self, key):
        return super().__contains__(self.__class__._k(key))

    def has_key(self, key):
        return key in self

    def pop(self, key, *args, **kwargs):
        # pylint: disable=protected-access
        return super().pop(self.__class__._k(key), *args, **kwargs)

    def get(self, key, *args, **kwargs):
        # pylint: disable=protected-access
        return super().get(self.__class__._k(key), *args, **kwargs)

    def setdefault(self, key, *args, **kwargs):
        # pylint: disable=protected-access
        return super().setdefault(self.__class__._k(key), *args, **kwargs)

    def update(self, e=None, **f):
        if e is not None:
            super().update(self.__class__(CaseInsensitiveOrderedDict, e))
        super().update(self.__class__(CaseInsensitiveOrderedDict, **f))

    def _convert_keys(self):
        for k in list(self.keys()):
            v = super().pop(k)
            self[k] = v
