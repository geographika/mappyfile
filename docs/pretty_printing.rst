.. _pretty-printing:
    
Pretty Printing
===============

+ Any ``INCLUDE`` directives will have been parsed and treated as part of the original Mapfile 
  so there will never be any ``INCLUDE`` keywords in the output
+ Indentation can be set as an option e.g. 2 or 4 spaces

Taking an input similar to below:

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

    # START OF THE LAYER DEFINITION
    LAYER
    NAME 'land'
    TYPE POLYGON
    DATA '../data/vector/naturalearth/ne_110m_land'
    # START OF THE CLASS DEFINITION
    CLASS
    # START OF THE STYLE DEFINITION
    STYLE
    COLOR 107 208 107
    OUTLINECOLOR 2 2 2
    WIDTH 1
    END
    END
    END
    END

``mappyfile`` will output a nicely indented version.

.. code-block:: python

    mf = r"C:\Mapfiles\example.map"
    mapfile = mappyfile.parse(mf)

    with open('compact.map', 'w') as mf2:
        mapfile.write(mf2, indent=4, with_comments=False)
        
Output:

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
            NAME 'land'
            TYPE POLYGON
            DATA '../data/vector/naturalearth/ne_110m_land'
            CLASS
                STYLE
                    COLOR 107 208 107
                    OUTLINECOLOR 2 2 2
                    WIDTH 1
                END
            END
        END
    END