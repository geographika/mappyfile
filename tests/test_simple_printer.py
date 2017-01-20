from collections import OrderedDict

# constants / types
IGNORE = 0
CONTAINER = 1
QUOTED = 2
NONQUOTED = 3

# alias names for different group types
aliases = {
    "layers": "LAYER",
    "classes": "CLASS",
    "styles": "STYLE",
    "features": "FEATURE"    
    # TODO - check for more groups
    }

def create_sample_dict():
    style1 = OrderedDict()
    sn1 = "0"
    style1["color"] = ("99 231 117", NONQUOTED)
    style1["width"] = ("1", NONQUOTED)

    style2 = OrderedDict()
    sn2 = "MyStyle"
    style2["name"] = (sn2, QUOTED)
    style2["color"] = ("108 201 187", NONQUOTED)
    style2["width"] = ("2", NONQUOTED)

    styles = OrderedDict()
    styles["0"] = (style1, CONTAINER)
    styles[sn2] = (style2, CONTAINER)

    class1 = OrderedDict()
    cn1 = "Class1"
    class1["name"] = (cn1, QUOTED)
    class1["styles"] = (styles, IGNORE)

    classes = OrderedDict()
    classes[cn1] = (class1, CONTAINER)

    layer1 = OrderedDict()
    ln1 = "Layer1"
    layer1["name"] = (ln1, QUOTED)
    layer1["classes"] = (classes, IGNORE)

    points = ["0 100", "100 200", "40 90"]

    feature1 = OrderedDict()
    feature1["points"] = (points, NONQUOTED)
    features = OrderedDict()  

    features["0"] = (feature1, NONQUOTED)

    layer1["features"] = (features, IGNORE)

    ln2 = "Layer2"
    layer2 = OrderedDict()
    layer2["name"] = (ln2, QUOTED)

    layers = OrderedDict()
    layers[ln1] = (layer1, CONTAINER)
    layers[ln2] = (layer2, CONTAINER)

    map_ = OrderedDict()

    projection = ["proj=utm", "ellps=GRS80", "datum=NAD83", "zone=15", "units=m", "north", "no_defs"]
    map_["projection"] = (projection, QUOTED)

    map_["layers"] = (layers, IGNORE)

    return map_

def quote_value(v):
    return "'%s'" % str(v)

def format_list(val, type_, spacer):
    """
    Print out a list of values
    """
    if type_ == QUOTED:
        vals = map(quote_value, val)
    elif type_ == NONQUOTED:
        vals = map(str, val)
    else:
        raise ValueError("Unknown type %s!" % str(type_))
    
    s = "\n".join([spacer + v for v in vals])

    return s

def format_value(val, type_):
    """
    Print out a string
    """
    if type_ == QUOTED:
        v = quote_value(val)               
    elif type_ == NONQUOTED:
        v = str(val)
    else:
        raise ValueError("Unknown type %s!" % str(type_))

    return v

def pretty_print(d, indent=0, space="\t", parent=None):

    lines = []

    for key, value in d.iteritems(): 
        v = value[0]
        type_ = value[1]

        if isinstance(v, OrderedDict):
            # containers
            if type_ != IGNORE: # ignore grouping dicts
                s = space * indent + parent                           
                lines.append(s)
                new_indent = indent
            else:
                new_indent = indent + 1
                parent = aliases[key]

            lines += pretty_print(v, new_indent, space=space, parent=parent)
        else:
            # properties
            spacer = space * (indent + 1)
            ukey = str(key).upper()
            if isinstance(v, list):
                list_spacer = space * (indent + 2)
                s = format_list(v, type_, list_spacer)
                lines.append(spacer + ukey)
                lines.append(s)
                s = space * (indent + 1) + "END"
                lines.append(s)
            else:
                myval = format_value(v, type_)
                s = spacer + ukey + " " + myval
                lines.append(s)

        if type_ == CONTAINER:            
            s = space * indent + "END"
            lines.append(s)

    return lines

map_ = create_sample_dict()

lines = pretty_print(map_, space="    ")
lines.insert(0, "MAP")
lines.append("END")

print("\n".join(lines))
