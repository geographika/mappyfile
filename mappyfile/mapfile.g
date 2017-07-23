start: (_NL* composite _NL*)+

composite: composite_type attr? _NL* composite_body _END
       | composite_type points _END
       | composite_type pattern _END
       | composite_type attr _END
	   | metadata
	   | validation

composite_body: _composite_item*
_composite_item: (composite|attr|points|projection|pattern|values) _NL+

points: "POINTS"i _NL* (_num_pair _NL*)* _END
pattern: "PATTERN"i _NL* (_num_pair _NL*)* _END

projection: "PROJECTION"i _NL* ((string _NL*)+|AUTO _NL+) _END
values: "VALUES"i _NL* ((string_pair) _NL+)+ _END

metadata: "METADATA"i _NL* ((string_pair|attr) _NL+)+ _END
validation: "VALIDATION"i _NL* ((string_pair|attr) _NL+)+ _END

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

_num_pair: (int|float) _NL* (int|float)

attr_bind: "[" bare_string "]"

not_expression: ("!"|"NOT"i) expression
expression: "(" or_test ")"
?or_test : (or_test ("OR"i|"||"))? and_test
?and_test : (and_test ("AND"i|"&&"))? comparison
?comparison: (comparison compare_op)? add
!compare_op: ">=" | "<" | "=*" | "==" | "=" | "~" | "~*" | ">" | "<=" | "IN" | "NE" | "EQ"

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
REGEXP1: /\/.*?\/i?/
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