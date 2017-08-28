import json
import os
import jsonschema
import logging

log = logging.getLogger("mappyfile")


class Validator(object):

    def __init__(self):
        self.schemas = {}

    def get_schema(self, schema_name):
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

    def validate(self, d, schema_name="map"):

        schema_name += ".json"

        if schema_name in self.schemas.keys():
            schema, resolver = self.schemas[schema_name]
        else:
            jsn = json.loads(json.dumps(d))
            schema_path, schema = self.get_schema(schema_name)
            resolver = jsonschema.RefResolver(schema_path, None)
            self.schemas[schema_name] = (schema, resolver)

        try:
            jsonschema.validate(jsn, schema, resolver=resolver)
        except jsonschema.ValidationError as ex:
            log.error(ex)
            return False

        return True
