import pytest
from lark import UnexpectedCharacters, UnexpectedToken, Tree
from mappyfile.parser import Parser
from mappyfile.transformer import ConfigfileTransformer, MapfileToDict
from mappyfile.pprint import PrettyPrinter

def test_parser_validation():
    p = Parser()

    config_text_ok = """CONFIG
    ENV
            MS_MAP_PATTERN "."
            PROJ_LIB "C:/MapServer/bin/proj7/SHARE"
    END
    MAPS
            test1 "C:/Maps/test1.map"
            test2 "C:/Maps/test2.map"
    END    
    END
    """
    tree: Tree = p.parse(config_text_ok)
    assert tree.data == "config"
    assert tree.children[0].data == "env"

    m = MapfileToDict(
        include_position=True, include_comments=True, transformer_class=ConfigfileTransformer
    )
    d = m.transform(tree)

    pp = PrettyPrinter(indent=0, newlinechar=" ", quote="'")
    # pp = PrettyPrinter()
    s = pp.pprint(d)
    print(s)    
        
    # Test bad punctuation
    config_text_bad1 = """CONFIG
    ENV
            MS_MAP_PATTERN "."
            PROJ_LIB" "C:/MapServer/bin/proj7/SHARE"
    END
    END
    """
    with pytest.raises(UnexpectedCharacters) as e:
        res = p.parse(config_text_bad1)
    assert e.value.line == 4

    # Test mapfile composites inside the config
    config_text_bad2 = """CONFIG
    ENV
            METADATA
            "ows_title" "layer_0"
            END
    END
    END
    """
    with pytest.raises(UnexpectedToken) as e:
        res = p.parse(config_text_bad2)

def run_tests():
    pytest.main(["tests/test_config.py"])


if __name__ == "__main__":
    # logging.basicConfig(level=logging.DEBUG)
    run_tests()
    print("Done!")
