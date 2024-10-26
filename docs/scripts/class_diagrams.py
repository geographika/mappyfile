r"""
Create MapServer class diagrams

Requires https://graphviz.gitlab.io/_pages/Download/Download_windows.html (tested with graphviz-11.0.0 (64-bit) EXE installer)
For DOT language see http://www.graphviz.org/doc/info/attrs.html
See also https://stackoverflow.com/questions/1494492/graphviz-how-to-go-from-dot-to-a-graph
For Entity Relationship diagram example see https://graphviz.readthedocs.io/en/stable/examples.html#er-py


pip install pydot

# to generate diagrams run the following in PowerShell

C:\VirtualEnvs\mappyfile3\Scripts\activate.ps1
$env:Path = "C:\Program Files\Graphviz\bin;" + $env:Path
# dot -Tpng D:\GitHub\mappyfile\mapfile_classes.dot -o outfile.png

cd D:\GitHub\mappyfile\docs\scripts
python class_diagrams.py
"""

import os
import pydot

FONT = "Lucida Sans"


def add_child(graph, child_id, child_label, parent_id, colour):
    """
    http://www.graphviz.org/doc/info/shapes.html#polygon
    """
    node = pydot.Node(
        child_id,
        style="filled",
        fillcolor=colour,
        label=child_label,
        shape="polygon",
        fontname=FONT,
    )
    graph.add_node(node)
    graph.add_edge(pydot.Edge(parent_id, node))


def add_children(graph, parent_id, d, level=0):
    blue = "#6b6bd1"
    white = "#fdfefd"
    green = "#33a333"
    colours = [blue, white, green] * 3

    for class_, children in d.items():
        colour = colours[level]
        child_label = class_
        child_id = parent_id + "_" + class_
        add_child(graph, child_id, child_label, parent_id, colour)
        add_children(graph, child_id, children, level + 1)


def save_file(graph, fn):
    filename = "%s.png" % fn
    graph.write_png(filename)
    graph.write("%s.dot" % fn)
    os.startfile(filename)


def layer_children():
    return {
        "CLASS": {
            "LABEL": {"STYLE": {}},
            "CONNECTIONOPTIONS": {},
            "LEADER": {"STYLE": {}},
            "STYLE": {},
            "VALIDATION": {},
        },
        "CLUSTER": {},
        "COMPOSITE": {},
        "FEATURE": {"POINTS": {}},
        "GRID": {},
        "JOIN": {},
        "METADATA": {},
        "PROJECTION": {},
        "SCALETOKEN": {"VALUES": {}},
        "VALIDATION": {},
    }


def map_children():
    return {
        "MAP": {
            "LAYER": layer_children(),
            "LEGEND": {"LABEL": {}},
            "PROJECTION": {},
            "QUERYMAP": {},
            "REFERENCE": {},
            "SCALEBAR": {"LABEL": {}},
            "SYMBOL": {},
            "WEB": {"METADATA": {}, "VALIDATION": {}},
        }
    }


def simple_classes():
    return {
        "MAP": {
            "LAYER": {
                "CLASS": {
                    "STYLE": {},
                }
            },
            "PROJECTION": {},
            "SYMBOL": {},
            "WEB": {
                "METADATA": {},
            },
        }
    }


def very_simple_classes():
    return {
        "MAP": {
            "LAYER": {
                "CLASS": {
                    "STYLE": {},
                }
            },
            "PROJECTION": {},
            "WEB": {
                "METADATA": {},
            },
        }
    }


def generate_graph(root, classes, fn):
    graph = pydot.Dot(graph_type="digraph", rankdir="TB")
    node = pydot.Node(
        root,
        style="filled",
        fillcolor="#33a333",
        label=root,
        fontname=FONT,
        shape="polygon",
    )
    graph.add_node(node)
    add_children(graph, root, classes[root])
    save_file(graph, fn)


def main():

    # pprint.pprint(layer_children)
    classes = map_children()
    generate_graph(root="LAYER", classes=classes["MAP"], fn="layer_classes")
    generate_graph(root="MAP", classes=classes, fn="map_classes")
    generate_graph(root="MAP", classes=simple_classes(), fn="simple_classes")
    generate_graph(root="MAP", classes=very_simple_classes(), fn="very_simple_classes")


if __name__ == "__main__":
    main()
    print("Done!")
