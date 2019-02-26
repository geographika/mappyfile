import json
import os
import sys
from collections import OrderedDict
import logging
import jsonschema
import jsonref
import mappyfile as utils

log = logging.getLogger("mappyfile")

PY2 = sys.version_info[0] < 3
if PY2:
    str = unicode # NOQA


class Validator(object):

    def __init__(self):
        self.schemas = {}
        self.expanded_schemas = {}

    def get_schema_path(self, schemas_folder):
        """
        Return a file protocol URI e.g. file:///D:/mappyfile/mappyfile/schemas/ on Windows
        and file:////home/user/mappyfile/mappyfile/schemas/ on Linux
        """

        # replace any Windows path back slashes with forward slashes
        schemas_folder = schemas_folder.replace("\\", "/")

        # HACK Python 2.7 on Linux seems to remove the root slash
        # so add this back in
        if schemas_folder.startswith("/"):
            schemas_folder = "/" + schemas_folder

        host = ""
        root_schema_path = "file://{}/{}".format(host, schemas_folder) + "/"

        return root_schema_path

    def get_schemas_folder(self):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), "schemas")

    def get_schema_file(self, schema_name):

        schema_name += ".json"
        schemas_folder = self.get_schemas_folder()
        schema_file = os.path.join(schemas_folder, schema_name)

        if not os.path.isfile(schema_file):
            raise IOError("The file %s does not exist" % schema_file)

        return schema_file

    def get_schema_validator(self, schema_name):
        """
        Had to remove the id property from map.json or it uses URLs for validation
        See various issues at https://github.com/Julian/jsonschema/pull/306
        """

        if schema_name not in self.schemas:
            schema_file = self.get_schema_file(schema_name)
            with open(schema_file) as f:
                try:
                    jsn_schema = json.load(f)
                except ValueError as ex:
                    log.error("Could not load %s", schema_file)
                    raise ex

            schemas_folder = self.get_schemas_folder()
            root_schema_path = self.get_schema_path(schemas_folder)
            resolver = jsonschema.RefResolver(root_schema_path, None)
            # cache the schema for future use
            self.schemas[schema_name] = (jsn_schema, resolver)
        else:
            jsn_schema, resolver = self.schemas[schema_name]

        validator = jsonschema.Draft4Validator(schema=jsn_schema, resolver=resolver)
        # validator.check_schema(jsn_schema) # check schema is valid

        return validator

    def convert_lowercase(self, x):

        if isinstance(x, list):
            return [self.convert_lowercase(v) for v in x]
        elif isinstance(x, dict):
            return OrderedDict((k.lower(), self.convert_lowercase(v)) for k, v in x.items())
        else:
            if isinstance(x, (str, bytes)):
                x = x.lower()

        return x

    def create_message(self, rootdict, path, error, add_comments):
        """
        Add a validation comment to the dictionary
        path is the path to the error object, it can be empty if the error is in the root object
        http://python-jsonschema.readthedocs.io/en/latest/errors/#jsonschema.exceptions.ValidationError.absolute_path
        It can also reference an object in a list e.g. [u'layers', 0]

        Unfortunately it is not currently possible to get the name of the failing property from the
        JSONSchema error object, even though it is in the error message.
        See https://github.com/Julian/jsonschema/issues/119
        """

        if not path:
            # error applies to the root type
            d = rootdict
            key = d["__type__"]
        elif isinstance(path[-1], int):
            # the error is on an object in a list
            d = utils.findkey(rootdict, *path)
            key = d["__type__"]
        else:
            key = path[-1]
            d = utils.findkey(rootdict, *path[:-1])

        error_message = "ERROR: Invalid value in {}".format(key.upper())

        # add a comment to the dict structure

        if add_comments:
            if "__comments__" not in d:
                d["__comments__"] = OrderedDict()

            d["__comments__"][key] = "# {}".format(error_message)

        error_message = {"error": error.message,
                         "message": error_message}

        # add in details of the error line, when Mapfile was parsed to
        # include position details

        if "__position__" in d:
            if not path:
                # position for the root object is stored in the root of the dict
                pd = d["__position__"]
            else:
                pd = d["__position__"][key]

            error_message["line"] = pd.get("line")
            error_message["column"] = pd.get("column")

        return error_message

    def get_error_messages(self, d, errors, add_comments):

        error_messages = []

        for error in errors:
            pth = error.absolute_path
            pth = list(pth)  # convert deque to list
            em = self.create_message(d, pth, error, add_comments)
            error_messages.append(em)

        return error_messages

    def _validate(self, d, validator, add_comments, schema_name):
        lowercase_dict = self.convert_lowercase(d)
        jsn = json.loads(json.dumps(lowercase_dict), object_pairs_hook=OrderedDict)

        errors = list(validator.iter_errors(jsn))
        error_messages = self.get_error_messages(d, errors, add_comments)

        return error_messages

    def validate(self, value, add_comments=False, schema_name="map"):
        """
        verbose - also return the jsonschema error details
        """
        validator = self.get_schema_validator(schema_name)

        error_messages = []

        if isinstance(value, list):
            for d in value:
                error_messages += self._validate(d, validator, add_comments, schema_name)
        else:
            error_messages = self._validate(value, validator, add_comments, schema_name)

        return error_messages

    def get_expanded_schema(self, schema_name):
        """
        Return a schema file with all $ref properties expanded
        """
        if schema_name not in self.expanded_schemas:
            fn = self.get_schema_file(schema_name)
            schemas_folder = self.get_schemas_folder()
            base_uri = self.get_schema_path(schemas_folder)

            with open(fn) as f:
                jsn_schema = jsonref.load(f, base_uri=base_uri)

                # cache the schema for future use
                self.expanded_schemas[schema_name] = jsn_schema
        else:
            jsn_schema = self.expanded_schemas[schema_name]

        return jsn_schema
