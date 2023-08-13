"""

Validate against schema
http://www.opengeospatial.org/standards/filter
http://docs.opengeospatial.org/is/09-026r2/09-026r2.html#41
mappyfile-expressions

https://mapserver.org/ogc/sld.html#introduction
https://github.com/mapserver/mapserver/blob/branch-7-2/mapogcfiltercommon.c
https://github.com/mapserver/mapserver/blob/branch-7-2/mapogcfilter.c

https://mapserver.org/fr/mapfile/class.html

2 way conversion

Use https://github.com/martinblech/xmltodict

pip install xmltodict

<Filter>
  <OR>
  <PropertyIsEqualTo>
    <PropertyName>NAME</PropertyName>
    <Literal>Sydney</Literal>
  </PropertyIsEqualTo>
  <PropertyIsEqualTo>
  <PropertyName>NAME</PropertyName><Literal>Halifax</Literal>
  </PropertyIsEqualTo>
  </OR>
  </Filter>

"""

import logging
import json
from mappyfile.parser import Parser
from mappyfile.transformer import MapfileTransformer
from mappyfile.quoter import Quoter
import xmltodict


class ExpressionsTransformer(MapfileTransformer):
    def __init__(self):
        self.quoter = Quoter()
        self.include_position = False
        self.include_comments = False

    def start(self, t):
        return {"filter": t}

    def composite(self, t):
        print("COMPOSITE {}".format(t))
        return t
        # return t[1][1]

    def attr(self, tokens):
        # print(tokens)
        print("attr {}".format(tokens))
        return tokens[1]  # [1][1]

    def expression(self, t):
        # exp = " ".join([str(v.value) for v in t])  # convert to string for boolean expressions e.g. (true)
        # exp_dict = {}

        # if not self.quoter.in_parenthesis(exp):
        #    t[0].value = exp_dict["rule"] = exp # ({})".format(exp)

        # return t[0]
        return t

    def comparison(self, t):
        """
        <PropertyIsEqualTo>
          <PropertyName>NAME</PropertyName>
          <Literal>Sydney</Literal>
        </PropertyIsEqualTo>
        """
        assert len(t) == 3

        d = {"PropertyIsEqualTo": [t[0], t[1], t[2]]}

        # parts = [str(p.value) for p in t]
        # v = " ".join(parts)

        # v = "( {} )".format(v)
        # t[0].value = v
        # return t[0]
        return d

    def attr_bind(self, t):
        assert len(t) == 1
        # t = t[0]
        # t.value = "[{}]".format(t.value)
        attr_dict = {"PropertyName": {"#PropertyName": t[0]}}
        return attr_dict

    def or_test(self, t):
        # print("OR TEST {}".format(t))
        assert len(t) == 2
        # print(t)
        # t[0].value = "( {} OR {} )".format(t[0].value, t[1].value)
        # t[0].value = "<or> {} OR {} </or>".format(t[0].value, t[1].value)
        or_dict = {"or": [t[0], t[1]]}
        return or_dict


def output(s):
    """
    Parse, transform, and pretty print
    the result
    """
    p = Parser()
    t = ExpressionsTransformer()

    ast = p.parse(s)
    logging.debug(ast.pretty())
    print(ast.pretty())
    d = t.transform(ast)
    print(json.dumps(d, indent=4))
    return d


s = """
CLASS
    EXPRESSION (([NAME_E] < 8) OR ([VAL] = 3))
END
"""
# s = "EXPRESSION (([NAME_E] < 8) OR ([VAL] = 3))"
mydict = output(s)

print(xmltodict.unparse(mydict, pretty=True))
