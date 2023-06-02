from mappyfile.parser import Parser
import os

GVIZ_PATH = r"C:\Program Files (x86)\Graphviz2.38\bin"


def graphviz_setup():
    os.environ["PATH"] = GVIZ_PATH + ";" + os.environ["PATH"]


def create_layer_diagram():
    s = """
      CLASS
        text "country name"
        NAME "test1"
        STYLE
            COLOR 180 180 180
        END
      END
    """

    p = Parser()
    ast = p.parse(s)

    of = "./docs/images/class_parsed.png"

    ast.to_png_with_pydot(of)


if __name__ == "__main__":
    create_layer_diagram()
    print("Done!")
