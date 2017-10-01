import logging
import json
import inspect
import pytest
from mappyfile.parser import Parser
from mappyfile.pprint import PrettyPrinter
from mappyfile.transformer import MapfileToDict


def output(s):
    """
    Parse, transform, and pretty print
    the result
    """
    p = Parser()
    m = MapfileToDict()

    # https://stackoverflow.com/questions/900392/getting-the-caller-function-name-inside-another-function-in-python
    logging.info(inspect.stack()[1][3])

    ast = p.parse(s)
    logging.debug(ast)
    d = m.transform(ast)
    logging.debug(json.dumps(d, indent=4))
    pp = PrettyPrinter(indent=0, newlinechar=" ", quote="'")
    s = pp.pprint(d)
    logging.debug(s)
    return s


def check_result(s):
    try:
        s2 = output(s)
        assert(s == s2)
    except AssertionError:
        logging.info(s)
        logging.info(s2)
        raise


def test_class_expression1():
    s = '''
    CLASS
      TEXT ([area])
    END
    '''
    exp = "CLASS TEXT ([area]) END"
    assert(output(s) == exp)


def test_class_expression2():
    """
    shp2img -m C:\Temp\msautotest\query\text.tmp.map  -l text_test002 -o c:\temp\tmp_onl0lk.png
    """
    s = '''
    CLASS
      TEXT ("[area]")
    END
    '''
    exp = 'CLASS TEXT ("[area]") END'
    assert(output(s) == exp)


def test_complex_class_expression():
    s = '''
    CLASS
      TEXT ("Area is: " + tostring([area],"%.2f"))
    END
    '''
    exp = '''CLASS TEXT ("Area is: " + (tostring([area],"%.2f"))) END'''
    assert(output(s) == exp)


def test_or_expressions():
    """
    See http://www.mapserver.org/mapfile/expressions.html#expressions
    """

    s = '''
    CLASS
        EXPRESSION ("[style_class]" = "10" OR "[style_class]" = "20")
    END
    '''

    exp = 'CLASS EXPRESSION ( ( "[style_class]" = "10" ) or ( "[style_class]" = "20" ) ) END'
    assert(output(s) == exp)

    s = '''
    CLASS
        EXPRESSION ("[style_class]" = "10" || "[style_class]" = "20")
    END
    '''

    exp = 'CLASS EXPRESSION ( ( "[style_class]" = "10" ) or ( "[style_class]" = "20" ) ) END'
    assert(output(s) == exp)


def test_and_expressions():
    s = '''
    CLASS
        EXPRESSION ("[style_class]" = "10" AND "[style_class]" = "20")
    END
    '''

    exp = 'CLASS EXPRESSION ( ( "[style_class]" = "10" ) and ( "[style_class]" = "20" ) ) END'
    assert(output(s) == exp)

    s = '''
    CLASS
        EXPRESSION ("[style_class]" = "10" && "[style_class]" = "20")
    END
    '''

    exp = 'CLASS EXPRESSION ( ( "[style_class]" = "10" ) and ( "[style_class]" = "20" ) ) END'
    assert(output(s) == exp)


def test_not_expressions():
    s = '''
    CLASS
        EXPRESSION NOT("[style_class]" = "20")
    END
    '''

    exp = 'CLASS EXPRESSION NOT ( "[style_class]" = "20" ) END'
    assert(output(s) == exp)

    s = '''
    CLASS
        EXPRESSION !("[style_class]" = "20")
    END
    '''

    exp = 'CLASS EXPRESSION NOT ( "[style_class]" = "20" ) END'
    assert(output(s) == exp)


def test_runtime_expression():
    s = """
    CLASS
      EXPRESSION ( [EPPL_Q100_] = %eppl% )
    END
    """
    exp = "CLASS EXPRESSION ( [EPPL_Q100_] = %eppl% ) END"
    # print(output(s))
    assert(output(s) == exp)


def test_ne_comparison():
    """
    IS NOT is not valid
    NE (Not Equals) should be used instead
    Uses Earley
    """
    s = """
    CLASS
        # EXPRESSION ( "[building]" IS NOT NULL) # incorrect syntax
        EXPRESSION ( "[building]" NE NULL)
    END
    """
    exp = 'CLASS EXPRESSION ( "[building]" NE NULL ) END'
    assert(output(s) == exp)


def test_eq_comparison():
    """
    Case is not changed for comparison (EQ/eq stay the same)
    Uses Earley
    """
    s = """
    CLASS
        EXPRESSION ( "[building]" eq NULL)
    END
    """
    exp = 'CLASS EXPRESSION ( "[building]" eq NULL ) END'
    # print(output(s))
    assert(output(s) == exp)


def test_expression():
    """
    Addressed in issue #27, now parses successfully.
    """
    s = """
    CLASS
        EXPRESSION ('[construct]' ~* /Br.*$/)
        STYLE
            ANGLE 360
        END
    END
    """
    exp = "CLASS EXPRESSION ( '[construct]' ~* /Br.*$/ ) STYLE ANGLE 360 END END"
    assert(output(s) == exp)


def test_list_expression():
    """
    See issue #27
    """
    s = """
    CLASS
        EXPRESSION /NS_Bahn|NS_BahnAuto/
    END
    """
    exp = "CLASS EXPRESSION /NS_Bahn|NS_BahnAuto/ END"
    assert(output(s) == exp)


@pytest.mark.xfail
def test_list_expression2():
    """
    See issue #38
    http://mapserver.org/mapfile/expressions.html#list-expressions
    These expressions are much more preformant in MapServer
    List expressions do not support quote escaping, or attribute values that contain a comma in them.

    To activate them enclose a comma separated list of values between {}, without adding quotes or extra spaces.
    """
    s = """
    CLASS
        EXPRESSION {2_Klass,Rte2etr}
    END
    """
    exp = "CLASS EXPRESSION {2_Klass,Rte2etr} END"
    assert(output(s) == exp)


def test_numerical_operator_ge_expression():
    s = """
    CLASS
        EXPRESSION ([power] ge 10000)
    END
    """
    exp = "CLASS EXPRESSION ( [power] ge 10000 ) END"
    assert(output(s) == exp)


def test_numerical_operator_gt_expression():
    s = """
    CLASS
        EXPRESSION ([power] gt 10000)
    END
    """
    exp = "CLASS EXPRESSION ( [power] gt 10000 ) END"
    assert(output(s) == exp)


def test_numerical_operator_le_expression():
    s = """
    CLASS
        EXPRESSION ([power] le 100)
    END
    """
    exp = "CLASS EXPRESSION ( [power] le 100 ) END"
    assert(output(s) == exp)


def test_numerical_operator_lt_expression():
    s = """
    CLASS
        EXPRESSION ([power] lt 100)
    END
    """
    exp = "CLASS EXPRESSION ( [power] lt 100 ) END"
    assert(output(s) == exp)


@pytest.mark.xfail
def test_divide_expression():
    s = """
    CLASS
        EXPRESSION ([field1] / [field2] > 0.1)
    END
    """
    exp = "CLASS EXPRESSION ( [field1] / [field2] > 0.1 ) END"
    assert(output(s) == exp)


@pytest.mark.xfail
def test_escaped_string():
    """
    http://mapserver.org/mapfile/expressions.html#quotes-escaping-in-strings
    Extra spaces currently added
    Starting with MapServer 6.0 you don't need to escape single quotes within double quoted strings
    and you don't need to escape double quotes within single quoted strings
    """
    s = """
    CLASS
        EXPRESSION "National \"hero\" statue"
    END
    """
    exp = "CLASS EXPRESSION 'National 'hero' statue' END"
    assert(output(s) == exp)


def run_tests():
    """
    Need to comment out the following line in C:\VirtualEnvs\mappyfile\Lib\site-packages\pep8.py
    #stdin_get_value = sys.stdin.read
    Or get AttributeError: '_ReplInput' object has no attribute 'read'
    """
    pytest.main(["tests/test_expressions.py"])


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # test_divide_expression()  # test_list_expression
    run_tests()
    print("Done!")
