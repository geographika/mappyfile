r"""
Create MapServer class diagrams

Requires https://graphviz.gitlab.io/_pages/Download/Download_windows.html
https://stackoverflow.com/questions/1494492/graphviz-how-to-go-from-dot-to-a-graph

For DOT languge see http://www.graphviz.org/doc/info/attrs.html

cd C:\Program Files (x86)\Graphviz2.38\bin
dot -Tpng D:\GitHub\mappyfile\mapfile_classes.dot -o outfile.png
outfile.png

For Entity Relationship diagrams:

https://graphviz.readthedocs.io/en/stable/examples.html#er-py

"""

import os
import pydot
# import pprint


FONT = "Lucida Sans"


def graphviz_setup(gviz_path):
    os.environ['PATH'] = gviz_path + ";" + os.environ['PATH']


def add_child(graph, child_id, child_label, parent_id, colour):
    """
    http://www.graphviz.org/doc/info/shapes.html#polygon
    """
    node = pydot.Node(child_id, style="filled", fillcolor=colour, label=child_label, shape="polygon", fontname=FONT)
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
        add_children(graph, child_id, children, level+1)


def save_file(graph, fn):
    filename = "%s.png" % fn
    graph.write_png(filename)
    graph.write("%s.dot" % fn)
    os.startfile(filename)


def main(gviz_path, layer_only=False):

    graphviz_setup(gviz_path)
    graph = pydot.Dot(graph_type='digraph', rankdir="TB")

    layer_children = {
            'CLASS': {
                'LABEL': {'STYLE': {}},
                'CONNECTIONOPTIONS': {},
                'LEADER': {'STYLE': {}},
                'STYLE': {},
                'VALIDATION': {}
            },
            'CLUSTER': {},
            'COMPOSITE': {},
            'FEATURE': {'POINTS': {}},
            'GRID': {},
            'JOIN': {},
            'METADATA': {},
            'PROJECTION': {},
            'SCALETOKEN': {'VALUES': {}},
            'VALIDATION': {}
     }

    # pprint.pprint(layer_children)

    classes = {
        "MAP": {
            "LAYER": layer_children,
            'LEGEND': {'LABEL': {}},
            'PROJECTION': {},
            'QUERYMAP': {},
            'REFERENCE': {},
            'SCALEBAR': {'LABEL': {}},
            'SYMBOL': {},
            'WEB': {'METADATA': {}, 'VALIDATION': {}}
        }
     }

    if layer_only:
        root = "LAYER"
        classes = classes["MAP"]
        fn = "layer_classes"
    else:
        fn = "map_classes"
        root,  = classes.keys()

    node = pydot.Node(root, style="filled", fillcolor="#33a333", label=root, fontname=FONT, shape="polygon")
    graph.add_node(node)
    add_children(graph, root, classes[root])
    save_file(graph, fn)


if __name__ == "__main__":
    gviz_path = r"C:\Program Files (x86)\Graphviz2.38\bin"
    main(gviz_path, True)
    main(gviz_path, False)
    print("Done!")
