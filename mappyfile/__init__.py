import logging
# allow high-level functions to be accessed directly from the mappyfile module
from mappyfile.utils import load, loads, find, findall, dumps, write

__version__ = "0.6.0"

__all__ = ['load', 'loads', 'find', 'findall', 'dumps', 'write']

# Set default logging handler to avoid "No handler found" warnings.

try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger("mappyfile").addHandler(NullHandler())
