import sys
is_python3 = sys.version_info.major == 3
if is_python3:
    unicode = str
    
from mappyfile.tokens import COMPOSITE_NAMES, ATTRIBUTE_NAMES, SINGLETON_COMPOSITE_NAMES

class PrettyPrinter(object):
    def __init__(self, indent=4, spacer=" ", quote="'", newlinechar="\n"):
        """
        Option use "\t" for spacer with an indent of 1
        """

        assert (quote == "'" or quote == '"')

        self.indent = indent
        self.spacer = spacer * self.indent
        self.newlinechar = newlinechar
        self.quote = quote
        self.end = u"END"

        if self.quote == "'":
            self.altquote = '"'
        else:
            self.altquote = "'"

    def whitespace(self, level, indent):

        return self.spacer * (level + indent)

    def singular(self, s):
        if s == 'points':
            return s
        elif s.endswith('es'):
            return s[:-2]
        return s[:-1]

    def is_block_list(self, lst):

        if len(lst) == 1 and isinstance(lst[0], list):
            return True
        else:
            return False

    def all_keywords(self):

        return COMPOSITE_NAMES.union(ATTRIBUTE_NAMES).union(SINGLETON_COMPOSITE_NAMES)

    def process_dict(self, key, d, level):

        lines = []
        lines.append(self.whitespace(level, 1) + self.format_key(key))

        for k, v in d.items():
            lines.append(self.format_line(self.whitespace(level, 2), k, v))

        lines.append(self.whitespace(level, 1) + self.end)

        return lines

    def process_list(self, key, lst, level):
        
        lines = []
        spacer = self.spacer * (level + 1)


        block_list = self.is_block_list(lst)

        # add the items in the list

        if block_list:
            # add KEYWORD to signify start of block
            lines.append(spacer + self.format_key(key))
            list_spacer = self.spacer * (level + 2)
            s = self.format_list(lst[0], list_spacer)
            lines.append(s)
        else:
            # put all values on same line
            if key == 'processing':
                for v in lst:
                    lines.append(self.format_line(spacer, key, v))
            else:
                s = " ".join(map(self.format_value, lst))
                s = self.format_line(spacer, key, s)
                lines.append(s)
       
        if block_list:
            # add END to close the block
            s = self.spacer * (level + 1) + self.end
            lines.append(s)

        return lines


    def format_list(self, val, spacer):
        """
        Print out a list of values
        """

        vals = map(str, val)  
        s = self.newlinechar.join([spacer + v for v in vals])

        return s

    def format_attribute(self, val):

        if self.in_quotes(val):
            val = self.standardise_quotes(val)
        else:
            val = self.add_quotes(val)

        return self.format_value(val)

    def format_value(self, val):
        """
        Print out a string
        """

        if isinstance(val, (unicode, str)):
            val = self.standardise_quotes(val)
        
        try:
            val = unicode(val)
        except UnicodeDecodeError:
            # obj is byte string
            ascii_text = str(val).encode('string_escape')
            val = unicode(ascii_text)

        return val

    def add_quotes(self, val):
        return "%s%s%s" % (self.quote, val, self.quote)

    def in_quotes(self, val):

        if (val.startswith(self.quote) and val.endswith(self.quote)) \
            or  (val.startswith(self.altquote) and val.endswith(self.altquote)):
            return True
        else:
            return False

    def standardise_quotes(self, val):

        if val.startswith(self.altquote) and val.endswith(self.altquote):
            val = "%s%s%s"  % (self.quote, val[1:-1], self.quote)

        return val

    def format_key(self, key):
        """
        All non-quoted keys should be un uppercase
        Otherwise do not modify input
        """

        if self.in_quotes(key):
            key = self.format_value(key) 
        else:
            if key in self.all_keywords():
                key = self.format_value(key.upper())
            else:
                key = self.format_value(self.add_quotes(key.lower()))

        return key

    def format_line(self, spacer, key, value):

        tmpl = u"{spacer}{key} {value}"
        d = {
            "spacer": spacer,
            "key": self.format_key(key),
            "value": self.format_value(value)
            }
        return tmpl.format(**d)

    def is_composite(self, val):

        if isinstance(val, dict) and "__type__" in val.keys():
            return True
        else:
            return False

    def is_hidden_container(self, key, val):
        """
        The key is not one of the Mapfile keywords, and its 
        values are a list
        """

        if key not in self.all_keywords() and isinstance(val, list):
            return True
        else:
            return False

    def pprint(self, composite):
        """
        Print out a nicely indented Mapfile
        """
        lines = self._format(composite)
        return self.newlinechar.join(lines)

    def _format(self, composite, level=0):
        """
        TODO Refactor this and create functions for each unique type
        """
        lines = []
        if isinstance(composite, dict) and  '__type__' in composite.keys():
            type_ = composite['__type__']
            assert(type_ in COMPOSITE_NAMES.union(SINGLETON_COMPOSITE_NAMES))
            is_hidden = False
            s = self.whitespace(level, 0) + type_ .upper()                          
            lines.append(s)
            # we can now filter out the type property so the rest of the 
            # values are displayed
            items = ((k, v) for k, v in composite.items() if k != '__type__')
        else:
            # hidden container
            assert(len(composite.keys()) == 1)
            is_hidden = True
            items = enumerate(composite.values()[0])

        for key, value in items:             
            if self.is_hidden_container(key, value): # HiddenContainer
                # now recursively print all the items in the container
                if self.is_block_list(value):
                    k = self.singular(key)
                    lines += self.process_list(k, value, level)
                else:
                    for v in value:
                        lines += self._format(v, level + 1)

            elif self.is_composite(value): # Container
                lines += self._format(value, level + 1)
            else:
                if key in SINGLETON_COMPOSITE_NAMES:
                    lines += self.process_dict(key, value, level)
                elif isinstance(value, dict): 
                    if key == "config":
                        # config declaration allows for pairs of values
                        value = ["%s %s" % (self.format_key(k), self.format_attribute(v)) for k,v in value.items()]
                    for v in value:                        
                        lines.append(self.format_line(self.whitespace(level, 1), key, v))
                elif isinstance(value, list):
                    lines += self.process_list(key, value, level)
                else:
                    lines.append(self.format_line(self.whitespace(level, 1), key, value))

        if not is_hidden: # Container
            # close the container block with an END            
            s = self.whitespace(level, 0) + self.end
            lines.append(s)

        return lines
