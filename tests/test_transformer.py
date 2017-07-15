import pytest
from mappyfile.parser import Parser
from mappyfile.transformer import MapfileToDict

def test_processing_directive():

    s = """
    LAYER
        NAME 'ProcessingLayer'
        PROCESSING 'BANDS=1'
        PROCESSING 'CONTOUR_ITEM=elevation'
        PROCESSING 'CONTOUR_INTERVAL=20'
    END
    """

    p = Parser()
    ast = p.parse(s)
    t = MapfileToDict()
    d = t.transform(ast)
    assert(len(d["processing"]) == 3)

def test_config_directive():

    s = """
    MAP
        NAME 'ConfigMap'
        CONFIG MS_ERRORFILE "stderr"
        CONFIG "PROJ_DEBUG" "OFF"
        CONFIG "ON_MISSING_DATA" "IGNORE"
    END
    """

    p = Parser()
    ast = p.parse(s)
    t = MapfileToDict()
    d = t.transform(ast)
    assert(len(d["config"]) == 3)

def test_metadata():

    s = """
    MAP
        METADATA
            'wms_enable_request'  '*'     
        END
    END
    """

    p = Parser()
    ast = p.parse(s)
    t = MapfileToDict()
    d = t.transform(ast)
    #print(dict(d["metadata"]))
    assert(d["metadata"]["'wms_enable_request'"] == "'*'")

def run_tests():        
    #pytest.main(["tests/test_transformer.py::test_config_directive"])
    pytest.main(["tests/test_transformer.py"])

if __name__ == '__main__':
    #run_tests()
    test_metadata()
    print("Done!")