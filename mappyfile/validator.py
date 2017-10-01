import json
import os
from collections import OrderedDict
import logging
import jsonschema

log = logging.getLogger("mappyfile")


class Validator(object):

    def __init__(self):
        self.schemas = {}

    def get_schema(self, schema_name):
        """
        Had to remove the id property from map.json or it uses URLs for validation
        See various issues at https://github.com/Julian/jsonschema/pull/306
        """

        schema_name += ".json"

        if schema_name not in self.schemas.keys():
            schemas_folder = os.path.join(os.path.dirname(__file__), "schemas")
            schema = os.path.join(schemas_folder, schema_name)
            if not os.path.isfile(schema):
                raise IOError("The file %s does not exist" % schema)

            # need to set a full file URI to the base schema
            root_schema_path = "file:///{}".format(os.path.abspath(schema)).replace("\\", "/")

            with open(schema) as f:
                try:
                    jsn_schema = json.loads(f.read())
                except ValueError as ex:
                    log.error("Could not load %s", schema)
                    raise ex

            resolver = jsonschema.RefResolver(root_schema_path, None)
            # cache the schema for future use
            self.schemas[schema_name] = (jsn_schema, resolver)
        else:
            jsn_schema, resolver = self.schemas[schema_name]

        return jsn_schema, resolver

    def convert_lowercase(self, x):

        if isinstance(x, list):
            return [self.convert_lowercase(v) for v in x]
        elif isinstance(x, dict):
            return OrderedDict((k.lower(), self.convert_lowercase(v)) for k, v in x.items())
        else:
            if isinstance(x, (str, unicode)):
                x = x.lower()

        return x

    def validate(self, d, schema_name="map"):

        jsn_schema, resolver = self.get_schema(schema_name)
        lowercase_dict = self.convert_lowercase(d)

        jsn = json.loads(json.dumps(lowercase_dict), object_pairs_hook=OrderedDict)

        try:
            jsonschema.validate(jsn, jsn_schema, resolver=resolver)
        except jsonschema.ValidationError as ex:
            log.error(ex)
            return False

        return True
