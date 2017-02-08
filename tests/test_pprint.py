import pytest
from mappyfile.pprint import PrettyPrinter
import mappyfile

def test_format_list():

    s = """
        CLASS
            STYLE
                COLOR 173 216 230
            END
            STYLE
                OUTLINECOLOR 2 2 2
                WIDTH 1
                LINECAP BUTT
                PATTERN
                    5 5
                    10 10
                END
            END
        END
    """

    ast = mappyfile.loads(s)
    #print ast

    pp = PrettyPrinter(indent=0) # expected

    k = "pattern"
    lst = [[5, 5, 10, 10]]

    assert(pp.is_paired_list(k))
    r = pp.process_list(k, lst, 0)
    exp = [u'PATTERN', '5 5\n10 10', u'END']
    assert(r == exp)

def run_tests():        
    pytest.main(["tests/test_pprint.py::test_format_list"])
    #pytest.main(["tests/test_pprint.py"])

if __name__ == "__main__":
    #run_tests()
    test_format_list()
