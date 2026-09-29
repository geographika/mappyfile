import logging
import glob
import json
import os
import re
import pytest
import mappyfile
from mappyfile.parser import Parser
from mappyfile.pprint import PrettyPrinter
from mappyfile.transformer import MapfileToDict
from mappyfile.validator import Validator


def output(s, include_position=True, schema_name="map"):
    """
    Parse, transform, validate, and pretty print
    the result
    """
    p = Parser()
    m = MapfileToDict(include_position=include_position)
    ast = p.parse(s)
    logging.debug(ast.pretty())
    d = m.transform(ast)
    logging.debug(json.dumps(d, indent=4))
    v = Validator()
    errors = v.validate(d, schema_name=schema_name)
    logging.error(errors)
    pp = PrettyPrinter(indent=0, newlinechar=" ", quote="'")
    s = pp.pprint(d)
    logging.debug(s)
    assert len(errors) == 0
    return s


def test_only_style_and_symbol_are_attribute_keywords():
    """
    The grammar lets only STYLE and SYMBOL be a block keyword and an attribute key,
    so no other block keyword may be a plain attribute in any schema
    """
    folder = os.path.dirname(mappyfile.__file__)
    grammar = open(os.path.join(folder, "mapfile.lark"), encoding="utf-8").read()
    rule = re.search(r"!composite_type:(.*?)\n\n", grammar, re.S)
    assert rule is not None
    keywords = set(re.findall(r'"(\w+)"i', rule.group(1))) | {"STYLE", "SYMBOL"}
    schemas = {}
    for fn in glob.glob(os.path.join(folder, "schemas", "*.json")):
        schemas[os.path.basename(fn)] = json.load(open(fn, encoding="utf-8"))

    def is_block(prop):
        if "$ref" in prop:
            return is_block(schemas[prop["$ref"]])
        if prop.get("type") == "object":
            return True
        if prop.get("type") == "array":
            return is_block(prop.get("items", {}))
        alternatives = prop.get("allOf") or prop.get("oneOf") or prop.get("anyOf")
        return bool(alternatives) and all(is_block(a) for a in alternatives)

    attribute_keywords = {
        kw
        for kw in keywords
        for schema in schemas.values()
        if kw.lower() in schema.get("properties", {})
        and not is_block(schema["properties"][kw.lower()])
    }
    assert attribute_keywords == {"STYLE", "SYMBOL"}


def test_symbol_keys_cover_the_schema():
    """
    A SYMBOL block is recognised by its first key, so every key in the symbol
    schema must be in the grammar, apart from the blocks it has rules for
    """
    folder = os.path.dirname(mappyfile.__file__)
    grammar = open(os.path.join(folder, "mapfile.lark"), encoding="utf-8").read()
    rule = re.search(r"symbol_key:(.*?)\n\n", grammar, re.S)
    assert rule is not None
    keys = set(re.findall(r'"(\w+)"i', rule.group(1)))
    schema = json.load(open(os.path.join(folder, "schemas", "symbol.json"), encoding="utf-8"))
    properties = {k.upper() for k in schema["properties"] if not k.startswith("__")}
    assert properties - {"POINTS"} <= keys


def test_symbolset_include():
    s = """
    MAP
        NAME "Test"
        SYMBOLSET "./symbolset.txt"
        SIZE 200 200
    END
    """

    print(output(s, schema_name="map"))
    exp = "MAP NAME 'Test' SYMBOLSET './symbolset.txt' SIZE 200 200 END"
    assert output(s, schema_name="map") == exp


def test_symbolset_file():
    s = """
    SYMBOLSET
        SYMBOL
            NAME 'default-circle'
            TYPE ELLIPSE
            FILLED TRUE
            POINTS
                1 1
            END
        END
        SYMBOL
            NAME 'other-circle'
            TYPE ELLIPSE
            FILLED FALSE
            POINTS
                1 1
            END
        END
    END
    """

    print(output(s, schema_name="symbolset"))
    exp = (
        "SYMBOLSET SYMBOL NAME 'default-circle' TYPE ELLIPSE FILLED TRUE POINTS 1 1 END "
        "END SYMBOL NAME 'other-circle' TYPE ELLIPSE FILLED FALSE POINTS 1 1 END END END"
    )
    assert output(s, schema_name="symbolset") == exp


def run_tests():
    pytest.main(["tests/test_symbolset.py"])


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    run_tests()
    print("Done!")
