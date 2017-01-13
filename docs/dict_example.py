import pprint
from collections import OrderedDict
import json

pp = pprint.PrettyPrinter(indent=4)

d = OrderedDict()

layers = OrderedDict()

classes = OrderedDict({
"class1": {"name": "class1","styles": OrderedDict({"0": {"color": "107 208 107", "width": 1 }})},
"class2": {"name": "class2", "styles": OrderedDict({"1": {"color": "10 108 207", "width": 1 }})}
})

layers["layer1"] = OrderedDict(
    {"name": "layer1",
     "classes": classes
     })
    
layers["layer2"] = OrderedDict({"name": "layer2",
                    "classes": OrderedDict({"name": "0",
                                "styles": OrderedDict({"0": {"color": "99 231 117",
                                          "width": 1
                                          }})}
                                           )
                })

    
pp.pprint(layers)

m = OrderedDict({"map":
                 OrderedDict({
"web": {"metadata": {"wms_enable_request": "*"}},
"projection": "init=epsg:4326",
                     "layers": layers})})

pp.pprint(m)

print json.dumps(m, sort_keys=True, indent=4)

"""
d = {
        "map": {
            "web": {
                    "metadata": {
"wms_enable_request": "*"
                        }
                }
    }
        "projection": "init=epsg:4326"
}


pp.pprint(d)
"""
