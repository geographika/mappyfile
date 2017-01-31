import pytest
from mappyfile.pprint import PrettyPrinter
from tests.helper import create_sample_map, create_style1
from tests.point_vector import create_sample_map

def export_map():
    map_ = create_sample_map()

    pp = PrettyPrinter()
    print(pp.pprint(map_))

    # print a partial part of the map
    #print(pp.pprint(map_["layers"][0]["classes"][0]))
    #print(pp.pprint(map_["layers"][0]["classes"]))

def test_print_style():
    style1 = create_style1()
    pp = PrettyPrinter() # expected
    txt = pp.pprint(style1)
    expected = """STYLE
    COLOR 99 231 117
    WIDTH 1
END"""
    assert(txt == expected)

def test_print_map():
    expected = """MAP
    WEB
        METADATA
            'wms_enable_request' '*'
        END
    END
    PROJECTION
        'proj=utm'
        'ellps=GRS80'
        'datum=NAD83'
        'zone=15'
        'units=m'
        'north'
        'no_defs'
    END
    LAYER
        NAME 'Layer1'
        CLASS
            NAME 'Class1'
            STYLE
                COLOR 99 231 117
                WIDTH 1
            END
            STYLE
                NAME 'MyStyle'
                COLOR 108 201 187
                WIDTH 2
            END
        END
        FEATURE
            POINTS
                0 100
                100 200
                40 90
            END
        END
    END
    LAYER
        NAME 'Layer2'
        PROCESSING 'BANDS=1'
        PROCESSING 'CONTOUR_ITEM=elevation'
        PROCESSING 'CONTOUR_INTERVAL=20'
    END
END"""

    mf = create_sample_map()
    pp = PrettyPrinter() # expected
    txt = pp.pprint(mf)
    assert(expected == txt)

def run_tests():        
    #pytest.main(["tests/test_pprint.py::test_print_map"])
    pytest.main(["tests/test_pprint.py"])

if __name__ == "__main__":
    export_map()
    run_tests()

