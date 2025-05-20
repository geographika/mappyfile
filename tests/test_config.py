import pytest
from lark import UnexpectedCharacters, UnexpectedToken, Tree
from mappyfile.parser import Parser


def test_parser_validation():
    p = Parser()

    config_text_ok = """CONFIG
    ENV
            MS_MAP_PATTERN "."
            PROJ_LIB "C:/MapServer/bin/proj7/SHARE"
    END
    END
    """
    tree: Tree = p.parse(config_text_ok)
    assert tree.data == "config"
    assert tree.children[0].data == "env"

    # Test bad punctuation
    config_text_bad1 = """CONFIG
    ENV
            MS_MAP_PATTERN "."
            PROJ_LIB" "C:/MapServer/bin/proj7/SHARE"
    END
    END
    """
    with pytest.raises(UnexpectedCharacters) as e:
        p.parse(config_text_bad1)
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
        p.parse(config_text_bad2)
