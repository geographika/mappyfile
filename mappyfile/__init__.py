# allow high-level functions to be accessed directly from the mappyfile module
from mappyfile.utils import load, loads, find, findall, dumps, write

__version__ = "0.4.1"

__all__ = ['load', 'loads', 'find', 'findall', 'dumps', 'write']
