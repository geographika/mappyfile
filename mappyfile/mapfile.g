start: NL* composite NL*;

composite: composite_type attr? NL+ composite_body END
       | composite_type points END
       | composite_type attr END
       ;
composite_body: composite_item* ;
@composite_item: (composite|attr|points|projection|metadata|pattern|validation|values) NL+;

points: POINTS NL+ (num_pair NL*)* END
      | POINTS num_pair* END
      ;
pattern: PATTERN int_pair* END;

projection: PROJECTION NL+ ((string NL*)+|AUTO NL+) END;
metadata: METADATA NL+ ((string_pair|attr) NL+)+ END;
values: VALUES NL+ ((string_pair) NL+)+ END;
validation: VALIDATION NL+ ((attr NL+)+|(string NL*)+) END;


attr: attr_name value+;

attr_name: NAME | composite_type;
@value: bare_string | string | int | float | expression | attr_bind | path | regexp | runtime_var | list;

int: INT;
int_pair: int int;
bare_string: NAME | SYMBOL | AUTO | GRID | CLASS;
string: STRING1 | STRING2 | STRING3 ;
string_pair: string string;
float: FLOAT;
float_pair: float float;
path: PATH;
regexp: REGEXP;
runtime_var: RUNTIME_VAR;
list: '{' value (',' value)* '}';

@num_pair: (int|float) (int|float);

attr_bind: '\[' bare_string '\]';

@expression: '\(' or_test '\)';
?or_test : (or_test OR)? and_test;
?and_test : (and_test AND)? comparison;
?comparison: (comparison compare_op)? add;
compare_op: '>=' | '<' | '=[*]' | '==' | '=' | '~' | '~[*]' | '>' | '<=' | IN;

?add: (add '\+')? (func_call | value);
func_call: attr_name '\(' func_params '\)';
func_params: value (',' value)*;

composite_type: CLASS
            | CLUSTER
            | COMPOSITE
            | CONFIG
            | FEATURE
            | FONTSET
            | GRID
            | INCLUDE
            | JOIN
            | LABEL
            | LAYER
            | LEADER
            | LEGEND
            | MAP
            | OUTPUTFORMAT
            | QUERYMAP
            | REFERENCE
            | SCALEBAR
            | SCALETOKEN
            | STYLE
            | SYMBOL
            | WEB
            ;

%fragment I: '(?i)';    // Case Insensitive
%fragment S: '(?s)';    // Dot Matches Newline

NAME: I '[a-z_][a-z0-9_]*(?=([\s(]|\]))' (%unless
    END: I 'END';
    AND: I 'AND';
    OR: I 'OR';
    AUTO: I 'AUTO';
    IN: I 'IN';

    // Valid composites
    CLASS: I 'CLASS';
    CLUSTER: I 'CLUSTER';
    COMPOSITE: I 'COMPOSITE';
    CONFIG: I 'CONFIG';
    FEATURE: I 'FEATURE';
    FONTSET: I 'FONTSET';
    GRID: I 'GRID';
    INCLUDE: I 'INCLUDE';
    JOIN: I 'JOIN';
    LABEL: I 'LABEL';
    LAYER: I 'LAYER';
    LEADER: I 'LEADER';
    LEGEND: I 'LEGEND';
    MAP: I 'MAP';
    OUTPUTFORMAT: I 'OUTPUTFORMAT';
    QUERYMAP: I 'QUERYMAP';
    REFERENCE: I 'REFERENCE';
    SCALEBAR: I 'SCALEBAR';
    SCALETOKEN: I 'SCALETOKEN';
    STYLE: I 'STYLE';
    SYMBOL: I 'SYMBOL';
    VALUES: I 'VALUES';
    WEB: I 'WEB';

    // Special composites
    POINTS: I 'POINTS';
    PATTERN: I 'PATTERN';
    PROJECTION: I 'PROJECTION';
    METADATA: I 'METADATA';
    VALIDATION: I 'VALIDATION';
 ); // Match names and paths

%fragment EXP_POSTFIX: I 'e[-+]?\d+';

PATH: I '[a-z_]*[./][a-z0-9_/.]+' ;

INT: I '-?\d+';
FLOAT: '-?(\d+\.\d*|\.\d+)(' EXP_POSTFIX ')?'
       '|\d+' EXP_POSTFIX;

%fragment STRING_INTERNAL: '.*?(?<!\\)(\\\\)*?' ;

STRING1: '"' STRING_INTERNAL '"' ;
STRING2: '\'' STRING_INTERNAL '\'' ;
STRING3: '`.*?`' ;  // XXX TODO
REGEXP: '/.*?/' ;
RUNTIME_VAR: '%.*?%' ;

COMMENT: '\#[^\n]*'(%ignore);
CCOMMENT: S '/[*].*?[*]/' (%ignore) (%newline);

WS: '[ \t\f]+' (%ignore);
NL: '[\r\n]+' (%newline);
