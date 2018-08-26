"""
jsonref

Docs

C:\VirtualEnvs\mappyfile\Scripts\activate.bat
SET "input_folder=D:\GitHub\mappyfile\mappyfile\schemas"
SET "output_folder=D:\GitHub\mappyfile\docs\schemas\"
jsonschema2rst %input_folder% %output_folder%

"""
import os
from pprint import pprint
import jsonref
from jsonref import JsonRef

def get_full_schema(schema_dir):
    print(schema_dir)
    os.chdir(schema_dir)
    fn = "map.json"

    uri = "file:///{}/".format(schema_dir)

    with open(fn) as f:
        j = jsonref.load(f, base_uri=uri)

    jsn = jsonref.dumps(j, indent=4, sort_keys=False)
    full_schema = jsonref.dumps(j, indent=4, sort_keys=False)
    with open(r"C:\Temp\mapfile.json", "w") as f:
        f.write(full_schema)

    return full_schema

# create_versioned_schema

def update_schema(full_schema):
    if isinstance(obj, dict):
        for k in obj.keys():
            if k == bad:
                del obj[k]
            else:
                update_schema(obj[k], bad)
    elif isinstance(obj, list):
        for i in reversed(range(len(obj))):
            if obj[i] == bad:
                del obj[i]
            else:
                update_schema(obj[i], bad)

    else:
        # neither a dict nor a list, do nothing
        pass

def main(schema_dir):
    full_schema = get_full_schema(schema_dir)
    update_schema(full_schema)

if __name__ == "__main__":
    project_dir = os.path.dirname(os.path.dirname(__file__))
    schema_dir = os.path.join(project_dir, "mappyfile", "schemas")
    main(schema_dir)
    print("Done!")