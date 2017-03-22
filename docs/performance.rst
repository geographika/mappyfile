ncalls
    for the number of calls,
tottime
    for the total time spent in the given function (and excluding time made in calls to sub-functions),
percall
    is the quotient of tottime divided by ncalls
cumtime
    is the total time spent in this and all subfunctions (from invocation till exit). This figure is accurate even for recursive functions.
percall
    is the quotient of cumtime divided by primitive calls


With saving:

         29362467 function calls (28402404 primitive calls) in 25.749 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
  1203653    5.221    0.000    5.782    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\plyplus\pearley.py:16(__init__)
  1203653    4.313    0.000   13.905    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\plyplus\pearley.py:46(process)
  1173487    1.939    0.000    2.054    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\plyplus\pearley.py:84(epsilon_closure)
5396271/5396270    1.019    0.000    1.026    0.000 {isinstance}
433851/66    0.822    0.000    2.814    0.043 C:\VirtualEnvs\mappyfile\lib\site-packages\plyplus\strees.py:323(_visit)
  3699185    0.794    0.000    1.636    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\plyplus\pearley.py:40(consume_nonterminal)
  2202385    0.620    0.000    0.837    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\plyplus\strees.py:296(is_stree)
      136    0.588    0.004    0.588    0.004 {method 'close' of 'file' objects}
    29858    0.565    0.000   14.470    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\plyplus\pearley.py:113(advance_to)
        1    0.547    0.547    0.547    0.547 {pyodbc.connect}
  1051897    0.496    0.000    0.496    0.000 {getattr}
 25816/32    0.492    0.000    2.371    0.074 C:\VirtualEnvs\mappyfile\lib\site-packages\mappyfile\pprint.py:215(_format)
   286836    0.383    0.000    0.657    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\plyplus\plyplus.py:230(_flatten)
  1202465    0.382    0.000    0.477    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\plyplus\pearley.py:33(consume_terminal)
        1    0.363    0.363    0.363    0.363 {method 'execute' of 'pyodbc.Cursor' objects}
       33    0.340    0.010   15.282    0.463 C:\VirtualEnvs\mappyfile\lib\site-packages\plyplus\pearley.py:117(feed)
   151240    0.297    0.000    0.938    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\plyplus\pearley.py:30(next_state)
   426555    0.288    0.000    0.288    0.000 {method 'match' of '_sre.SRE_Pattern' objects}
417978/66    0.280    0.000    2.814    0.043 C:\VirtualEnvs\mappyfile\lib\site-packages\plyplus\plyplus.py:224(_visit)
    81535    0.278    0.000    0.502    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\plyplus\engine_pearley.py:38(_handle_rule)
   269252    0.232    0.000    0.443    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\mappyfile\pprint.py:129(format_value)
   106576    0.215    0.000    0.215    0.000 {method 'format' of 'unicode' objects}
    71735    0.199    0.000    0.531    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\ply\lex.py:305(token)
  1954798    0.198    0.000    0.198    0.000 {method 'append' of 'list' objects}
 39605/66    0.158    0.000    0.507    0.008 C:\VirtualEnvs\mappyfile\lib\site-packages\plyplus\strees.py:342(_transform)
   125829    0.158    0.000    0.515    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\plyplus\plyplus.py:238(rule)
       33    0.151    0.005    0.459    0.014 C:\VirtualEnvs\mappyfile\lib\site-packages\ply\yacc.py:1001(parseopt_notrack)
10498/5480    0.145    0.000    0.396    0.000 C:\VirtualEnvs\mappyfile\lib\sre_parse.py:395(_parse)

Creating a single parser/transformer for all EAs


         15330143 function calls (15194176 primitive calls) in 14.956 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
   639550    2.745    0.000    3.047    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\plyplus\pearley.py:16(__init__)
   639550    2.330    0.000    7.396    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\plyplus\pearley.py:46(process)
   622700    1.027    0.000    1.089    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\plyplus\pearley.py:84(epsilon_closure)
      137    0.593    0.004    0.593    0.004 {method 'close' of 'file' objects}
        1    0.552    0.552    0.552    0.552 {pyodbc.connect}
2713996/2713995    0.526    0.000    0.533    0.000 {isinstance}
 25816/32    0.499    0.000    2.399    0.075 C:\VirtualEnvs\mappyfile\lib\site-packages\mappyfile\pprint.py:215(_format)
  2023537    0.447    0.000    0.990    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\plyplus\pearley.py:40(consume_nonterminal)
        1    0.316    0.316    0.316    0.316 {method 'execute' of 'pyodbc.Cursor' objects}
    16731    0.283    0.000    7.678    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\plyplus\pearley.py:113(advance_to)
   382784    0.266    0.000    0.266    0.000 {method 'match' of '_sre.SRE_Pattern' objects}
   269252    0.237    0.000    0.453    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\mappyfile\pprint.py:129(format_value)
   106576    0.215    0.000    0.215    0.000 {method 'format' of 'unicode' objects}
   639481    0.208    0.000    0.261    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\plyplus\pearley.py:33(consume_terminal)
        1    0.189    0.189    8.132    8.132 C:\VirtualEnvs\mappyfile\lib\site-packages\plyplus\pearley.py:117(feed)
       35    0.157    0.004    0.738    0.021 C:\VirtualEnvs\mappyfile\lib\site-packages\ply\yacc.py:1001(parseopt_notrack)
    44855    0.154    0.000    0.271    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\plyplus\engine_pearley.py:38(_handle_rule)
        1    0.148    0.148   14.955   14.955 C:\build\build_map2.py:326(run)
    51365    0.143    0.000    0.462    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\ply\lex.py:305(token)
   451354    0.130    0.000    0.168    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\plyplus\strees.py:296(is_stree)
    83696    0.126    0.000    0.596    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\plyplus\pearley.py:30(next_state)
      104    0.123    0.001    0.279    0.003 C:\Python27\Lib\ConfigParser.py:464(_read)

Using Lark:

         30552164 function calls (30474395 primitive calls) in 24.866 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
  1197450    3.687    0.000    6.412    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\lark\parsers\earley.py:35(__init__)
  1271377    2.532    0.000    2.532    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\lark\tree.py:6(__init__)
   158255    2.219    0.000    5.187    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\lark\parsers\earley.py:91(add)
    45162    1.542    0.000    7.798    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\lark\parsers\earley.py:144(predict)
  2393212    1.140    0.000    1.528    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\lark\parsers\earley.py:56(__hash__)
    30038    0.846    0.000   16.572    0.001 C:\VirtualEnvs\mappyfile\lib\site-packages\lark\parsers\earley.py:152(process_column)
  1197450    0.773    0.000    3.082    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\lark\parsers\earley.py:28(__init__)
      136    0.689    0.005    0.689    0.005 {method 'close' of 'file' objects}
 32376/32    0.684    0.000    4.077    0.127 C:\VirtualEnvs\mappyfile\lib\site-packages\mappyfile\pprint.py:234(_format)
  3164403    0.679    0.000    0.679    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\lark\parsers\earley.py:41(expect)
        1    0.590    0.590    0.590    0.590 {pyodbc.connect}
   152617    0.574    0.000    1.104    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\lark\parsers\earley.py:49(advance)
    82978    0.561    0.000    1.777    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\lark\parsers\earley.py:148(complete)
2480201/2480200    0.476    0.000    0.482    0.000 {isinstance}
  1197450    0.424    0.000    0.503    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\lark\parsers\earley.py:45(is_complete)
        1    0.361    0.361    0.361    0.361 {method 'execute' of 'pyodbc.Cursor' objects}
  1121918    0.358    0.000    1.039    0.000 {method 'add' of 'set' objects}
   390132    0.330    0.000    1.159    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\mappyfile\pprint.py:128(format_value)
   152560    0.312    0.000    0.312    0.000 {method 'format' of 'unicode' objects}
   283204    0.308    0.000    0.470    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\mappyfile\pprint.py:156(escape_quotes)
   836381    0.230    0.000    0.230    0.000 {method 'startswith' of 'unicode' objects}
   101189    0.215    0.000    0.215    0.000 {method 'match' of '_sre.SRE_Pattern' objects}
2405543/2405447    0.209    0.000    0.209    0.000 {hash}
   283204    0.201    0.000    0.758    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\mappyfile\pprint.py:168(standardise_quotes)
   158224    0.200    0.000    0.876    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\mappyfile\pprint.py:181(format_key)
  2393212    0.180    0.000    0.180    0.000 {id}
   731520    0.172    0.000    0.172    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\lark\common.py:111(match)
    31261    0.168    0.000    0.448    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\lark\lexer.py:146(lex)
   152368    0.162    0.000    2.030    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\mappyfile\pprint.py:196(format_line)
   298661    0.159    0.000    0.180    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\lark\parsers\earley.py:72(get_news)
  1467680    0.157    0.000    0.157    0.000 {method 'append' of 'list' objects}
    38832    0.152    0.000    0.270    0.000 C:\Python27\Lib\collections.py:125(items)
    38097    0.149    0.000    0.354    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\lark\parse_tree_builder.py:31(_build_ast)
        1    0.149    0.149   24.864   24.864 C:\Users\SG\Documents\Dropbox\Projects\LgcsbPms\PmsMapServer\pmsmapserver\build\build_map2.py:326(run)
    33996    0.134    0.000    0.134    0.000 {method 'union' of 'frozenset' objects}
   139596    0.132    0.000    0.174    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\lark\tree.py:64(iter_subtrees)
    30071    0.128    0.000    0.206    0.000 C:\VirtualEnvs\mappyfile\lib\site-packages\lark\parsers\earley.py:81(__init__)
      104    0.122    0.001    0.281    0.003 C:\Python27\Lib\ConfigParser.py:464(_read)

Using mapscript:

         1588964 function calls (1588944 primitive calls) in 4.107 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
       32    0.584    0.018    0.584    0.018 {_mapscript.new_mapObj}
        1    0.547    0.547    0.547    0.547 {pyodbc.connect}
      424    0.448    0.001    1.022    0.002 C:\Python27\Lib\ConfigParser.py:464(_read)
        1    0.370    0.370    0.370    0.370 {imp.load_module}
       32    0.331    0.010    0.331    0.010 {_mapscript.mapObj_save}
        1    0.311    0.311    0.311    0.311 {method 'execute' of 'pyodbc.Cursor' objects}
       32    0.242    0.008    0.242    0.008 {_mapscript.mapObj_setConfigOption}
   156620    0.157    0.000    0.157    0.000 C:\Python27\Lib\collections.py:71(__setitem__)
        1    0.141    0.141    4.107    4.107 C:\LgcsbPms\PmsMapServer\pmsmapserver\build\build_map.py:296(run)
   151736    0.113    0.000    0.113    0.000 {method 'match' of '_sre.SRE_Pattern' objects}
        1    0.083    0.083    0.083    0.083 {method 'fetchall' of 'pyodbc.Cursor' objects}
        1    0.071    0.071    1.014    1.014 .\pmsmapserver\build\engineering_areas.py:64(create_classes)
    97205    0.067    0.000    0.067    0.000 {method 'readline' of 'file' objects}
    80415    0.037    0.000    0.037    0.000 {method 'split' of 'str' objects}
     6156    0.032    0.000    0.052    0.000 C:\Python27\Lib\collections.py:50(__init__)
        1    0.030    0.030    0.418    0.418 .\mappyscript\common.py:35(setup)
      821    0.028    0.000    0.028    0.000 {nt.stat}
     5732    0.027    0.000    0.039    0.000 C:\Python27\Lib\collections.py:125(items)
    88463    0.026    0.000    0.026    0.000 {method 'group' of '_sre.SRE_Match' objects}
   152510    0.022    0.000    0.022    0.000 {method 'lower' of 'str' objects}
      445    0.022    0.000    0.022    0.000 {open}
   169783    0.021    0.000    0.021    0.000 {method 'str


