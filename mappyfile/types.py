from collections import OrderedDict

# Constant used to as the dict key to store
# the Mapfile object type e.g. MAP, LAYER, STYLE

MAPFILE_TYPE = "__type__"

#class NonQuotedList(list):
#    """
#    Used for property lists that should be left unquoted. 
#    E.g. a POINTS block can be defined as follows:

#    POINTS
#        0 100
#        100 200
#        40 90
#    END
#    """
#    pass

class KeyValueList(list):
    """
    PROCESSING "BANDS=1"
    PROCESSING "CONTOUR_ITEM=elevation"
    PROCESSING "CONTOUR_INTERVAL=20"
    """
    pass

class QuotedList(list):
    """
    Used for property lists that should be quoted. 
    E.g. the PROJECTION block can be defined as follows:

    PROJECTION
        'proj=utm'
        'ellps=GRS80'
        'datum=NAD83'
        'zone=15'
        'units=m'
        'north'
        'no_defs'
    END

    """
    pass

class QuotedString(str):
    """
    Used for quoted property values
    E.g.

    + NAME "Layer1"
    + DATA "lakes.shp"
    """
    pass

#class NonQuotedString(str):
#    """
#    Used for property values which aren't quoted.
#    E.g.

#    + WIDTH 1
#    + COLOR 255 0 0
#    """
#    pass

class HiddenContainer(list):
    """"
    These containers are not outputted as part of the pprint
    They are used to store objects of the same type
    E.g. LAYERs, CLASSes, STYLEs
    """
    pass

class Container(OrderedDict):
    """
    This is for container declarations which finish with the
    keyword END. Examples:
    
    + MAP ... END
    + LAYER ... END
    + CLASS ... END
    + STYLE ... END
    """
    pass