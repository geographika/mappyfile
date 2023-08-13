# =================================================================
#
# Authors: Seth Girvin
#
# Copyright (c) 2020 Seth Girvin
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

from __future__ import annotations
import json
import os
from collections import OrderedDict
import logging
import jsonschema
import jsonref
from mappyfile import dictutils
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT4
from typing import Any


log = logging.getLogger("mappyfile")


class Validator:
    def __init__(self):
        self.schemas = {}
        self.expanded_schemas = {}

    def get_schema_path(self, schemas_folder: str) -> str:
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
        root_schema_path = f"file://{host}/{schemas_folder}/"

        return root_schema_path

    def get_schemas_folder(self) -> str:
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), "schemas")

    def get_schema_file(self, schema_name: str) -> str:
        file_extension = os.path.splitext(schema_name)[1]

        # when loading from the schema files the ref already includes .json
        if file_extension != ".json":
            schema_name += ".json"

        schemas_folder = self.get_schemas_folder()
        schema_file = os.path.join(schemas_folder, schema_name)

        if not os.path.isfile(schema_file):
            raise IOError(f"The file {schema_file} does not exist")

        return schema_file

    def get_json_from_file(self, schema_name: str):
        if schema_name not in self.schemas:
            schema_file = self.get_schema_file(schema_name)
            with open(schema_file, encoding="utf-8") as f:
                try:
                    jsn_schema = json.load(f)
                except ValueError as ex:
                    log.error("Could not load %s", schema_file)
                    raise ex

            # cache the schema contents to avoid re-reading the file a second time
            self.schemas[schema_name] = jsn_schema
        else:
            jsn_schema = self.schemas[schema_name]

        return jsn_schema

    def retrieve_from_filesystem(self, schema_name: str):
        jsn_schema = self.get_json_from_file(schema_name)
        return Resource.from_contents(jsn_schema, default_specification=DRAFT4)

    def is_valid_for_version(self, d: dict, version: float) -> bool:
        """
        Check if the dict object has a metadata dict
        and if it does then check if the supplied
        version is valid against and minVersion or maxVersion
        values
        """
        if "metadata" in d:
            md = d["metadata"]
            min_version = md.get("minVersion", 0.0)
            max_version = md.get("maxVersion", 1000.0)
            if version < min_version or version > max_version:
                return False

        return True

    def get_versioned_schema(
        self, version: (float | None), schema_name: str = "map"
    ) -> dict:
        """
        Get a fully expanded JSON schema for a specific MapServer
        version. Optionally provide a schema_name to return an expanded
        subsection of the full schema.
        """
        jsn_schema = self.get_expanded_schema(schema_name, version)

        if version:
            # remove any properties based on minVersion and maxVersion
            properties = jsn_schema["properties"]
            jsn_schema["properties"] = self.get_versioned_properties(
                properties, version
            )

        return jsn_schema

    def get_versioned_properties(self, properties: dict, version: float) -> dict:
        """
        For a dict object recursively check each child object
        to see if it is valid for the supplied version
        """
        keys_copy = list(properties.keys())

        for key in keys_copy:
            v = properties[key]
            if isinstance(v, dict):
                if self.is_valid_for_version(v, version) is False:
                    del properties[key]
                self.get_versioned_properties(v, version)
            elif isinstance(v, list):
                valid_list = []
                for props in v:
                    if isinstance(props, dict):
                        if self.is_valid_for_version(props, version) is True:
                            valid_list.append(props)
                    else:
                        valid_list.append(props)
                properties[key] = valid_list

        return properties

    def get_schema_validator(self, schema_name: str) -> jsonschema.Draft4Validator:
        """
        Had to remove the id property from map.json or it uses URLs for validation
        See various issues at https://github.com/Julian/jsonschema/pull/306
        This is fixed in versions after Draft4
        """

        jsn_schema = self.get_json_from_file(schema_name)

        registry: Registry = Registry(retrieve=self.retrieve_from_filesystem)  # type: ignore

        validator = jsonschema.Draft4Validator(schema=jsn_schema, registry=registry)  # type: ignore
        # validator.check_schema(jsn_schema) # check schema is valid - commented out as for testing only

        return validator

    def convert_lowercase(self, x: Any) -> Any:
        if isinstance(x, list):
            return [self.convert_lowercase(v) for v in x]

        if isinstance(x, dict):
            return OrderedDict(
                (k.lower(), self.convert_lowercase(v)) for k, v in x.items()
            )

        if isinstance(x, (str, bytes)):
            x = x.lower()

        return x

    def create_message(
        self, rootdict: dict, path: str, error, add_comments: bool
    ) -> dict:
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
            d = dictutils.findkey(rootdict, *path)
            key = d["__type__"]
        else:
            key = path[-1]
            d = dictutils.findkey(rootdict, *path[:-1])

        error_message = f"ERROR: Invalid value in {key.upper()}"

        # add a comment to the dict structure

        if add_comments:
            if "__comments__" not in d:
                d["__comments__"] = OrderedDict()

            d["__comments__"][key] = f"# {error_message}"

        error_dict = {"error": error.message, "message": error_message}

        # add in details of the error line, when Mapfile was parsed to
        # include position details

        if "__position__" in d:
            if not path or key not in d["__position__"]:
                # position for the root object is stored in the root of the dict
                pd = d["__position__"]
            else:
                pd = d["__position__"][key]

            error_dict["line"] = pd.get("line")
            error_dict["column"] = pd.get("column")

        return error_dict

    def get_error_messages(
        self, d: dict, errors: list[Any], add_comments: bool
    ) -> list[dict]:
        error_messages = []

        for error in errors:
            pth = error.absolute_path
            pth = list(pth)  # convert deque to list
            em = self.create_message(d, pth, error, add_comments)
            error_messages.append(em)

        return error_messages

    def _get_errors(
        self, d: dict, validator: jsonschema.Draft4Validator, add_comments: bool
    ) -> list[dict]:
        lowercase_dict = self.convert_lowercase(d)
        jsn = json.loads(json.dumps(lowercase_dict), object_pairs_hook=OrderedDict)

        errors = list(validator.iter_errors(jsn))
        error_messages = self.get_error_messages(d, errors, add_comments)

        return error_messages

    def validate(
        self,
        value: Any,
        add_comments: bool = False,
        schema_name: str = "map",
        version: (float | None) = None,
    ):
        """
        verbose - also return the jsonschema error details
        """
        if version:
            jsn_schema = self.get_versioned_schema(version, schema_name)
            validator = jsonschema.Draft4Validator(schema=jsn_schema)
        else:
            validator = self.get_schema_validator(schema_name)

        error_messages = []

        if isinstance(value, list):
            for d in value:
                error_messages += self._get_errors(d, validator, add_comments)
        else:
            error_messages = self._get_errors(value, validator, add_comments)

        return error_messages

    def get_expanded_schema(
        self, schema_name: str, version: (float | None) = None
    ) -> dict:
        """
        Return a schema file with all $ref properties expanded
        """

        # ensure we cache per version to handle validator reuse
        if version is not None:
            cache_schema_name = schema_name + str(version)
        else:
            cache_schema_name = schema_name

        if cache_schema_name not in self.expanded_schemas:
            fn = self.get_schema_file(schema_name)
            schemas_folder = self.get_schemas_folder()
            base_uri = self.get_schema_path(schemas_folder)

            with open(fn, encoding="utf-8") as f:
                jsn_schema = jsonref.load(f, base_uri=base_uri)

                # cache the schema for future use
                self.expanded_schemas[cache_schema_name] = jsn_schema
        else:
            jsn_schema = self.expanded_schemas[cache_schema_name]

        return jsn_schema
