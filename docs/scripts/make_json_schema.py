"""
jsonref

Docs

C:\VirtualEnvs\mappyfile\Scripts\activate.bat
SET "input_folder=D:\GitHub\mappyfile\mappyfile\schemas"
SET "output_folder=D:\GitHub\mappyfile\docs\schemas\"
jsonschema2rst %input_folder% %output_folder%

"""

from pprint import pprint
import jsonref
from jsonref import JsonRef

# Sample JSON data, like from json.load
document = {
    "data": ["a", "b", "c"],
    "reference": {"$ref": "#/data/1"}
}

import os
d = r"D:/GitHub/mappyfile/mappyfile/schemas"
os.chdir(d)
fn = "map.json"

uri = "file:///D:/GitHub/mappyfile/mappyfile/schemas/"
with open(fn) as f:
    j = jsonref.load(f, base_uri=uri)

jsn = jsonref.dumps(j, indent=4, sort_keys=False)

with open("../../docs/schemas/mapfile.json", "w") as f:
    f.write(jsonref.dumps(j, indent=4, sort_keys=False))

## The JsonRef.replace_refs class method will return a copy of the document
## with refs replaced by :class:`JsonRef` objects
#pprint(JsonRef.replace_refs(document))

print("Done!")