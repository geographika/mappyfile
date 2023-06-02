import os
from lark import Lark

from lark.tree import pydot__tree_to_png

GVIZ_PATH = r"C:\Program Files (x86)\Graphviz2.38\bin"


def graphviz_setup():
    os.environ["PATH"] = GVIZ_PATH + ";" + os.environ["PATH"]


def main(s, out_fn):
    graphviz_setup()
    project_root = os.path.normpath(os.path.join(os.path.dirname(__file__), "../../"))
    fld = os.path.normpath(project_root + "./mappyfile")
    gf = os.path.join(fld, "mapfile.lark")
    grammar_text = open(gf).read()

    g = Lark(grammar_text, parser="lalr", lexer="contextual")
    t = g.parse(s)
    print(t)
    pydot__tree_to_png(t, os.path.join(project_root, "docs/images", out_fn))
    print(t.pretty())


s = "MAP NAME 'Test' END"
# main(s, "tree.png")
main(s, "tree_no_terminals.png")  # remove ! from !composite_type rule
print("Done!")
