import json
from tests import helper
from mappyfile.types import *

# point_vector.map

def print_dict_structure():
    """
    # http://stackoverflow.com/questions/3229419/pretty-printing-nested-dictionaries-in-python
    """
    d = helper.create_sample_map()
    print json.dumps(d, indent=4)

def test_add_layer():
    d = helper.create_sample_map()

    assert(len(d["layers"]) == 2)

    layer = Container()
    layer[MAPFILE_TYPE] = "layer"
    layer["name"] = QuotedString("Layer1.5")
    d["layers"].insert(1, layer)

    assert(len(d["layers"]) == 3)

def run_tests():
    import pytest
    
    #pytest.main(["tests/test_transformer.py::test_add_layer"])
    pytest.main(["tests/test_transformer.py"])


if __name__ == "__main__":
    print_dict_structure()
    run_tests()