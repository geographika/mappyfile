# =================================================================
#
# Authors: Seth Girvin
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

import logging
import importlib.metadata
from logging import NullHandler
import sys
from types import ModuleType

# allow high-level functions to be accessed directly from the mappyfile module
# pylint: disable=redefined-builtin
from mappyfile.utils import (
    open,
    create,
    load,
    loads,
    dumps,
    dump,
    save,
    validate,
)
from mappyfile.dictutils import (
    find,
    findall,
    findkey,
    findunique,
    update,
    dict_move_to_end,
)

__version__ = "1.0.2"

__all__ = [
    "open",
    "load",
    "loads",
    "find",
    "findall",
    "findunique",
    "dumps",
    "dump",
    "save",
    "findkey",
    "update",
    "validate",
    "create",
    "dict_move_to_end",
]


module = ModuleType("mappyfile.plugins")
sys.modules["mappyfile.plugins"] = module

if sys.version_info >= (3, 10):
    plugins = importlib.metadata.entry_points(group="mappyfile.plugins")
else:
    plugins = importlib.metadata.entry_points().get("mappyfile.plugins", [])

for plugin in plugins:
    setattr(module, plugin.name, plugin.load())

# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger("mappyfile").addHandler(NullHandler())
