import sys
import logging
import numbers
from mappyfile.tokens import COMPOSITE_NAMES, SINGLETON_COMPOSITE_NAMES
from mappyfile.validator import Validator

log = logging.getLogger("mappyfile")

PY2 = sys.version_info[0] < 3
if PY2:
    str = unicode # NOQA


class Quoter(object):
    """
    A class to handle adding and standardising quotes around strings
    """
    def __init__(self, quote='"'):

        assert (quote == "'" or quote == '"')

        self.quote = quote

        if self.quote == "'":
            self.altquote = '"'
        else:
            self.altquote = "'"

    def add_quotes(self, val):
        return self._add_quotes(val, self.quote)

    def add_altquotes(self, val):
        return self._add_quotes(val, self.altquote)

    def _add_quotes(self, val, quote):
        return u"{}{}{}".format(quote, val, quote)

    def in_quotes(self, val):
        return self._in_quotes(val, self.quote) or self._in_quotes(val, self.altquote)

    def _in_quotes(self, val, char):
        return val.startswith(char) and val.endswith(char)

    def escape_quotes(self, val):
        """
        Escape any quotes in a value
        """
        if self.is_string(val) and self._in_quotes(val, self.quote):
            # make sure any previously escaped quotes are not re-escaped
            middle = self.remove_quotes(val).replace("\\" + self.quote, self.quote)
            middle = middle.replace(self.quote, "\\" + self.quote)
            val = self.add_quotes(middle)

        return val

    def is_string(self, val):
        # check for bytes as str is aliased to unicode in Python2
        return isinstance(val, (bytes, str))

    def remove_quotes(self, val):

        if isinstance(val, list):
            return list(map(self.remove_quotes, val))

        if not self.is_string(val):
            return val

        if self.in_quotes(val):
            return val[1:-1]
        else:
            return val

    def in_brackets(self, val):
        val = val.strip()
        return val.startswith("[") and val.endswith("]")

    def in_parenthesis(self, val):
        val = val.strip()
        return val.startswith("(") and val.endswith(")")

    def in_slashes(self, val):
        val = val.strip()
        return self._in_quotes(val, "/")

    def standardise_quotes(self, val):
        """
        Change the quotes used to wrap a value to the pprint default
        E.g. "val" to 'val' or 'val' to "val"
        """
        if self._in_quotes(val, self.altquote):
            middle = self.remove_quotes(val)
            val = self.add_quotes(middle)

        return self.escape_quotes(val)


class PrettyPrinter(object):
    def __init__(self, indent=4, spacer=" ", quote='"', newlinechar="\n"):
        """
        Option use "\t" for spacer with an indent of 1
        """

        assert (quote == "'" or quote == '"')

        self.indent = indent
        self.spacer = spacer * self.indent
        self.newlinechar = newlinechar
        self.quoter = Quoter(quote)
        self.end = u"END"
        self.validator = Validator()

    def whitespace(self, level, indent):
        return self.spacer * (level + indent)

    def singular(self, s):
        if s == 'points':
            return s
        elif s.endswith('es'):
            return s[:-2]
        return s[:-1]

    def add_start_line(self, key, level):
        return self.whitespace(level, 1) + key.upper()

    def add_end_line(self, level, indent):
        return self.whitespace(level, indent) + self.end

    def __format_line(self, spacer, key, value):

        tmpl = u"{spacer}{key} {value}"
        d = {
            "spacer": spacer,
            "key": key,
            "value": value
        }
        return tmpl.format(**d)

    def process_key_dict(self, key, d, level):
        """
        Process key value dicts e.g. METADATA "key" "value"
        """
        lines = [self.add_start_line(key, level)]
        lines += self.process_dict(d, level)
        lines.append(self.add_end_line(level, 1))

        return lines

    def process_dict(self, d, level):
        """
        Process keys and values within a block
        """
        lines = []

        for k, v in d.items():
            if k != "__type__":
                k = self.quoter.add_quotes(k)
                v = self.quoter.add_quotes(v)
                lines.append(self.__format_line(self.whitespace(level, 2), k, v))

        return lines

    def process_config_dict(self, key, d, level):
        """
        Process the CONFIG block
        """
        lines = []
        for k, v in d.items():
            k = "CONFIG {}".format(self.quoter.add_quotes(k.upper()))
            v = self.quoter.add_quotes(v)
            lines.append(self.__format_line(self.whitespace(level, 1), k, v))
        return lines

    def process_repeated_list(self, key, lst, level):
        """
        Process blocks of repeated keys e.g. FORMATOPTION
        """
        lines = []

        for v in lst:
            k = key.upper()
            v = self.quoter.add_quotes(v)
            lines.append(self.__format_line(self.whitespace(level, 1), k, v))

        return lines

    def process_projection(self, key, lst, level):

        lines = [self.add_start_line(key, level)]

        if len(lst) == 1 and lst[0].upper() == "AUTO":
            lines.append(u"{}{}".format(self.whitespace(level, 2), "AUTO"))
        else:
            for v in lst:
                v = self.quoter.add_quotes(v)
                lines.append(u"{}{}".format(self.whitespace(level, 2), v))

        lines.append(self.add_end_line(level, 1))
        return lines

    def format_pair_list(self, key, pair_list, level):
        """
        Process lists of pairs (e.g. PATTERN block)
        """

        lines = [self.add_start_line(key, level)]

        list_spacer = self.spacer * (level + 2)
        pairs = ["{}{} {}".format(list_spacer, p[0], p[1]) for p in pair_list]
        lines += pairs

        lines.append(self.add_end_line(level, 1))

        return lines

    def format_repeated_pair_list(self, key, root_list, level):
        """
        Process repeated lists of pairs e.g. POINTs blocks
        """

        lines = []

        for pair_list in root_list:
            lines += self.format_pair_list(key, pair_list, level)

        return lines

    def is_composite(self, val):

        if isinstance(val, dict) and "__type__" in val.keys():
            return True
        else:
            return False

    def is_hidden_container(self, key, val):
        """
        The key is not one of the Mapfile keywords, and its
        values are a list
        """

        if key in ("layers", "classes", "styles", "symbols", "labels",
                   "outputformats", "features", "scaletokens",
                   "composites") and isinstance(val, list):
            return True
        else:
            return False

    def pprint(self, composites):
        """
        Print out a nicely indented Mapfile
        """

        # if only a single composite is used then cast to list
        # and allow for multiple root composites

        if not isinstance(composites, list):
            composites = [composites]

        lines = []

        for composite in composites:
            type_ = composite["__type__"]
            if type_ in ("metadata", "validation"):
                # types are being parsed directly, and not as an attr of a parent
                lines += self.process_key_dict(type_, composite, level=0)
            else:
                lines += self._format(composite)

        return self.newlinechar.join(lines)

    def get_attribute_properties(self, type_, attr):

        jsn_schema, resolver = self.validator.get_schema(type_)
        props = jsn_schema["properties"]

        # check if a value needs to be quoted or not, by referring to the Json schema
        try:
            attr_props = props[attr]
        except KeyError as ex:
            log.error("The key '{}' was not found in the JSON schema for '{}'".format(attr, type_))
            log.error(ex)
            return {}

        if "$ref" in attr_props:
            _, attr_props = resolver.resolve(attr_props["$ref"])

        return attr_props

    def is_expression(self, option):
        return "description" in option and (option["description"] == "expression")

    def check_options_list(self, options_list, value):
        for option in options_list:
            if "enum" in option and value.lower() in option["enum"]:
                return value.upper()
            elif self.is_expression(option):
                if value.endswith("'i") or value.endswith('"i'):
                    return value

        if self.quoter.in_slashes(value):
            return value
        else:
            return self.quoter.add_quotes(value)

    def format_value(self, attr, attr_props, value):
        """
        TODO - refactor and add more specific tests (particularly for expressions)
        """
        if isinstance(value, bool):
            return str(value).upper()

        if any(i in ["enum"] for i in attr_props):
            if not isinstance(value, numbers.Number):
                return value.upper()  # value is from a set list, no need for quote
            else:
                return value

        if "type" in attr_props and attr_props["type"] == "string":  # and "enum" not in attr_props
            # check schemas for expressions and handle accordingly
            if self.is_expression(attr_props) and self.quoter.in_slashes(value):
                return value
            elif self.is_expression(attr_props) and (value.endswith("'i") or value.endswith('"i')):
                # for case insensitive regex
                return value
            else:
                return self.quoter.add_quotes(value)

        # expressions can be one of a string or an expression in brackets
        if any(i in ["oneOf", "anyOf"] for i in attr_props):  # and check that type string is in list
            if "oneOf" in attr_props:
                options_list = attr_props["oneOf"]
            else:
                options_list = attr_props["anyOf"]
            if isinstance(value, (str)):
                if self.quoter.in_parenthesis(value):
                    pass
                elif self.quoter.in_brackets(value) and attr != "text":
                    # TEXT expressions are often "[field1]-[field2]" so need to leave quotes for these
                    pass
                elif value.startswith("NOT ") and self.quoter.in_parenthesis(value[4:]):
                    value = "NOT {}".format(value[4:])
                else:
                    value = self.check_options_list(options_list, value)

        if isinstance(value, list):
            new_values = []

            for v in value:
                if not isinstance(v, numbers.Number):
                    v = self.quoter.add_quotes(v)
                new_values.append(v)

            value = " ".join(list(map(str, new_values)))
        else:
            value = self.quoter.escape_quotes(value)

        return value

    def process_attribute(self, type_, attr, value, level):
        """
        Process one of the main composite types (see the type_ value)
        """

        attr_props = self.get_attribute_properties(type_, attr)
        value = self.format_value(attr, attr_props, value)
        line = self.__format_line(self.whitespace(level, 1), attr.upper(), value)

        return line

    def _format(self, composite, level=0):

        lines = []

        if isinstance(composite, dict) and '__type__' in composite.keys():
            type_ = composite['__type__']
            assert(type_ in COMPOSITE_NAMES.union(SINGLETON_COMPOSITE_NAMES))
            is_hidden = False
            s = self.whitespace(level, 0) + type_.upper()
            lines.append(s)

        for attr, value in composite.items():
            if attr == "__type__":
                # skip this hidden attribute
                continue
            elif self.is_hidden_container(attr, value):
                # now recursively print all the items in the container
                for v in value:
                    lines += self._format(v, level + 1)
            elif attr == "pattern":
                lines += self.format_pair_list(attr, value, level)
            elif attr in ("metadata", "validation", "values"):
                # as metadata and values are also composites, process them before calling self._format
                lines += self.process_key_dict(attr, value, level)
            elif attr == "projection":
                lines += self.process_projection(attr, value, level)
            elif attr in ("processing", "formatoption", "include"):
                lines += self.process_repeated_list(attr, value, level)
            elif attr == "points":
                lines += self.format_repeated_pair_list(attr, value, level)
            elif attr == "config":
                lines += self.process_config_dict(attr, value, level)
            elif self.is_composite(value):
                lines += self._format(value, level + 1)  # recursively add the child class
            else:
                # standard key value pair
                lines.append(self.process_attribute(type_, attr, value, level))

        if not is_hidden:
            # close the container block with an END
            lines.append(self.add_end_line(level, 0))

        return lines
