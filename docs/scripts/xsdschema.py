"""
Use forked version to get lxml as a wheel
pip install git+https://github.com/geographika/xsdtojson.git
"""
import xsdtojson

from xsdtojson import xsd_to_json_schema

xsd_file = r"D:\GitHub\mapserver\xmlmapfile\mapfile.xsd"

json_schema = xsd_to_json_schema(xsd_file)
print(json_schema)