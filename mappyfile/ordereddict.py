from collections import OrderedDict
import copy
import sys


try:
    from collections.abc import Callable  # noqa
except ImportError:
    from collections import Callable  # noqa


PY2 = sys.version_info[0] < 3
if PY2:
    str = unicode # NOQA


class DefaultOrderedDict(OrderedDict):
    """
    Used for storing components
    Source: http://stackoverflow.com/a/6190500/562769
    http://code.activestate.com/recipes/523034-emulate-collectionsdefaultdict/
    """

    def __init__(self, default_factory=None, *a, **kw):
        if (default_factory is not None and not isinstance(default_factory, Callable)):
            raise TypeError('First argument must be callable')

        OrderedDict.__init__(self, *a, **kw)
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
        self[key] = value = self.default_factory()
        return value

    def __reduce__(self):
        if self.default_factory is None:
            args = tuple()
        else:
            args = self.default_factory,
        return type(self), args, None, None, iter(self.items())

    def copy(self):
        return self.__copy__()

    def __copy__(self):
        return type(self)(self.default_factory, self)

    def __deepcopy__(self, memo):
        return type(self)(self.default_factory,
                          copy.deepcopy(list(self.items())))

    def __repr__(self):
        return 'DefaultOrderedDict(%s, %s)' % (self.default_factory,
                                               OrderedDict.__repr__(self))


class CaseInsensitiveOrderedDict(DefaultOrderedDict):
    """
    Based on: https://stackoverflow.com/a/32888599/179520
    """
    @classmethod
    def _k(cls, key):
        return key.lower() if isinstance(key, (bytes, str)) else key

    def __init__(self, *args, **kwargs):
        super(CaseInsensitiveOrderedDict, self).__init__(*args, **kwargs)
        self._convert_keys()

    def __getitem__(self, key):
        return super(CaseInsensitiveOrderedDict, self).__getitem__(self.__class__._k(key))

    def __setitem__(self, key, value):
        super(CaseInsensitiveOrderedDict, self).__setitem__(self.__class__._k(key), value)

    def __delitem__(self, key):
        return super(CaseInsensitiveOrderedDict, self).__delitem__(self.__class__._k(key))

    def __contains__(self, key):
        return super(CaseInsensitiveOrderedDict, self).__contains__(self.__class__._k(key))

    def has_key(self, key):
        return key in self

    def pop(self, key, *args, **kwargs):
        return super(CaseInsensitiveOrderedDict, self).pop(self.__class__._k(key), *args, **kwargs)

    def get(self, key, *args, **kwargs):
        return super(CaseInsensitiveOrderedDict, self).get(self.__class__._k(key), *args, **kwargs)

    def setdefault(self, key, *args, **kwargs):
        return super(CaseInsensitiveOrderedDict, self).setdefault(self.__class__._k(key), *args, **kwargs)

    def update(self, E=None, **F):
        if E is not None:
            super(CaseInsensitiveOrderedDict, self).update(self.__class__(CaseInsensitiveOrderedDict, E))
        super(CaseInsensitiveOrderedDict, self).update(self.__class__(CaseInsensitiveOrderedDict, **F))

    def _convert_keys(self):
        for k in list(self.keys()):
            v = super(CaseInsensitiveOrderedDict, self).pop(k)
            self.__setitem__(k, v)
