import pytest
from lark import UnexpectedCharacters, UnexpectedToken, Tree
from mappyfile.parser import Parser
from mappyfile.transformer import ConfigfileTransformer, MapfileToDict
from mappyfile.pprint import PrettyPrinter


def test_parser_validation():
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
    p = Parser()
    tree: Tree = p.parse(config_text_ok)
    assert tree.data == "config"
    assert tree.children[0].data == "env"


def test_invalid_config_parser():
    # Test bad punctuation

    config_text_bad1 = """CONFIG
    ENV
            MS_MAP_PATTERN "."
            PROJ_LIB" "C:/MapServer/bin/proj7/SHARE"
    END
    END
    """

    p = Parser()
    with pytest.raises(UnexpectedCharacters) as e:
        p.parse(config_text_bad1)
    assert e.value.line == 4


def test_invalid_config2_parser():
    # Test mapfile composites inside the config
    p = Parser()
    config_text_bad2 = """CONFIG
    ENV
            METADATA
            "ows_title" "layer_0"
            END
    END
    END
    """
    with pytest.raises(UnexpectedToken):
        p.parse(config_text_bad2)


def test_config():
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
    p = Parser()
    tree: Tree = p.parse(config_text_ok)

    m = MapfileToDict(
        include_position=False,
        include_comments=False,
        transformer_class=ConfigfileTransformer,
    )
    d = m.transform(tree)

    # import json
    # print(json.dumps(d))
    pp = PrettyPrinter(indent=0, newlinechar=" ", quote="'")
    s = pp.pprint(d)
    assert (
        s
        == "CONFIG ENV ms_map_pattern '.' proj_lib 'C:/MapServer/bin/proj7/SHARE' END MAPS test1 'C:/Maps/test1.map' test2 'C:/Maps/test2.map' END END"
    )


def test_config_with_comments():
    """
    TODO fix block-level comments
    """
    config_text_ok = """CONFIG
    # block comment
    ENV
            MS_MAP_PATTERN "."
            PROJ_LIB "C:/MapServer/bin/proj7/SHARE"
    END
    MAPS
            # this is a test map
            test1 "C:/Maps/test1.map"
            # another test map
            test2 "C:/Maps/test2.map"
    END
    END
    """
    p = Parser(include_comments=True)
    tree: Tree = p.parse(config_text_ok)

    m = MapfileToDict(
        include_position=True,
        include_comments=True,
        transformer_class=ConfigfileTransformer,
    )
    d = m.transform(tree)

    # import json
    # print(json.dumps(d))
    pp = PrettyPrinter(indent=0, newlinechar="\n", quote="'")
    s = pp.pprint(d)
    assert (
        s
        == """CONFIG
ENV
ms_map_pattern '.' # block comment
proj_lib 'C:/MapServer/bin/proj7/SHARE'
END
MAPS
test1 'C:/Maps/test1.map' # this is a test map
test2 'C:/Maps/test2.map' # another test map
END
END"""
    )


def test_config_with_quoted_keys():
    config_text_ok = """CONFIG
    ENV
            MS_MAP_PATTERN "."
            "PROJ_LIB" "C:/MapServer/bin/proj7/SHARE"
    END
    MAPS
            test1 "C:/Maps/test1.map"
            'test2' "C:/Maps/test2.map"
    END
    END
    """
    p = Parser()
    tree: Tree = p.parse(config_text_ok)

    m = MapfileToDict(
        include_position=False,
        include_comments=False,
        transformer_class=ConfigfileTransformer,
    )
    d = m.transform(tree)

    d["env"]["curl_ca_bundle"] = "C:/MapServer/bin/curl-ca-bundle.crt"
    # import json
    # print(json.dumps(d))
    pp = PrettyPrinter(indent=0, newlinechar=" ", quote="'")
    s = pp.pprint(d)
    assert (
        s
        == """CONFIG ENV ms_map_pattern '.' "proj_lib" 'C:/MapServer/bin/proj7/SHARE' curl_ca_bundle """
        """'C:/MapServer/bin/curl-ca-bundle.crt' END MAPS test1 'C:/Maps/test1.map' 'test2' 'C:/Maps/test2.map' END END"""
    )


def run_tests():
    pytest.main(["tests/test_config.py"])


if __name__ == "__main__":
    # logging.basicConfig(level=logging.DEBUG)
    # run_tests()
    test_parser_validation()
    test_config()
    test_config_with_comments()
    test_config_with_quoted_keys()
    print("Done!")
