start: "SYMBOLSET"i composite_body _END   -> symbolset
     | composite+

composite: composite_type composite_body _END
       | metadata
       | validation

composite_body: _composite_item*
_composite_item: (composite|attr|points|projection|pattern|values|config)

!projection: "PROJECTION"i (string*|AUTO) _END
!config: "CONFIG"i (string | UNQUOTED_STRING) (string | UNQUOTED_STRING)

!points: "POINTS"i num_pair* _END
!pattern: "PATTERN"i num_pair* _END

!values: "VALUES"i string_pair* _END
!metadata: "METADATA"i string_pair* _END
!validation: "VALIDATION"i string_pair* _END

attr: (UNQUOTED_STRING | composite_type) (value | UNQUOTED_STRING)
//attr: (UNQUOTED_STRING | SYMBOL) (value | UNQUOTED_STRING)
// SYMBOL is listed in composite_type but is also an attribute name

?value: string | int | float | expression | not_expression | attr_bind | path
| regexp | runtime_var | list | NULL | true | false | extent | rgb | hexcolor
| colorrange | hexcolorrange | num_pair | attr_bind_pair | _attr_keyword

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
float: SIGNED_FLOAT
float_pair: float float
path: PATH
regexp: REGEXP1 | REGEXP2
runtime_var: RUNTIME_VAR
list: "{" (value | UNQUOTED_STRING) ("," (value | UNQUOTED_STRING))* "}"

num_pair: (int|float) (int|float)

attr_bind: "[" UNQUOTED_STRING "]"

not_expression: ("!"|"NOT"i) expression
expression: "(" or_test ")"
?or_test : (or_test ("OR"i|"||"))? and_test
?and_test : (and_test ("AND"i|"&&"))? comparison
?comparison: (comparison compare_op)? sum
!compare_op: ">=" | "<" | "=*" | "==" | "=" | "!=" | "~" | "~*" | ">" | "%"
| "<=" | "IN"i | "NE"i | "EQ"i | "LE"i | "LT"i | "GE"i | "GT"i | "LIKE"i

?sum: product
    | sum "+" product -> add
    | sum "-" product -> sub

?product: atom
    | product "*" atom -> mul
    | product "/" atom -> div
    | product "^" atom -> power

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
UNQUOTED_STRING: /[a-z0-9_\-:]+/i
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
