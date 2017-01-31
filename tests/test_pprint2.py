import pytest
from mappyfile.pprint import PrettyPrinter
from tests.point_vector import create_map
import os
import subprocess
import tempfile, shutil

from mappyfile.types import Container, MAPFILE_TYPE

from subprocess import call
#call(["ls", "-l"])

def export_map():
    map_ = create_map()
    
    print map_
    map_["layers"][0]["features"][0]["points"].append('100 100')
    print map_["layers"][0]["features"][0]["points"]

    map_["extent"] = "0 0 100 100" #[0, 0, 100, 100]

    # search
    # next((item for item in dicts if item["name"] == "Pam"), False)
    # http://stackoverflow.com/questions/8653516/python-list-of-dictionaries-search

    new_feature = Container()
    new_feature[MAPFILE_TYPE] = "feature"
    new_points = ["150 150"]
    new_feature["points"] = new_points

    map_["layers"][0]["features"].insert(0, new_feature)
    pp = PrettyPrinter()

    f = tempfile.NamedTemporaryFile(delete=False, suffix=".map")
    f.write(pp.pprint(map_))
    f.close()


    of = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    of.close()

    print f.name

    shutil.copy("./tests/symbolset", tempfile.gettempdir())

    params = ["shp2img","-m",f.name,"-i","png","-o", of.name]

    dll_location = r"C:\MapServer\bin"
    os.environ['PATH'] = dll_location + ';' + os.environ['PATH']
    print " ".join(params)
    # [SHP2IMG] -m [MAPFILE] -i png -o [RESULT]

    #call(params)
    p = subprocess.Popen(params)
    print p.__dict__
    print p.stdout

    #if p.returncode == 0:
    os.startfile(of.name)


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
    #run_tests()

