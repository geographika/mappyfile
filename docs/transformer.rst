Transforming the Parsed File
============================

+ *To allow updates of objects and properties would the best approach may be to use a transformer to change the tree into a OrderedDict type class? 
  STree objects are read-only?*
+ *How can STree collections be turned into a nested dictionary type object?*
  It would then need to be turned back into a tree object to use the STransformer class for pretty printing and creating diagrams. 
  *Alternatively a pretty printing function could be used directly on the dictionary type Mapfile class?* The pydot diagrams however are a nice feature. 
+ Could one approach be to write the dict to a Mapfile string and reparse this for diagrams?

For example taking the Mapfile below:

.. code-block:: mapfile
   
    MAP
        WEB
            METADATA
                "wms_enable_request"  "*"
            END
        END
        PROJECTION
            "init=epsg:4326"
        END
        LAYER
            NAME 'layer1'
            CLASS
                NAME 'class1'
                STYLE
                    COLOR 107 208 107
                    WIDTH 1
                END
            END
            CLASS
                NAME 'class2'
                STYLE
                    COLOR 10 108 207
                    WIDTH 1
                END
            END			
        END
        LAYER
            NAME 'layer2'
            CLASS
                STYLE
                    COLOR 99 231 117
                    WIDTH 1
                END
            END
        END		
    END
	
Would become a nested dictionary similar to below. 

.. code-block:: python

    {
      "map": {
        "web": {
          "metadata": {
            "wms_enable_request": "*"
          }
        },       
        "projection": ["init=epsg:4326"],      
        "layers": {
          "layer1": {
            "name": "layer1",
            "classes": {
              "class1": {
                "name": "class1", 
                "styles": {
                  "0": {
                    "color": "107 208 107", 
                    "width": 1
                  }
                }
              }, 
              "class2": {
                "name": "class2", 
                "styles": {
                  "0": {
                    "color": "10 108 207", 
                    "width": 1
                  }
                }
              }
            }
          }, 
          "layer2": {
            "name": "layer2",
            "classes": {
              "0": {
                "styles": {
                  "0": {
                    "color": "99 231 117", 
                    "width": 1
                  }
                }
              }
            }
          }
        }
      }
    }
    
Notes on the above:

+ Objects that can have multiple instances in a Mapfile will be stored as a OrderedDict of Dicts (as order is important).
  The ``NAME`` value of the object will be used for the key. If this is not present then the index can be used.  These keys ignored when outputting 
  the representation back to a Mapfile. 
+ Most objects have a set of key/value pairs. ``PROJECTION`` however should be treated as a list 
  (see http://www.mapserver.org/mapfile/projection.html).
+ Some keys are already quoted e.g. in the ``METADATA`` object items such as "wms_enable_request" are strings rather than keywords. Maybe values need to be tuples to
  record this e.g. ``"wms_enable_request": ("*", False)`` where ``False`` is to indicate the key is not a keyword. This can be checked when outputting to text so the key is quoted. 
+ Some keys are duplicated within an object. E.g.

  .. code-block:: mapfile
  
        PROCESSING "BANDS=1"
        PROCESSING "CONTOUR_ITEM=elevation"
        PROCESSING "CONTOUR_INTERVAL=20"
        
        # Same for POINTS
        
  Could turn this into a list? E.g.
  
  .. code-block:: python
  
      "layer": {
        "processing": ["BANDS=1", "CONTOUR_ITEM=elevation", "CONTOUR_INTERVAL=20"]
      }
      
      # to update and manipulate then use an API such as below
      layer["processing"][0] = "BANDS=1,2,3"

  
Implementation Notes
++++++++++++++++++++

+ Use iterators for the dicts? See http://stackoverflow.com/a/4391722/179520 for making these iterators. 
+ If iterators are used then they will need to be converted to lists when accessed

  .. code-block:: python

	  # depending on if an iterator approach is used may need to do something like the below
	  layers = list(d.items()) # for Python 3 and iterator approach- http://stackoverflow.com/questions/10058140/accessing-items-in-a-ordereddict

+ Could make use of https://github.com/bcj/AttrDict to allow property-like access to dictionary objects (see proposed API examples below)?
	