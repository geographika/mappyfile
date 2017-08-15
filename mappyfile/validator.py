import json
import os
import jsonschema
import logging


def get_schema(schema_name):
    """
    Had to remove the id property from map.json or it uses URLs for validation
    See various issues at https://github.com/Julian/jsonschema/pull/306
    """
    schema_path = os.path.join(os.path.dirname(__file__), "schemas")
    schema = os.path.join(schema_path, schema_name)
    assert(os.path.isfile(schema))

    # need to set a full file URI to the base schema
    schema_path = "file:///{}".format(os.path.abspath(schema)
                                      ).replace("\\", "/")
    return schema_path, json.load(open(schema))


def validate(d, schema_name="map.json"):

    jsn = json.loads(json.dumps(d))
    schema_path, schema = get_schema(schema_name)

    resolver = jsonschema.RefResolver(schema_path, None)

    try:
        jsonschema.validate(jsn, schema, resolver=resolver)
    except jsonschema.ValidationError as ex:
        logging.error(ex)
        return False

    return True
