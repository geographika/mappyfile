// =================================================================
// 
// Authors: Erez Shinan, Seth Girvin
// 
// Copyright (c) 2020 Seth Girvin
// 
// Permission is hereby granted, free of charge, to any person
// obtaining a copy of this software and associated documentation
// files (the "Software"), to deal in the Software without
// restriction, including without limitation the rights to use,
// copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the
// Software is furnished to do so, subject to the following
// conditions:
// 
// The above copyright notice and this permission notice shall be
// included in all copies or substantial portions of the Software.
// 
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
// EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
// OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
// NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
// HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
// WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
// FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
// OTHER DEALINGS IN THE SOFTWARE.
// 
// =================================================================

start: "SYMBOLSET"i composite_body _END   -> symbolset
     | composite+

composite: composite_type composite_body _END
       | metadata
       | validation
       | connectionoptions

composite_body: _composite_item*
_composite_item: (composite|attr|points|projection|pattern|values|config)

!projection: "PROJECTION"i (string*|AUTO) _END
!config: "CONFIG"i (string | UNQUOTED_STRING) (string | UNQUOTED_STRING)

!points: "POINTS"i num_pair* _END
!pattern: "PATTERN"i num_pair* _END

!values: "VALUES"i string_pair* _END
!metadata: "METADATA"i string_pair* _END
!validation: "VALIDATION"i string_pair* _END
!connectionoptions: "CONNECTIONOPTIONS"i string_pair* _END

attr: (UNQUOTED_STRING | composite_type) (value | UNQUOTED_STRING)
//attr: (UNQUOTED_STRING | SYMBOL) (value | UNQUOTED_STRING)
// SYMBOL is listed in composite_type but is also an attribute name

?value: string | int | float | expression | not_expression | attr_bind | path
| regexp | runtime_var | list | NULL | true | false | extent | rgb | hexcolor
| colorrange | hexcolorrange | num_pair | attr_bind_pair | attr_mixed_pair | _attr_keyword

int: SIGNED_INT
int_pair: int int
rgb: int int int
colorrange: int int int int int int
hexcolorrange: hexcolor hexcolor
hexcolor: DOUBLE_QUOTED_HEXCOLOR | SINGLE_QUOTED_HEXCOLOR

extent: (int|float) (int|float) (int|float) (int|float) 

!_attr_keyword: "AUTO"i | "HILITE"i | "SELECTED"i 

string: DOUBLE_QUOTED_STRING | SINGLE_QUOTED_STRING | ESCAPED_STRING
string_pair: (string|UNQUOTED_STRING) (string|UNQUOTED_STRING)

attr_bind_pair: attr_bind attr_bind
attr_mixed_pair: attr_bind (int|float) | (int|float) attr_bind
float: SIGNED_FLOAT
float_pair: float float
path: PATH
regexp: REGEXP1 | REGEXP2
runtime_var: RUNTIME_VAR
list: "{" (value | UNQUOTED_STRING_SPACE) ("," (value | UNQUOTED_STRING_SPACE))* "}"

num_pair: (int|float) (int|float)

attr_bind: "[" UNQUOTED_STRING "]"

not_expression: ("!"|"NOT"i) comparison
expression: "(" or_test ")"
?or_test : (or_test ("OR"i|"||"))? and_test
?and_test : (and_test ("AND"i|"&&"))? comparison
?comparison: (comparison compare_op)? sum
!compare_op: ">=" | "<" | "=*" | "==" | "=" | "!=" | "~" | "~*" | ">" | "%"
| "<=" | "IN"i | "NE"i | "EQ"i | "LE"i | "LT"i | "GE"i | "GT"i | "LIKE"i

?sum: product
    | sum "+" product -> add
    | sum "-" product -> sub

?product: unary_expr
    | product "*" unary_expr -> mul
    | product "/" unary_expr -> div
    | product "^" unary_expr -> power

?unary_expr: atom
    | "-" unary_expr -> neg
    | "+" unary_expr

?atom: (func_call | value)
// ?multiply: (multiply "*")? (func_call | value)

func_call: UNQUOTED_STRING "(" func_params ")"
func_params: value ("," value)*

!true: "TRUE"i
!false: "FALSE"i

!composite_type: "CLASS"i
            | "CLUSTER"i
            | "COMPOSITE"i
            | "FEATURE"i
            | "GRID"i
            | "JOIN"i
            | "LABEL"i
            | "LAYER"i
            | "LEADER"i
            | "LEGEND"i
            | "MAP"i
            | "OUTPUTFORMAT"i
            | "QUERYMAP"i
            | "REFERENCE"i
            | "SCALEBAR"i
            | "SCALETOKEN"i
            | "STYLE"i
            | "WEB"i
            | "SYMBOL"i

AUTO: "AUTO"i
PATH: /([a-z0-9_]*\.*\/|[a-z0-9_]+[.\/])[a-z0-9_\/\.-]+/i

// rules allow optional alphachannel
DOUBLE_QUOTED_HEXCOLOR.2: /\"#(?:[0-9a-fA-F]{3}){1,2}([0-9a-fA-F]{2})?\"/
SINGLE_QUOTED_HEXCOLOR.2: /'#(?:[0-9a-fA-F]{3}){1,2}([0-9a-fA-F]{2})?'/

NULL: "NULL"i

SIGNED_FLOAT: ["-"|"+"] FLOAT
SIGNED_INT: ["-"|"+"] INT

INT: /[0-9]+(?![_a-zA-Z])/

%import common.FLOAT

// UNQUOTED_STRING: /[a-z_][a-z0-9_\-]*/i
UNQUOTED_STRING: /[a-z0-9_\xc0-\xff\-:]+/i
UNQUOTED_STRING_SPACE: /[a-z0-9\xc0-\xff_\-: ']+/i
DOUBLE_QUOTED_STRING: "\"" ("\\\""|/[^"]/)* "\"" "i"?
SINGLE_QUOTED_STRING: "'" ("\\'"|/[^']/)* "'" "i"?
ESCAPED_STRING: /`.*?`i?/
//KEYWORD: /[a-z]+/i

//UNQUOTED_NUMERIC_STRING: /[a-z_][a-z0-9_\-]*/i

REGEXP1.2: /\/.*?\/i?/
REGEXP2: /\\\\.*?\\\\i?/

RUNTIME_VAR: /%.*?%/

COMMENT: /\#[^\n]*/
CCOMMENT.3: /\/[*].*?[*]\//s

_END: "END"i

WS: /[ \t\f]+/
_NL: /[\r\n]+/

%ignore COMMENT
%ignore CCOMMENT
%ignore WS
%ignore _NL
