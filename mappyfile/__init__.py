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
import pkg_resources
import sys
from types import ModuleType
# allow high-level functions to be accessed directly from the mappyfile module
from mappyfile.utils import open, load, loads, find, findall, findunique, dumps, dump, save
from mappyfile.utils import findkey, update, validate, create

__version__ = "0.9.3"

__all__ = ['open', 'load', 'loads', 'find', 'findall', 'findunique', 'dumps', 'dump', 'save',
           'findkey', 'update', 'validate', 'create']


plugins = ModuleType('mappyfile.plugins')
sys.modules['mappyfile.plugins'] = plugins

for ep in pkg_resources.iter_entry_points(group='mappyfile.plugins'):
    setattr(plugins, ep.name, ep.load())

# Set default logging handler to avoid "No handler found" warnings.

try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger("mappyfile").addHandler(NullHandler())
