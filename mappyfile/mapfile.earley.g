start: composite+

composite: composite_type attr? composite_body _END
       | metadata
       | validation

composite_body: _composite_item*
_composite_item: (composite|attr|points|projection|pattern|values)

points: "POINTS"i _num_pair* _END
pattern: "PATTERN"i _num_pair* _END

projection: "PROJECTION"i (string+|AUTO) _END
values: "VALUES"i string_pair+ _END

metadata: "METADATA"i (string_pair|attr)+ _END
validation: "VALIDATION"i (string_pair|attr)+ _END

attr: attr_name value+

attr_name: NAME | composite_type
?value: bare_string | string | int | float | expression | not_expression | attr_bind | path | regexp | runtime_var | list

int: SIGNED_INT
int_pair: int int
!bare_string: NAME | "SYMBOL"i | "AUTO"i | "GRID"i | "CLASS"i | "FEATURE"i
string: STRING1 | STRING2 | STRING3
string_pair: string string
float: SIGNED_FLOAT
float_pair: float float
path: PATH
regexp: REGEXP1 | REGEXP2
runtime_var: RUNTIME_VAR
list: "{" value ("," value)* "}"

_num_pair: (int|float) (int|float)

attr_bind: "[" bare_string "]"

not_expression: ("!"|"NOT"i) expression
expression: "(" or_test ")"
?or_test : (or_test ("OR"i|"||"))? and_test
?and_test : (and_test ("AND"i|"&&"))? comparison
?comparison: (comparison compare_op)? add
!compare_op: ">=" | "<" | "=*" | "==" | "=" | "!=" | "~" | "~*" | ">" | "<=" | "IN" | "NE" | "EQ" | "LE" | "LT" | "GE" | "GT"

?add: (add "+")? (func_call | value)
func_call: attr_name "(" func_params ")"
func_params: value ("," value)*

!composite_type: "CLASS"i
            | "CLUSTER"i
            | "COMPOSITE"i
            | "CONFIG"i
            | "FEATURE"i
            | "FONTSET"i
            | "GRID"i
            | "INCLUDE"i
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
            | "SYMBOL"i
            | "WEB"i

AUTO: "AUTO"i
PATH: /[a-z_]*[.\/][a-z0-9_\/.]+/i
NAME: /[a-z_][a-z0-9_]*/i

SIGNED_FLOAT: ["-"|"+"] FLOAT
SIGNED_INT: ["-"|"+"] INT

%import common.FLOAT
%import common.INT

STRING1: /".*?(?<!\\\\)(\\\\\\\\)*?"i?/
STRING2: /'.*?(?<!\\\\)(\\\\\\\\)*?'i?/
STRING3: /`.*?`i?/   // XXX TODO
REGEXP1.2: /\/.*?\/i?/
REGEXP2: /\\\\.*?\\\\i?/
RUNTIME_VAR: /%.*?%/

COMMENT: /\#[^\n]*/
CCOMMENT: /\/(?s)[*].*?[*]\//

_END: "END"i

WS: /[ \t\f]+/
_NL: /[\r\n]+/

%ignore COMMENT
%ignore CCOMMENT
%ignore WS
%ignore _NL
