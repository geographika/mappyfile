from mappyfile.types import *

class PrettyPrinter(object):
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
        else:
            assert(isinstance(val, list))
            vals = map(str, val)    

        s = self.lfchar.join([spacer + v for v in vals])

        return s

    def format_value(self, val):
        """
        Print out a string
        """
        if isinstance(val, QuotedString):
            val = self.quote_value(val)               
        else:
            val = str(val)

        return val

    def format_key(self, key):
        """
        All non-quoted keys should be un uppercase
        Otherwise do not modify input
        """
        if isinstance(key, QuotedString):
            key = self.format_value(key) 
        else:
            key = self.format_value(key.upper())

        return key

    def format_line(self, spacer, key, value):

        tmpl = "{spacer}{key} {value}"
        d = {
            "spacer": spacer,
            "key": self.format_key(key),
            "value": self.format_value(value)
            }
        return tmpl.format(**d)


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
            # we can now filter out the type property
            items = ((k, v) for k, v in container.items() if k != MAPFILE_TYPE)
        else:
            assert(isinstance(container, HiddenContainer))
            items = enumerate(container)

        for key, value in items: 
            if isinstance(value, HiddenContainer):
                # now recursively print all the items in the container
                for v in value:
                    lines += self._format(v, level + 1)
            elif isinstance(value, Container):
                lines += self._format(value, level + 1)
            else:
                # properties
                spacer = self.spacer * (level + 1)

                if isinstance(value, KeyValueList):
                    for v in value:
                        lines.append(self.format_line(spacer, key, v))
                elif isinstance(value, list):
                    # add KEYWORD to signify start of block
                    lines.append(spacer + self.format_key(key))

                    # add the items in the list
                    list_spacer = self.spacer * (level + 2)
                    s = self.format_list(value, list_spacer)
                    lines.append(s)

                    # add END to close the block
                    s = self.spacer * (level + 1) + self.end
                    lines.append(s)
                else:
                    lines.append(self.format_line(spacer, key, value))

        if isinstance(container, Container):
            # close the container block with an END            
            s = self.spacer * level + self.end
            lines.append(s)

        return lines