import os
from lark import Lark

from lark.tree import pydot__tree_to_png

GVIZ_PATH = r"C:\Program Files (x86)\Graphviz2.38\bin"

def graphviz_setup():
    os.environ['PATH'] = GVIZ_PATH + ';' + os.environ['PATH']


graphviz_setup()

fld = os.path.normpath(os.path.join(os.path.dirname(__file__), "../.././mappyfile"))
gf = os.path.join(fld, "mapfile.g")
grammar_text = open(gf).read()

g = Lark(grammar_text, parser='earley', lexer='standard')
t = g.parse("MAP NAME 'Test' END")
print(t)
pydot__tree_to_png(t, r"C:\temp\tree.png")
print(t.pretty())
