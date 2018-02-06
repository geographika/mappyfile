import logging
import pkg_resources
import sys
from types import ModuleType

plugins = ModuleType('mappyfile.plugins')
sys.modules['mappyfile.plugins'] = plugins

for ep in pkg_resources.iter_entry_points(group='mappyfile.plugins'):
    setattr(plugins, ep.name, ep.load())

# allow high-level functions to be accessed directly from the mappyfile module
from mappyfile.utils import load, loads, find, findall, dumps, write

__version__ = "0.6.3"

__all__ = ['load', 'loads', 'find', 'findall', 'dumps', 'write']

# Set default logging handler to avoid "No handler found" warnings.

try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger("mappyfile").addHandler(NullHandler())
