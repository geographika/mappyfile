from collections import OrderedDict

# Constant used to as the dict key to store
# the Mapfile object type e.g. MAP, LAYER, STYLE

MAPFILE_TYPE = "__type__"

class NonQuotedList(list):
    """
    Used for property lists that should be left unquoted. 
    E.g. a POINTS block can be defined as follows:

    POINTS
        0 100
        100 200
        40 90
    END
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

class NonQuotedString(str):
    """
    Used for property values which aren't quoted.
    E.g.

    + WIDTH 1
    + COLOR 255 0 0
    """
    pass

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

class PrettyPrinter:
    def __init__(self, indent=4, spacer=" ", quote="'", lfchar="\n"):
        """
        Option use "\t" for spacer with an indent of 1
        """
        self.indent = indent
        self.spacer = spacer * self.indent
        self.lfchar = lfchar
        self.quote = quote
        self.end = "END"

    def quote_value(self, v):
        return "%s%s%s" % (self.quote, str(v), self.quote)

    def format_list(self, val, spacer):
        """
        Print out a list of values
        """

        if isinstance(val, QuotedList):
            vals = map(self.quote_value, val)
        elif isinstance(val, NonQuotedList):
            vals = map(str, val)
        else:
            raise ValueError("Unknown type %s for %s!" % (type(val), val))
    
        s = self.lfchar.join([spacer + v for v in vals])

        return s

    def format_value(self, val):
        """
        Print out a string
        """
        if isinstance(val, QuotedString):
            v = self.quote_value(val)               
        elif isinstance(val, NonQuotedString):
            v = str(val)
        else:
            raise ValueError("Unknown type %s for %s!" % (type(val), val))

        return v

    def pprint(self, container):
        """
        Print out a nicely indented Mapfile
        """
        lines = self._format(container)
        return self.lfchar.join(lines)

    def _format(self, container, level=0):

        lines = []

        if isinstance(container, Container):
            type_ = container[MAPFILE_TYPE].upper()
            s = self.spacer * level + type_                           
            lines.append(s)
            items = container.items()
        else:
            assert(isinstance(container, HiddenContainer))
            items = enumerate(container)

        for key, value in items: 
            if isinstance(value, HiddenContainer):
                # now recursively print all the items in the container
                for v in value:
                    lines += self._format(v, level + 1)
            elif isinstance(value, Container):
                lines += self._format(value, level)
            else:
                if key != MAPFILE_TYPE:
                    # properties
                    spacer = self.spacer * (level + 1)
                    ukey = str(key).upper()

                    if isinstance(value, (QuotedList, NonQuotedList)):
                        list_spacer = self.spacer * (level + 2)
                        s = self.format_list(value, list_spacer)
                        lines.append(spacer + ukey)
                        lines.append(s)
                        s = self.spacer * (level + 1) + self.end
                        lines.append(s)
                    else:
                        myval = self.format_value(value)
                        s = spacer + ukey + " " + myval
                        lines.append(s)

        if isinstance(container, Container):            
            s = self.spacer * level + self.end
            lines.append(s)

        return lines