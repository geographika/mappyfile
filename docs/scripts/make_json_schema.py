r"""
jsonref

Docs

C:\VirtualEnvs\mappyfile\Scripts\activate.bat
SET "input_folder=D:\GitHub\mappyfile\mappyfile\schemas"
SET "output_folder=D:\GitHub\mappyfile\docs\schemas\"
jsonschema2rst %input_folder% %output_folder%

"""

import os
import json
from jsonschema import Draft4Validator
import glob
from mappyfile.validator import Validator


def check_schema(fn):
    print(fn)

    with open(fn) as f:
        jsn = json.load(f)
        Draft4Validator.check_schema(jsn)


def save_full_schema(output_file):
    validator = Validator()

    # check individual schema files

    fld = validator.get_schemas_folder()
    jsn_files = glob.glob(fld + "/*.json")

    for fn in jsn_files:
        check_schema(fn)

    # now check the combined schema
    jsn = validator.get_versioned_schema()
    full_schema = json.dumps(jsn, indent=4, sort_keys=False)

    with open(output_file, "w") as f:
        f.write(full_schema)

    check_schema(output_file)


if __name__ == "__main__":
    project_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    output_file = os.path.join(project_dir, "docs", "schemas", "mapfile.json")
    print(output_file)
    save_full_schema(output_file)
    print("Done!")
